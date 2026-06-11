"""Local Windows client: web UI + polling thread for print jobs."""
import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import requests
from PIL import Image, ImageDraw
from flask import Flask, render_template, request, jsonify, send_file
from printer import (
    print_label, list_printers, render_label, render_dimensions,
    set_custom_emojis, set_custom_sizes, set_emoji_darkness, _BUILTIN_SIZE_KEYS,
    LABEL_SIZES, FONT_STYLES, FONT_WEIGHTS, BORDER_STYLES, TEXT_CASES,
    STYLE_PRESETS, STYLE_PRESET_GROUPS, WIN32_AVAILABLE,
    _IMAGE_BORDER_ENTRIES,
)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ── Config ───────────────────────────────────────────────────────────────────
RELAY_URL    = os.environ.get("RELAY_URL", "https://yourserver.com")
TOKEN        = os.environ.get("LABEL_TOKEN", "changeme")
POLL_SECS    = int(os.environ.get("POLL_SECS", "3"))

# Live connection config, editable from the (localhost-only) Advanced page and
# persisted to config.json. Effective value = saved override, else the .env
# default above. The poll loop reads this fresh each cycle, so changes apply
# without a restart.
runtime = {"relay_url": RELAY_URL, "token": TOKEN}
SHOUTRRR_URL = os.environ.get("SHOUTRRR_URL", "")

# Telegram credentials — initially parsed from SHOUTRRR_URL, overridable via
# config.json and the Advanced Settings page without restarting.
_TG_TOKEN   = None
_TG_CHAT    = None
_TG_ENABLED = True
_m = re.match(r"telegram://([^@]+)@telegram\?chats=(\d+)", SHOUTRRR_URL)
if _m:
    _TG_TOKEN, _TG_CHAT = _m.group(1), _m.group(2)

# Keys persisted to / loaded from settings.json
_SETTINGS_KEYS = ("printer", "size", "font_style", "font_weight", "border", "text_case", "text_align", "icons", "style_preset", "qr_show_text", "default_style")
_APP_DIR       = os.path.dirname(os.path.abspath(__file__))

# Store data in %APPDATA%\LabelPrinter — avoids OneDrive sync interference.
# LABEL_DATA_DIR overrides the location (used by tests so they never touch the
# live settings/history/config under %APPDATA%).
_DATA_DIR      = os.environ.get("LABEL_DATA_DIR") or os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")), "LabelPrinter")
os.makedirs(_DATA_DIR, exist_ok=True)
_SETTINGS_PATH   = os.path.join(_DATA_DIR, "settings.json")
_HISTORY_PATH    = os.path.join(_DATA_DIR, "history.json")
_ADDRESSES_PATH  = os.path.join(_DATA_DIR, "addresses.json")
_CONFIG_PATH     = os.path.join(_DATA_DIR, "config.json")
_CUSTOM_EMOJIS_PATH = os.path.join(_DATA_DIR, "custom_emojis.json")
_CUSTOM_SIZES_PATH  = os.path.join(_DATA_DIR, "custom_sizes.json")
_HISTORY_MAX     = 500

# One-time migration: copy settings.json from the old OneDrive location if it exists
# and the new location doesn't yet
_OLD_SETTINGS = os.path.join(_APP_DIR, "settings.json")
if os.path.isfile(_OLD_SETTINGS) and not os.path.isfile(_SETTINGS_PATH):
    try:
        import shutil
        shutil.copy2(_OLD_SETTINGS, _SETTINGS_PATH)
    except Exception:
        pass

_addresses = []   # list of {id, label, name, line1, line2, csz}

state = {
    "printer":    os.environ.get("DEFAULT_PRINTER", ""),
    "size":       os.environ.get("DEFAULT_SIZE", "2x1"),
    "font_style":   os.environ.get("DEFAULT_FONT_STYLE", "enhanced"),
    "font_weight":  os.environ.get("DEFAULT_FONT_WEIGHT", "bold"),
    "border":       os.environ.get("DEFAULT_BORDER", "none"),
    "text_case":    os.environ.get("DEFAULT_TEXT_CASE", "none"),
    "text_align":   "center",
    "style_preset": "none",
    "icons":        True,
    "qr_show_text":   True,
    "default_style":  None,   # saved via POST /style/default
    "history":    [],
    "polling":    True,
}

# ── Settings persistence ──────────────────────────────────────────────────────

def _load_settings():
    """Merge saved settings.json into state (silently ignored if missing/corrupt)."""
    try:
        with open(_SETTINGS_PATH) as f:
            saved = json.load(f)
        for key in _SETTINGS_KEYS:
            if key in saved:
                state[key] = bool(saved[key]) if key == "icons" else saved[key]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass


def _save_settings():
    """Persist the current user-facing settings to settings.json."""
    try:
        with open(_SETTINGS_PATH, "w") as f:
            json.dump({k: state[k] for k in _SETTINGS_KEYS}, f, indent=2)
    except Exception:
        pass


def _load_history():
    """Load saved print history from history.json into state."""
    try:
        with open(_HISTORY_PATH) as f:
            state["history"] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


def _save_history():
    """Persist the current print history to history.json."""
    try:
        with open(_HISTORY_PATH, "w") as f:
            json.dump(state["history"], f, indent=2)
    except Exception:
        pass


_emoji_darkness = 0   # 0–100, persisted in config.json


def _load_config():
    """Load runtime overrides (set via the Advanced page). Saved values win
    over .env defaults; missing keys keep their current value."""
    global _emoji_darkness, _TG_TOKEN, _TG_CHAT, _TG_ENABLED
    try:
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        if cfg.get("relay_url"):
            runtime["relay_url"] = cfg["relay_url"]
        if cfg.get("token"):
            runtime["token"] = cfg["token"]
        if "emoji_darkness" in cfg:
            _emoji_darkness = max(0, min(100, int(cfg["emoji_darkness"])))
            set_emoji_darkness(_emoji_darkness)
        if cfg.get("tg_token"):
            _TG_TOKEN = cfg["tg_token"]
        if "tg_chat" in cfg:
            _TG_CHAT = cfg["tg_chat"] or None
        if "tg_enabled" in cfg:
            _TG_ENABLED = bool(cfg["tg_enabled"])
    except (FileNotFoundError, json.JSONDecodeError):
        pass


def _save_config():
    """Persist runtime overrides to config.json (%APPDATA%\\LabelPrinter)."""
    try:
        with open(_CONFIG_PATH, "w") as f:
            json.dump({
                "relay_url":      runtime["relay_url"],
                "token":          runtime["token"],
                "emoji_darkness": _emoji_darkness,
                "tg_token":   _TG_TOKEN or "",
                "tg_chat":    _TG_CHAT  or "",
                "tg_enabled": _TG_ENABLED,
            }, f, indent=2)
    except Exception:
        pass


# ── Custom emojis ─────────────────────────────────────────────────────────────
# User-defined keyword → emoji overrides, edited on the Advanced page. Canonical
# form groups keywords per emoji: [{"emoji": "🍕", "keywords": ["pizza", "friday"]}]
_custom_emojis = []   # list of {emoji, keywords:[...], enabled:bool}


def _normalize_emojis(raw):
    """Validate/clean an incoming custom-emoji list. Drops entries with no emoji
    or no keywords; lowercases, trims and de-dupes keywords."""
    out = []
    for entry in (raw or [])[:200]:                       # cap entries
        if not isinstance(entry, dict):
            continue
        emoji = (entry.get("emoji") or "").strip()
        if not emoji or len(emoji) > 16:                  # 16 covers ZWJ/flag seqs
            continue
        seen, kws = set(), []
        for kw in (entry.get("keywords") or [])[:50]:     # cap keywords/entry
            kw = (str(kw) or "").strip().lower()
            if kw and kw not in seen:
                seen.add(kw)
                kws.append(kw)
        if kws:
            out.append({"emoji": emoji, "keywords": kws,
                        "enabled": bool(entry.get("enabled", True))})
    return out


def _emoji_flat_map():
    """Flatten enabled _custom_emojis to {keyword: emoji} for the printer."""
    flat = {}
    for entry in _custom_emojis:
        if not entry.get("enabled", True):
            continue
        for kw in entry["keywords"]:
            flat[kw] = entry["emoji"]
    return flat


def _apply_custom_emojis():
    set_custom_emojis(_emoji_flat_map())


def _load_custom_emojis():
    """Load custom_emojis.json into state and push it into the printer."""
    global _custom_emojis
    try:
        with open(_CUSTOM_EMOJIS_PATH, encoding="utf-8") as f:
            _custom_emojis = _normalize_emojis(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        _custom_emojis = []
    _apply_custom_emojis()


def _save_custom_emojis():
    try:
        with open(_CUSTOM_EMOJIS_PATH, "w", encoding="utf-8") as f:
            json.dump(_custom_emojis, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ── Custom label sizes ────────────────────────────────────────────────────────
# User-defined label sizes, edited on the Advanced page. Stored with the unit the
# user entered (in/mm/cm) so the UI round-trips; converted to inches for the
# render/print pipeline. Form: [{"name": "Euro Tag", "unit": "mm", "width": 50, "height": 25}]
_custom_sizes = []
_SIZE_UNITS   = {"in": 1.0, "mm": 1.0 / 25.4, "cm": 1.0 / 2.54}


def _normalize_sizes(raw):
    """Validate/clean an incoming custom-size list. Drops invalid entries, rejects
    names that collide with a built-in or another custom size (case-insensitive),
    and requires dimensions that convert to 0.1–24 inches."""
    builtin = {k.lower() for k in _BUILTIN_SIZE_KEYS}
    out, seen = [], set()
    for entry in (raw or [])[:50]:                        # cap entries
        if not isinstance(entry, dict):
            continue
        name = (entry.get("name") or "").strip()[:40]
        unit = (entry.get("unit") or "in").strip().lower()
        if not name or unit not in _SIZE_UNITS:
            continue
        low = name.lower()
        if low in builtin or low in seen:                 # no collisions / dupes
            continue
        try:
            w = float(entry.get("width"))
            h = float(entry.get("height"))
        except (TypeError, ValueError):
            continue
        f = _SIZE_UNITS[unit]
        if not (0.1 <= w * f <= 24 and 0.1 <= h * f <= 24):
            continue
        seen.add(low)
        out.append({"name": name, "unit": unit, "width": w, "height": h})
    return out


def _apply_custom_sizes():
    mapping = {s["name"]: (s["width"] * _SIZE_UNITS[s["unit"]],
                           s["height"] * _SIZE_UNITS[s["unit"]]) for s in _custom_sizes}
    set_custom_sizes(mapping)


def _load_custom_sizes():
    global _custom_sizes
    try:
        with open(_CUSTOM_SIZES_PATH, encoding="utf-8") as f:
            _custom_sizes = _normalize_sizes(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        _custom_sizes = []
    _apply_custom_sizes()


def _save_custom_sizes():
    try:
        with open(_CUSTOM_SIZES_PATH, "w", encoding="utf-8") as f:
            json.dump(_custom_sizes, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _size_options():
    """[(key, label)] for the Print Settings dropdown — built-ins shown in inches,
    custom sizes shown as 'Name (W × H unit)'."""
    custom = {s["name"]: s for s in _custom_sizes}
    opts = []
    for key in LABEL_SIZES:
        s = custom.get(key)
        if s:
            opts.append((key, f"{key} ({s['width']:g} × {s['height']:g} {s['unit']})"))
        else:
            opts.append((key, f"{key} inches"))
    return opts


def _load_addresses():
    """Load saved addresses from addresses.json."""
    try:
        with open(_ADDRESSES_PATH) as f:
            _addresses.extend(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass


def _save_addresses():
    """Persist saved addresses to addresses.json."""
    try:
        with open(_ADDRESSES_PATH, "w") as f:
            json.dump(_addresses, f, indent=2)
    except Exception:
        pass


# ── Telegram notification ─────────────────────────────────────────────────────

def _notify(text, size, source="manual", error=None):
    """Fire-and-forget Telegram message. Silently skipped if not configured or disabled."""
    if not (_TG_TOKEN and _TG_CHAT and _TG_ENABLED):
        return
    icon   = "🎙" if source == "voice" else "🖥"
    prefix = "❌" if error else "🖨"
    msg    = f'{prefix} {icon} {size} · "{text}"' + (f' · {error}' if error else '')
    try:
        requests.post(
            f"https://api.telegram.org/bot{_TG_TOKEN}/sendMessage",
            json={"chat_id": _TG_CHAT, "text": msg},
            timeout=5,
        )
    except Exception:
        pass


# ── Routes ────────────────────────────────────────────────────────────────────

def _is_local_request():
    """True only for requests from this PC. The Advanced page edits the relay
    token, so it must never be reachable from other LAN devices."""
    return request.remote_addr in ("127.0.0.1", "::1")


@app.route("/")
def index():
    return render_template(
        "index.html",
        printers=list_printers(),
        sizes=list(LABEL_SIZES.keys()),
        size_options=_size_options(),
        font_styles=FONT_STYLES,
        font_weights=FONT_WEIGHTS,
        border_styles=BORDER_STYLES,
        image_border_entries=_IMAGE_BORDER_ENTRIES,
        text_cases=TEXT_CASES,
        style_presets=STYLE_PRESETS,
        style_preset_groups=STYLE_PRESET_GROUPS,
        state=state,
        is_local=_is_local_request(),
    )


# ── Advanced settings (localhost only) ────────────────────────────────────────

@app.route("/advanced")
def advanced_page():
    if not _is_local_request():
        return ("Advanced settings can only be opened on the computer running "
                "Label Printer."), 403
    return render_template("advanced.html")


@app.route("/config/advanced", methods=["GET"])
def get_advanced():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    # Never return the token itself — only whether one is set (write-only field).
    return jsonify({
        "relay_url": runtime["relay_url"],
        "token_set": bool(runtime["token"]),
    })


@app.route("/config/advanced", methods=["POST"])
def set_advanced():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    data  = request.get_json(silent=True) or {}

    relay = (data.get("relay_url") or "").strip().rstrip("/")
    if relay:
        if not (relay.startswith("http://") or relay.startswith("https://")):
            return jsonify({"error": "Relay URL must start with http:// or https://"}), 400
        runtime["relay_url"] = relay

    # Write-only token: only overwrite when a non-empty value is supplied, so an
    # empty field means "keep the current token".
    token = (data.get("token") or "").strip()
    if token:
        runtime["token"] = token

    _save_config()
    return jsonify({"ok": True, "relay_url": runtime["relay_url"],
                    "token_set": bool(runtime["token"])})


@app.route("/config/advanced/test", methods=["POST"])
def test_advanced():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    data  = request.get_json(silent=True) or {}
    relay = (data.get("relay_url") or runtime["relay_url"] or "").strip().rstrip("/")
    token = (data.get("token") or "").strip() or runtime["token"]
    if not relay:
        return jsonify({"ok": False, "detail": "No relay URL set."})
    try:
        r = requests.get(f"{relay}/jobs/pending", headers={"X-Token": token}, timeout=8)
    except requests.RequestException as e:
        return jsonify({"ok": False,
                        "detail": f"Could not reach {relay} ({e.__class__.__name__})."})
    if r.status_code == 200:
        return jsonify({"ok": True, "detail": "Connected and authorized ✓"})
    if r.status_code == 401:
        return jsonify({"ok": False,
                        "detail": "Reached the server, but the token was rejected (401)."})
    return jsonify({"ok": False, "detail": f"Server responded with HTTP {r.status_code}."})


@app.route("/config/emojis", methods=["GET"])
def get_emojis():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    return jsonify(_custom_emojis)


@app.route("/config/emojis", methods=["POST"])
def set_emojis():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    global _custom_emojis
    data = request.get_json(silent=True) or {}
    raw  = data.get("emojis") if isinstance(data, dict) else data
    _custom_emojis = _normalize_emojis(raw)
    _save_custom_emojis()
    _apply_custom_emojis()
    return jsonify({"ok": True, "emojis": _custom_emojis})


@app.route("/config/sizes", methods=["GET"])
def get_sizes():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    return jsonify(_custom_sizes)


@app.route("/config/sizes", methods=["POST"])
def set_sizes():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    global _custom_sizes
    data = request.get_json(silent=True) or {}
    raw  = data.get("sizes") if isinstance(data, dict) else data
    _custom_sizes = _normalize_sizes(raw)
    _save_custom_sizes()
    _apply_custom_sizes()       # live — registers into LABEL_SIZES immediately
    return jsonify({"ok": True, "sizes": _custom_sizes})


@app.route("/config/emoji-darkness/preview")
def emoji_darkness_preview():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    import printer as _pm
    pct = max(0, min(100, int(request.args.get("pct", 0))))
    samples = ["😀", "🍕", "❤️", "⭐", "🔥"]
    icon_sz = 52
    pad = 10
    w = pad + len(samples) * (icon_sz + pad)
    h = icon_sz + pad * 2
    preview_img = Image.new("RGB", (w, h), "white")
    orig = _pm._EMOJI_DARKNESS
    _pm.set_emoji_darkness(pct)
    try:
        for i, emoji in enumerate(samples):
            _pm._draw_icon(preview_img, emoji, pad + i * (icon_sz + pad), pad, icon_sz)
    finally:
        _pm.set_emoji_darkness(orig)
    buf = io.BytesIO()
    preview_img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png", max_age=0)


@app.route("/config/emoji-darkness", methods=["GET"])
def get_emoji_darkness():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    return jsonify({"emoji_darkness": _emoji_darkness})


@app.route("/config/emoji-darkness", methods=["POST"])
def post_emoji_darkness():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    global _emoji_darkness
    data = request.get_json(silent=True) or {}
    val  = data.get("emoji_darkness")
    if val is None:
        return jsonify({"error": "emoji_darkness required"}), 400
    _emoji_darkness = max(0, min(100, int(val)))
    set_emoji_darkness(_emoji_darkness)
    _save_config()
    return jsonify({"ok": True, "emoji_darkness": _emoji_darkness})


@app.route("/config/telegram", methods=["GET"])
def get_telegram():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    return jsonify({
        "tg_enabled":   _TG_ENABLED,
        "tg_token_set": bool(_TG_TOKEN),
        "tg_chat":      _TG_CHAT or "",
    })


@app.route("/config/telegram", methods=["POST"])
def set_telegram():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    global _TG_TOKEN, _TG_CHAT, _TG_ENABLED
    data = request.get_json(silent=True) or {}
    if "tg_enabled" in data:
        _TG_ENABLED = bool(data["tg_enabled"])
    tg_token = (data.get("tg_token") or "").strip()
    if tg_token:
        _TG_TOKEN = tg_token
    if "tg_chat" in data:
        _TG_CHAT = (data["tg_chat"] or "").strip() or None
    _save_config()
    return jsonify({"ok": True, "tg_enabled": _TG_ENABLED,
                    "tg_token_set": bool(_TG_TOKEN), "tg_chat": _TG_CHAT or ""})


@app.route("/config/telegram/test", methods=["POST"])
def test_telegram():
    if not _is_local_request():
        return jsonify({"error": "forbidden"}), 403
    if not (_TG_TOKEN and _TG_CHAT):
        return jsonify({"ok": False, "detail": "No Telegram bot configured yet."})
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{_TG_TOKEN}/sendMessage",
            json={"chat_id": _TG_CHAT, "text": "🖨 Label Printer — test message ✓"},
            timeout=8,
        )
        if r.ok:
            return jsonify({"ok": True, "detail": "Test message sent ✓"})
        desc = r.json().get("description", f"HTTP {r.status_code}")
        return jsonify({"ok": False, "detail": f"Telegram error: {desc}"})
    except Exception as e:
        return jsonify({"ok": False,
                        "detail": f"Could not reach Telegram ({e.__class__.__name__})."})


@app.route("/config", methods=["POST"])
def set_config():
    data = request.get_json(silent=True) or {}
    for key in ("printer", "size", "font_style", "font_weight", "border", "text_case", "text_align", "style_preset"):
        if key in data:
            state[key] = data[key]
    if "icons" in data:
        state["icons"] = bool(data["icons"])
    if "qr_show_text" in data:
        state["qr_show_text"] = bool(data["qr_show_text"])
    _save_settings()
    return jsonify({"ok": True})


@app.route("/preview")
def preview():
    text         = request.args.get("text", "Label Printer")
    size         = request.args.get("size",         state["size"])
    font_style   = request.args.get("font_style",   state["font_style"])
    font_weight  = request.args.get("font_weight",  state["font_weight"])
    border       = request.args.get("border",       state["border"])
    text_case    = request.args.get("text_case",    state["text_case"])
    text_align   = request.args.get("text_align",   state["text_align"])
    style_preset = request.args.get("style_preset", state["style_preset"])
    icons        = request.args.get("icons", str(state["icons"])).lower() not in ("false", "0")
    qr_show_text = request.args.get("qr_show_text", str(state["qr_show_text"])).lower() not in ("false", "0")
    if size not in LABEL_SIZES:
        size = "2x1"
    # Brother tape renders landscape so the preview matches the printed output
    w, h = render_dimensions(size)
    img  = render_label(text, w, h, dpi=203, font_style=font_style, border=border,
                        icons=icons, text_case=text_case, style_preset=style_preset,
                        font_weight=font_weight, qr_show_text=qr_show_text,
                        text_align=text_align)
    buf  = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/print", methods=["POST"])
def manual_print():
    data        = request.get_json(silent=True) or {}
    text        = (data.get("text") or "").strip()
    size        = data.get("size",        state["size"])
    printer     = data.get("printer",     state["printer"])
    font_style  = data.get("font_style",  state["font_style"])
    font_weight = data.get("font_weight", state["font_weight"])
    border       = data.get("border",       state["border"])
    text_case    = data.get("text_case",    state["text_case"])
    text_align   = data.get("text_align",   state["text_align"])
    style_preset = data.get("style_preset", state["style_preset"])
    icons        = data.get("icons",        state["icons"])
    qr_show_text = data.get("qr_show_text", state["qr_show_text"])
    copies       = max(1, min(10, int(data.get("copies", 1))))

    if not text:
        return jsonify({"error": "no text"}), 400
    if not printer:
        return jsonify({"error": "no printer selected"}), 400
    try:
        for i in range(copies):
            if i > 0:
                time.sleep(0.5)
            print_label(text, printer, size, font_style=font_style, font_weight=font_weight,
                        border=border, icons=icons, text_case=text_case, style_preset=style_preset,
                        qr_show_text=qr_show_text, text_align=text_align)
        status_label = "ok" if copies == 1 else f"ok ×{copies}"
        _record(text, size, status_label, font_style=font_style, font_weight=font_weight,
                border=border, text_case=text_case, style_preset=style_preset, icons=icons)
        threading.Thread(target=_notify, args=(text, size, "manual"), daemon=True).start()
        return jsonify({"ok": True})
    except Exception as e:
        _record(text, size, f"error: {e}", font_style=font_style, font_weight=font_weight,
                border=border, text_case=text_case, style_preset=style_preset, icons=icons)
        threading.Thread(target=_notify, args=(text, size, "manual"),
                         kwargs={"error": str(e)}, daemon=True).start()
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def history():
    return jsonify(state["history"])


@app.route("/style/default", methods=["GET"])
def get_default_style():
    if state["default_style"] is None:
        return jsonify({"error": "no default saved"}), 404
    return jsonify(state["default_style"])


@app.route("/style/default", methods=["POST"])
def set_default_style():
    data = request.get_json(force=True) or {}
    allowed = {"style_preset", "font_style", "font_weight", "border", "text_case", "text_align", "icons"}
    style = {k: v for k, v in data.items() if k in allowed}
    state["default_style"] = style
    _save_settings()
    return jsonify({"ok": True})


@app.route("/addresses")
def list_addresses():
    return jsonify(_addresses)


@app.route("/addresses", methods=["POST"])
def save_address():
    data = request.get_json() or {}
    addr = {
        "id":    str(int(time.time() * 1000)),
        "label": data.get("label", "Address"),
        "name":  data.get("name",  ""),
        "line1": data.get("line1", ""),
        "line2": data.get("line2", ""),
        "csz":   data.get("csz",   ""),
    }
    _addresses.append(addr)
    _save_addresses()
    return jsonify({"ok": True, "id": addr["id"]})


@app.route("/addresses/delete", methods=["POST"])
def delete_address_entry():
    aid = (request.get_json() or {}).get("id")
    if aid:
        _addresses[:] = [a for a in _addresses if a["id"] != aid]
        _save_addresses()
    return jsonify({"ok": True})


@app.route("/history/delete", methods=["POST"])
def delete_history():
    ts = (request.get_json() or {}).get("ts")
    if ts:
        state["history"] = [h for h in state["history"] if h["ts"] != ts]
        _save_history()
    return jsonify({"ok": True})


@app.route("/history/clear", methods=["POST"])
def clear_history():
    state["history"] = []
    _save_history()
    return jsonify({"ok": True})


@app.route("/status")
def status():
    return jsonify({
        "printer":    state["printer"],
        "size":       state["size"],
        "font_style":  state["font_style"],
        "font_weight": state["font_weight"],
        "border":      state["border"],
        "text_case":    state["text_case"],
        "text_align":   state["text_align"],
        "style_preset": state["style_preset"],
        "icons":        state["icons"],
        "qr_show_text": state["qr_show_text"],
        "polling":    state["polling"],
        "relay":      runtime["relay_url"],
        "win32":      WIN32_AVAILABLE,
        "telegram":   bool(_TG_TOKEN),
    })

# ── Background polling ────────────────────────────────────────────────────────

def _record(text, size, status, *, font_style=None, font_weight=None, border=None,
            text_case=None, style_preset=None, icons=None):
    from datetime import datetime
    state["history"].insert(0, {
        "text":         text,
        "size":         size,
        "status":       status,
        "ts":           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "font_style":   font_style   if font_style   is not None else state["font_style"],
        "font_weight":  font_weight  if font_weight  is not None else state["font_weight"],
        "border":       border       if border        is not None else state["border"],
        "text_case":    text_case    if text_case     is not None else state["text_case"],
        "style_preset": style_preset if style_preset  is not None else state["style_preset"],
        "icons":        icons        if icons         is not None else state["icons"],
    })
    if len(state["history"]) > _HISTORY_MAX:
        state["history"] = state["history"][:_HISTORY_MAX]
    _save_history()


def poll_loop():
    while state["polling"]:
        # Read connection config fresh each cycle so Advanced-page edits apply
        # without a restart. Token always rides in the X-Token header — never the
        # URL query string, which would leak it into access logs.
        relay   = runtime["relay_url"]
        headers = {"X-Token": runtime["token"]}
        try:
            # ── Settings changes ──────────────────────────────────────────
            rs = requests.get(f"{relay}/settings/pending", headers=headers, timeout=10)
            if rs.ok:
                for change in rs.json():
                    key, value, cid = change["key"], change["value"], change["id"]
                    if key in ("font_style", "font_weight", "border", "text_case", "style_preset", "size"):
                        state[key] = value
                        _save_settings()
                    elif key == "icons":
                        state["icons"] = (value == "true")
                        _save_settings()
                    requests.post(f"{relay}/settings/{cid}/complete",
                                  headers=headers, timeout=5)
        except Exception:
            pass

        try:
            # ── Print jobs ────────────────────────────────────────────────
            r = requests.get(f"{relay}/jobs/pending", headers=headers, timeout=10)
            if r.ok:
                for job in r.json():
                    job_id  = job["id"]
                    text    = job["text"]
                    printer = state["printer"]
                    if not printer:
                        continue
                    try:
                        print_label(
                            text, printer, state["size"],
                            font_style=state["font_style"],
                            font_weight=state["font_weight"],
                            border=state["border"],
                            icons=state["icons"],
                            text_case=state["text_case"],
                            text_align=state["text_align"],
                            style_preset=state["style_preset"],
                            qr_show_text=state["qr_show_text"],
                        )
                        requests.post(f"{relay}/jobs/{job_id}/complete",
                                      headers=headers, timeout=5)
                        _record(text, state["size"], "ok (voice)",
                                font_style=state["font_style"], font_weight=state["font_weight"],
                                border=state["border"],
                                text_case=state["text_case"], style_preset=state["style_preset"],
                                icons=state["icons"])
                        threading.Thread(
                            target=_notify,
                            args=(text, state["size"], "voice"),
                            daemon=True,
                        ).start()
                    except Exception as e:
                        requests.post(f"{relay}/jobs/{job_id}/fail",
                                      headers=headers, timeout=5)
                        _record(text, state["size"], f"error: {e}",
                                font_style=state["font_style"], font_weight=state["font_weight"],
                                border=state["border"],
                                text_case=state["text_case"], style_preset=state["style_preset"],
                                icons=state["icons"])
                        threading.Thread(
                            target=_notify,
                            args=(text, state["size"], "voice"),
                            kwargs={"error": str(e)},
                            daemon=True,
                        ).start()
        except Exception:
            pass
        time.sleep(POLL_SECS)


# ── System tray ───────────────────────────────────────────────────────────────

def _make_tray_image():
    """Draw a simple printer icon for the system tray using Pillow."""
    sz = 64
    img = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    # Paper in feed slot (top)
    d.rectangle([18, 4, 46, 18], fill="#e2e8f0")
    # Printer body
    d.rounded_rectangle([4, 14, 60, 42], radius=6, fill="#1e293b")
    # Output tray (white paper coming out the bottom)
    d.rectangle([12, 32, 52, 58], fill="white")
    d.rectangle([12, 32, 52, 58], outline="#cbd5e1", width=2)
    # Blue label lines on output paper
    d.rectangle([18, 39, 46, 43], fill="#3b82f6")
    d.rectangle([18, 47, 36, 51], fill="#93c5fd")
    # Green status light on printer body
    d.ellipse([46, 20, 54, 28], fill="#22c55e")
    return img


def _run_tray():
    """Run the system tray icon (blocks — must be called from the main thread)."""
    import webbrowser
    try:
        import pystray
    except ImportError:
        return  # pystray not available; caller handles fallback

    def on_open(icon, item):
        webbrowser.open("http://localhost:5000")

    def on_restart(icon, item):
        # Find pythonw.exe next to the current interpreter so the new
        # instance stays in the background (no console window).
        py_dir  = os.path.dirname(sys.executable)
        pythonw = os.path.join(py_dir, "pythonw.exe")
        if not os.path.exists(pythonw):
            pythonw = sys.executable          # fallback: regular python
        env = os.environ.copy()
        env["LABEL_PRINTER_RESTART"] = "1"   # skip browser auto-open on restart
        subprocess.Popen(
            [pythonw, os.path.join(_APP_DIR, "app.py")],
            cwd=_APP_DIR,
            env=env,
        )
        icon.stop()
        os._exit(0)

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("Open Label Printer", on_open, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Restart", on_restart),
        pystray.MenuItem("Quit", on_quit),
    )
    icon = pystray.Icon("label_printer", _make_tray_image(), "Label Printer", menu)
    icon.run()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _load_config()
    _load_settings()
    _load_history()
    _load_addresses()
    _load_custom_emojis()
    _load_custom_sizes()

    printers = list_printers()
    if printers and not state["printer"]:
        state["printer"] = printers[0]

    threading.Thread(target=poll_loop, daemon=True).start()

    try:
        import pystray  # noqa: F401 — just checking availability
        import webbrowser

        # pystray must own the main thread on Windows, so Flask runs in a thread
        flask_thread = threading.Thread(
            target=lambda: app.run(
                host="0.0.0.0", port=5000, debug=False, use_reloader=False
            ),
            daemon=True,
        )
        flask_thread.start()
        time.sleep(0.8)  # let Flask bind before opening the browser
        if not os.environ.get("LABEL_PRINTER_RESTART"):
            webbrowser.open("http://localhost:5000")
        _run_tray()      # blocks here until the user clicks Quit

    except ImportError:
        # pystray not installed — fall back to normal terminal mode
        print(f"Label Printer UI → http://localhost:5000")
        print(f"Polling {runtime['relay_url']} every {POLL_SECS}s")
        if _TG_TOKEN:
            print(f"Telegram notifications → chat {_TG_CHAT}")
        app.run(host="0.0.0.0", port=5000, debug=False)
