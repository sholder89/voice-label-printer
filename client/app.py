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
    print_label, list_printers, render_label,
    LABEL_SIZES, FONT_STYLES, FONT_WEIGHTS, BORDER_STYLES, TEXT_CASES,
    STYLE_PRESETS, STYLE_PRESET_GROUPS, WIN32_AVAILABLE,
    _IMAGE_BORDER_ENTRIES,
)

app = Flask(__name__)

# ── Config ───────────────────────────────────────────────────────────────────
RELAY_URL    = os.environ.get("RELAY_URL", "https://yourserver.com")
TOKEN        = os.environ.get("LABEL_TOKEN", "changeme")
POLL_SECS    = int(os.environ.get("POLL_SECS", "3"))
SHOUTRRR_URL = os.environ.get("SHOUTRRR_URL", "")

# Parse Telegram credentials from Shoutrrr URL:
# telegram://<bot_token>@telegram?chats=<chat_id>
_TG_TOKEN = _TG_CHAT = None
_m = re.match(r"telegram://([^@]+)@telegram\?chats=(\d+)", SHOUTRRR_URL)
if _m:
    _TG_TOKEN, _TG_CHAT = _m.group(1), _m.group(2)

# Keys persisted to / loaded from settings.json
_SETTINGS_KEYS = ("printer", "size", "font_style", "font_weight", "border", "text_case", "icons", "style_preset", "qr_show_text", "default_style")
_APP_DIR       = os.path.dirname(os.path.abspath(__file__))

# Store data in %APPDATA%\LabelPrinter — avoids OneDrive sync interference
_DATA_DIR      = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "LabelPrinter")
os.makedirs(_DATA_DIR, exist_ok=True)
_SETTINGS_PATH   = os.path.join(_DATA_DIR, "settings.json")
_HISTORY_PATH    = os.path.join(_DATA_DIR, "history.json")
_ADDRESSES_PATH  = os.path.join(_DATA_DIR, "addresses.json")
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
    """Fire-and-forget Telegram message. Silently skipped if not configured."""
    if not (_TG_TOKEN and _TG_CHAT):
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

@app.route("/")
def index():
    return render_template(
        "index.html",
        printers=list_printers(),
        sizes=list(LABEL_SIZES.keys()),
        font_styles=FONT_STYLES,
        font_weights=FONT_WEIGHTS,
        border_styles=BORDER_STYLES,
        image_border_entries=_IMAGE_BORDER_ENTRIES,
        text_cases=TEXT_CASES,
        style_presets=STYLE_PRESETS,
        style_preset_groups=STYLE_PRESET_GROUPS,
        state=state,
    )


@app.route("/config", methods=["POST"])
def set_config():
    data = request.get_json(silent=True) or {}
    for key in ("printer", "size", "font_style", "font_weight", "border", "text_case", "style_preset"):
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
    style_preset = request.args.get("style_preset", state["style_preset"])
    icons        = request.args.get("icons", str(state["icons"])).lower() not in ("false", "0")
    qr_show_text = request.args.get("qr_show_text", str(state["qr_show_text"])).lower() not in ("false", "0")
    if size not in LABEL_SIZES:
        size = "2x1"
    w, h = LABEL_SIZES[size]
    img  = render_label(text, w, h, dpi=203, font_style=font_style, border=border,
                        icons=icons, text_case=text_case, style_preset=style_preset,
                        font_weight=font_weight, qr_show_text=qr_show_text)
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
                        qr_show_text=qr_show_text)
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
    allowed = {"style_preset", "font_style", "font_weight", "border", "text_case", "icons"}
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
        "style_preset": state["style_preset"],
        "icons":        state["icons"],
        "qr_show_text": state["qr_show_text"],
        "polling":    state["polling"],
        "relay":      RELAY_URL,
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
    params = {"token": TOKEN}
    while state["polling"]:
        try:
            # ── Settings changes ──────────────────────────────────────────
            rs = requests.get(f"{RELAY_URL}/settings/pending", params=params, timeout=10)
            if rs.ok:
                for change in rs.json():
                    key, value, cid = change["key"], change["value"], change["id"]
                    if key in ("font_style", "font_weight", "border", "text_case", "style_preset", "size"):
                        state[key] = value
                        _save_settings()
                    elif key == "icons":
                        state["icons"] = (value == "true")
                        _save_settings()
                    requests.post(f"{RELAY_URL}/settings/{cid}/complete",
                                  params=params, timeout=5)
        except Exception:
            pass

        try:
            # ── Print jobs ────────────────────────────────────────────────
            r = requests.get(f"{RELAY_URL}/jobs/pending", params=params, timeout=10)
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
                            border=state["border"],
                            icons=state["icons"],
                            text_case=state["text_case"],
                            style_preset=state["style_preset"],
                        )
                        requests.post(f"{RELAY_URL}/jobs/{job_id}/complete",
                                      params=params, timeout=5)
                        _record(text, state["size"], "ok (voice)",
                                font_style=state["font_style"], border=state["border"],
                                text_case=state["text_case"], style_preset=state["style_preset"],
                                icons=state["icons"])
                        threading.Thread(
                            target=_notify,
                            args=(text, state["size"], "voice"),
                            daemon=True,
                        ).start()
                    except Exception as e:
                        requests.post(f"{RELAY_URL}/jobs/{job_id}/fail",
                                      params=params, timeout=5)
                        _record(text, state["size"], f"error: {e}",
                                font_style=state["font_style"], border=state["border"],
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
    _load_settings()
    _load_history()
    _load_addresses()

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
        print(f"Polling {RELAY_URL} every {POLL_SECS}s")
        if _TG_TOKEN:
            print(f"Telegram notifications → chat {_TG_CHAT}")
        app.run(host="0.0.0.0", port=5000, debug=False)
