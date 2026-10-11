"""MCP endpoint so local AI assistants can preview and print labels.

Serves MCP Streamable HTTP at http://<this-pc>:5002/mcp, on its own port beside
the Flask UI. Stateless, plain-JSON responses, LAN only.

Tools go through the Flask API over loopback rather than calling into app.py:
the handlers lean on Flask's request context and the shared `state`, and going
through HTTP keeps validation, history and Telegram notifications identical to
a print from the web UI. The only things read in-process are constants from
printer.py, which app.py doesn't serve (the preset list, the full size list).

    MCP_ENABLED          default true; false skips starting the server
    MCP_PORT             default 5002
    MCP_TOKEN            optional; when set, require "Authorization: Bearer <token>"
    MCP_ALLOWED_ORIGINS  comma-separated browser Origins to accept; default none
"""
import base64
import hmac
import ipaddress
import json
import os
import socket
import threading
from typing import Annotated, Literal

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult, ImageContent, TextContent, ToolAnnotations
from pydantic import Field

from printer import (
    LABEL_SIZES, SIZE_LABELS, HIDDEN_SIZES, FONT_STYLES, FONT_WEIGHTS, BORDER_STYLES,
    TEXT_CASES, TEXT_ALIGNS, STYLE_PRESETS, STYLE_PRESET_GROUPS,
    is_round, is_brother_tape,
)

SLUG    = "voice-label-printer"
VERSION = "1.0.0"
MAX_BODY = 1024 * 1024
MAX_COPIES = 5           # /print allows 10; an assistant doesn't need that many

INSTRUCTIONS = (
    "Voice Label Printer prints thermal labels from text. Text auto-matches an "
    "emoji icon; style presets change the look (QR code, barcode, address, price "
    "tag…). Always call label_preview and show the result before label_print "
    "unless the user already approved the exact text and style. Use "
    "label_list_printers / label_list_sizes for valid values."
)

# Presets whose text has to be shaped a particular way. Everything else just
# lays out whatever text it's given.
_PRESET_TEXT_NOTES = {
    "address":  "One address line per line of text, separated by \\n. "
                "label_list_addresses has saved ones.",
    "qr_code":  "Encodes the text as a QR code. Pass a caption to print "
                "something other than the encoded value beside it.",
    "barcode":  "Encodes the text as Code 128, so ASCII only. A caption replaces "
                "the printed human-readable line. Best on 4x2 or wider.",
    "name_tag": "Prints 'HELLO my name is' above the text; give just the name.",
}


def _env_bool(name, default=True):
    val = os.environ.get(name)
    if val is None or not val.strip():
        return default
    return val.strip().lower() not in ("0", "false", "no", "off")


def _env_list(name):
    return [v.strip() for v in os.environ.get(name, "").split(",") if v.strip()]


MCP_ENABLED = _env_bool("MCP_ENABLED", True)
MCP_PORT    = int(os.environ.get("MCP_PORT") or 5002)


# ── Talking to the Flask app ─────────────────────────────────────────────────

class _Api:
    """Loopback client for the Flask UI. The base URL is set at startup because
    the UI may have fallen back off port 5000."""

    def __init__(self):
        self.base = "http://127.0.0.1:5000"

    async def call(self, method, path, *, query=None, body=None):
        """Return (status, parsed JSON or raw bytes)."""
        async with httpx.AsyncClient(base_url=self.base, timeout=60) as client:
            r = await client.request(method, path, params=query, json=body)
        if r.headers.get("content-type", "").startswith("application/json"):
            return r.status_code, r.json()
        return r.status_code, r.content


api = _Api()


def _ok(data):
    return CallToolResult(content=[TextContent(type="text", text=json.dumps(data, ensure_ascii=False))],
                          structuredContent=data)


def _err(message):
    return CallToolResult(content=[TextContent(type="text", text=str(message))], isError=True)


def _error_text(status, data):
    if isinstance(data, dict):
        msg = data.get("error") or data.get("detail")
        if msg:
            return str(msg)
    return f"label printer returned HTTP {status}"


def _page(items, limit):
    return {"total": len(items), "items": items[:limit]}


def _known_size(size):
    return size in LABEL_SIZES


def _size_hint(size):
    return f"unknown size {size!r}; call label_list_sizes for valid keys"


# ── Input types ──────────────────────────────────────────────────────────────

Limit = Annotated[int, Field(ge=1, le=200, description="Maximum items to return (1–200).")]

Text = Annotated[str, Field(min_length=1, max_length=2000, description=(
    "Label text. Use \\n for line breaks. For the address preset, one address "
    "line per line."))]
Size = Annotated[str | None, Field(description=(
    "Size key from label_list_sizes, e.g. '2x1' (inches) or '50mm-round'. "
    "Omit to use the current size."))]
StylePreset = Annotated[Literal[tuple(STYLE_PRESETS)] | None, Field(description=(
    "Style preset key from label_list_style_presets. 'none' uses the individual "
    "font/border settings. Omit to use the current preset."))]
FontStyle = Annotated[Literal[tuple(FONT_STYLES)] | None, Field(
    description="Typeface. Omit to use the current setting.")]
FontWeight = Annotated[Literal[tuple(FONT_WEIGHTS)] | None, Field(
    description="Font weight. Omit to use the current setting.")]
Border = Annotated[Literal[tuple(BORDER_STYLES)] | None, Field(
    description="Border around the label. Omit to use the current setting.")]
TextCase = Annotated[Literal[tuple(TEXT_CASES)] | None, Field(
    description="Case transform applied to the text. Omit to use the current setting.")]
TextAlign = Annotated[Literal[tuple(TEXT_ALIGNS)] | None, Field(
    description="Horizontal alignment. Omit to use the current setting.")]
Icons = Annotated[bool | None, Field(description=(
    "Add an emoji icon matched from the text. Omit to use the current setting."))]
QrShowText = Annotated[bool | None, Field(description=(
    "QR code and barcode presets: print the human-readable text as well. "
    "Omit to use the current setting."))]


def _style_args(**kw):
    """Drop unset options so Flask falls back to the saved settings."""
    return {k: v for k, v in kw.items() if v is not None}


# ── Server ───────────────────────────────────────────────────────────────────

def _allowed_hosts():
    """Host headers to accept: loopback, this PC's names, and its current IPs.

    A DNS-rebinding page reaches us under its own domain name, so it's the
    names that matter. IPs are re-read on demand (see _guard) because DHCP can
    move this PC while the app runs.
    """
    hosts = {"127.0.0.1", "localhost", "[::1]"} | _local_ips()
    for name in {socket.gethostname(), socket.getfqdn()}:
        if name:
            hosts.update({name, name.lower(), f"{name.lower()}.local"})
    return sorted(f"{h}:*" for h in hosts)


def _local_ips():
    ips = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None):
            addr = info[4][0]
            ips.add(f"[{addr}]" if ":" in addr else addr)
    except OSError:
        pass
    return ips


def build_server(port=MCP_PORT, allowed_origins=None):
    origins = _env_list("MCP_ALLOWED_ORIGINS") if allowed_origins is None else allowed_origins
    mcp = FastMCP(
        SLUG,
        instructions=INSTRUCTIONS,
        stateless_http=True,
        json_response=True,
        host="0.0.0.0",
        port=port,
        max_request_body_size=MAX_BODY,
        log_level="WARNING",          # pythonw has no console to log to
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=_allowed_hosts(),
            allowed_origins=origins,
        ),
    )
    mcp._mcp_server.version = VERSION

    read  = ToolAnnotations(readOnlyHint=True, openWorldHint=False)

    # ── Reads ────────────────────────────────────────────────────────────────

    @mcp.tool(name="label_status", title="Printer status", annotations=read)
    async def label_status() -> CallToolResult:
        """Current printer, label size and style settings, the saved default
        style, and whether the relay (Alexa/Siri voice jobs) is being polled.
        These are the values preview and print use for any option you omit."""
        status, data = await api.call("GET", "/status")
        if status >= 400:
            return _err(_error_text(status, data))
        data.pop("telegram", None)
        dstatus, default = await api.call("GET", "/style/default")
        data["default_style"] = default if dstatus == 200 else None
        return _ok(data)

    @mcp.tool(name="label_list_printers", title="List printers", annotations=read)
    async def label_list_printers(limit: Limit = 50) -> CallToolResult:
        """Windows printers this PC can print to. `name` is what label_print's
        `printer` takes; `nickname` is the friendly name shown in the UI;
        `visible` is false for printers hidden in the UI (still printable);
        `current` marks the printer used when none is given. Returns {total, items}."""
        status, data = await api.call("GET", "/config/printers")
        if status >= 400:
            return _err(_error_text(status, data))
        _, st = await api.call("GET", "/status")
        current = st.get("printer") if isinstance(st, dict) else None
        items = [{"name": p["name"], "nickname": p.get("nickname", ""),
                  "visible": p.get("visible", True), "current": p["name"] == current}
                 for p in data]
        return _ok(_page(items, limit))

    @mcp.tool(name="label_list_sizes", title="List label sizes", annotations=read)
    async def label_list_sizes(limit: Limit = 50) -> CallToolResult:
        """Label sizes, built-in and user-defined. `key` is what `size` takes
        elsewhere. Dimensions are in inches; for round labels they're the square
        the circle is cut from. `current` marks the size used when none is given.
        Returns {total, items}."""
        _, st = await api.call("GET", "/status")
        current = st.get("size") if isinstance(st, dict) else None
        items = []
        for key, (w, h) in LABEL_SIZES.items():
            if key in HIDDEN_SIZES:
                continue
            kind = "round" if is_round(key) else "tape" if is_brother_tape(key) else "rectangle"
            items.append({"key": key, "label": SIZE_LABELS.get(key, f"{key} in"),
                          "width_in": round(w, 3), "height_in": round(h, 3),
                          "shape": kind, "current": key == current})
        return _ok(_page(items, limit))

    @mcp.tool(name="label_list_style_presets", title="List style presets", annotations=read)
    async def label_list_style_presets(limit: Limit = 50) -> CallToolResult:
        """Style presets that change a label's look. `key` is what `style_preset`
        takes. `sets` lists the font/border options a preset overrides; presets
        with their own layout ignore those options. `text_format` says how to
        shape the text where it matters. Returns {total, items}."""
        group_of = {k: g for g, keys in STYLE_PRESET_GROUPS for k in keys}
        items = []
        for key, preset in STYLE_PRESETS.items():
            label = preset.get("label", key)
            # Strip the decorative glyph the dropdown leads with.
            name = label.split(" ", 1)[1] if " " in label and not label[0].isalnum() else label
            item = {"key": key, "name": name.strip(), "group": group_of.get(key) or "Default"}
            sets = {k: v for k, v in preset.items() if k != "label"}
            if sets:
                item["sets"] = sets
            if key in _PRESET_TEXT_NOTES:
                item["text_format"] = _PRESET_TEXT_NOTES[key]
            items.append(item)
        return _ok(_page(items, limit))

    @mcp.tool(name="label_preview", title="Preview a label",
              annotations=read, structured_output=False)
    async def label_preview(
        text: Text,
        size: Size = None,
        style_preset: StylePreset = None,
        font_style: FontStyle = None,
        font_weight: FontWeight = None,
        border: Border = None,
        text_case: TextCase = None,
        text_align: TextAlign = None,
        icons: Icons = None,
        qr_show_text: QrShowText = None,
    ) -> CallToolResult:
        """Render a label without printing it. Returns a PNG at 203 dpi plus the
        settings used (omitted options come from label_status). Show the image
        to the user before calling label_print with the same arguments."""
        if size is not None and not _known_size(size):
            return _err(_size_hint(size))
        args = _style_args(size=size, style_preset=style_preset, font_style=font_style,
                           font_weight=font_weight, border=border, text_case=text_case,
                           text_align=text_align, icons=icons, qr_show_text=qr_show_text)
        query = {"text": text, **{k: (str(v).lower() if isinstance(v, bool) else v)
                                  for k, v in args.items()}}
        status, png = await api.call("GET", "/preview", query=query)
        if status >= 400 or not isinstance(png, bytes):
            return _err(_error_text(status, png))

        _, st = await api.call("GET", "/status")
        used = {k: st.get(k) for k in ("size", "style_preset", "font_style", "font_weight",
                                       "border", "text_case", "text_align", "icons",
                                       "qr_show_text")} if isinstance(st, dict) else {}
        used.update(args)
        used["text"] = text
        return CallToolResult(
            content=[ImageContent(type="image", data=base64.b64encode(png).decode("ascii"),
                                  mimeType="image/png"),
                     TextContent(type="text", text=json.dumps(used, ensure_ascii=False))],
            structuredContent=used,
        )

    @mcp.tool(name="label_history", title="Print history", annotations=read)
    async def label_history(limit: Limit = 50) -> CallToolResult:
        """Labels printed recently, newest first, from the web UI and voice.
        `status` is "ok", "ok ×N" for copies, "ok (voice)", or "error: …";
        `ts` is local time, YYYY-MM-DD HH:MM:SS. Returns {total, items}."""
        status, data = await api.call("GET", "/history")
        if status >= 400:
            return _err(_error_text(status, data))
        items = [{k: v for k, v in h.items() if k != "label_color"} for h in data]
        return _ok(_page(items, limit))

    @mcp.tool(name="label_list_addresses", title="List saved addresses", annotations=read)
    async def label_list_addresses(limit: Limit = 50) -> CallToolResult:
        """Addresses saved for the address preset. To print one, join name,
        line1, line2 and csz (city/state/zip) with \\n, skipping blanks, and
        use style_preset "address". Returns {total, items}."""
        status, data = await api.call("GET", "/addresses")
        if status >= 400:
            return _err(_error_text(status, data))
        return _ok(_page(data, limit))

    # ── Safe writes ──────────────────────────────────────────────────────────

    @mcp.tool(name="label_print", title="Print a label", annotations=ToolAnnotations(
        readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=True))
    async def label_print(
        text: Text,
        printer: Annotated[str | None, Field(description=(
            "Printer `name` from label_list_printers. Omit to use the current printer."))] = None,
        size: Size = None,
        style_preset: StylePreset = None,
        font_style: FontStyle = None,
        font_weight: FontWeight = None,
        border: Border = None,
        text_case: TextCase = None,
        text_align: TextAlign = None,
        icons: Icons = None,
        qr_show_text: QrShowText = None,
        caption: Annotated[str | None, Field(max_length=500, description=(
            "QR code and barcode presets only: text printed instead of the encoded "
            "value, e.g. a name for a URL. Ignored by other presets. "
            "Not shown by label_preview."))] = None,
        copies: Annotated[int, Field(ge=1, le=MAX_COPIES, description=(
            f"Number of labels to print, 1–{MAX_COPIES}."))] = 1,
    ) -> CallToolResult:
        """Print a label on a physical printer. Call label_preview with the same
        arguments first and show it to the user, unless they already approved
        this exact text and style. Each call prints again; it doesn't change any
        saved settings. Recorded in label_history."""
        if size is not None and not _known_size(size):
            return _err(_size_hint(size))
        body = {"text": text, "copies": copies,
                **_style_args(printer=printer, size=size, style_preset=style_preset,
                              font_style=font_style, font_weight=font_weight, border=border,
                              text_case=text_case, text_align=text_align, icons=icons,
                              qr_show_text=qr_show_text, caption=caption)}
        status, data = await api.call("POST", "/print", body=body)
        if status >= 400 or not (isinstance(data, dict) and data.get("ok")):
            return _err(_error_text(status, data))
        return _ok({"ok": True, "text": text, "copies": copies,
                    **{k: v for k, v in body.items() if k not in ("text", "copies")}})

    @mcp.tool(name="label_save_address", title="Save an address", annotations=ToolAnnotations(
        readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=False))
    async def label_save_address(
        label: Annotated[str, Field(min_length=1, max_length=100, description=(
            "Short name to pick it by, e.g. 'Mom' or 'Office'."))],
        name: Annotated[str, Field(max_length=200, description="Recipient name.")] = "",
        line1: Annotated[str, Field(max_length=200, description="Street address.")] = "",
        line2: Annotated[str, Field(max_length=200, description=(
            "Apartment, suite or second street line."))] = "",
        csz: Annotated[str, Field(max_length=200, description=(
            "City, state and ZIP on one line."))] = "",
    ) -> CallToolResult:
        """Save an address for the address preset. Always adds a new entry, so
        check label_list_addresses first to avoid duplicates. Returns its id."""
        status, data = await api.call("POST", "/addresses", body={
            "label": label, "name": name, "line1": line1, "line2": line2, "csz": csz})
        if status >= 400 or not (isinstance(data, dict) and data.get("ok")):
            return _err(_error_text(status, data))
        return _ok({"ok": True, "id": data["id"], "label": label})

    return mcp


# ── HTTP wrapper ─────────────────────────────────────────────────────────────

def _is_ip_host(host):
    """True when a Host header names an IP literal rather than a domain."""
    name = host.rsplit(":", 1)[0] if host.count(":") == 1 or host.startswith("[") else host
    try:
        ipaddress.ip_address(name.strip("[]"))
        return True
    except ValueError:
        return False


def _guard(inner, token, security):
    """ASGI wrapper for what the SDK doesn't do itself: 405 for GET/DELETE and
    the optional bearer token. Origin and Host checks are the SDK's (403/421).

    If this PC's DHCP lease moves it to a new IP, the SDK would start refusing
    that Host with 421, so re-read the local IPs when an unknown IP turns up.
    """
    expected = f"Bearer {token}".encode() if token else None

    def refresh_hosts(host):
        known = set(security.allowed_hosts)
        if f"{host.rsplit(':', 1)[0]}:*" in known or not _is_ip_host(host):
            return
        for h in _allowed_hosts():
            if h not in known:
                security.allowed_hosts.append(h)

    async def respond(send, status, body, headers=()):
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"text/plain; charset=utf-8"), *headers]})
        await send({"type": "http.response.body", "body": body.encode()})

    async def app(scope, receive, send):
        if scope["type"] != "http" or scope["path"].rstrip("/") != "/mcp":
            return await inner(scope, receive, send)
        if scope["method"] != "POST":
            return await respond(send, 405, "Method Not Allowed", [(b"allow", b"POST")])
        refresh_hosts(dict(scope["headers"]).get(b"host", b"").decode("latin-1"))
        if expected is not None:
            got = dict(scope["headers"]).get(b"authorization", b"")
            if not hmac.compare_digest(got, expected):
                return await respond(send, 401, "Unauthorized",
                                     [(b"www-authenticate", b"Bearer")])
        return await inner(scope, receive, send)

    return app


def start(ui_port, *, port=None, token=None, allowed_origins=None, log=None):
    """Start the MCP server in a daemon thread. Returns the thread, or None if
    disabled or the port can't be bound (the reason goes to `log`)."""
    import uvicorn
    if not MCP_ENABLED:
        return None
    port  = MCP_PORT if port is None else port
    token = os.environ.get("MCP_TOKEN", "").strip() if token is None else token
    api.base = f"http://127.0.0.1:{ui_port}"

    # Probe first, like the UI does: uvicorn exits its thread on a bind error
    # and pythonw has nowhere to print why.
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind(("0.0.0.0", port))
    except OSError as e:
        if log:
            log(f"MCP port {port} unavailable: {e}")
        return None
    finally:
        probe.close()

    mcp = build_server(port, allowed_origins)
    app = _guard(mcp.streamable_http_app(), token, mcp.settings.transport_security)
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_config=None,
                            log_level="warning", access_log=False, lifespan="on")
    server = uvicorn.Server(config)

    def run():
        try:
            server.run()
        except BaseException as e:      # SystemExit included: uvicorn's bind failure
            if log:
                log(f"MCP server stopped: {e!r}")

    thread = threading.Thread(target=run, name="mcp-server", daemon=True)
    thread.server = server
    thread.start()
    return thread
