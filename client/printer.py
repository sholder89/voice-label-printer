"""Label rendering and printing via Windows GDI."""
import ctypes
import glob
import math
import os
import re
import struct
import threading
from PIL import Image, ImageChops, ImageDraw, ImageFont

# Per-user font directory (works regardless of Windows username)
_USER_FONTS = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~") + r"\AppData\Local"),
    "Microsoft", "Windows", "Fonts",
)

try:
    import win32print
    import win32ui
    from PIL import ImageWin
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# ── Label sizes ───────────────────────────────────────────────────────────────

LABEL_SIZES = {
    "2x1":    (2.0,   1.0),
    "4x2":    (4.0,   2.0),
    "4x6":    (4.0,   6.0),
    "3x2":    (3.0,   2.0),
    "2x0.5":  (2.0,   0.5),
    # Brother QL 29 mm continuous tape (DK-22210 / RL-B-D22210)
    "1.1x3.5": (1.142, 3.543),   # 29 mm × 90 mm — address label
    "1.1x2.4": (1.142, 2.441),   # 29 mm × 62 mm — short label
}

# Brother QL prints on continuous tape that feeds skinny-side-first.  The
# natural reading orientation for these labels is LANDSCAPE (text along the long
# axis), so we RENDER them wide — both in the web preview and for printing — and
# then rotate 90° at print time to lay the design onto the physically-narrow
# tape.  This keeps the preview and the printed output looking identical.
_BROTHER_TAPE_SIZES = {"1.1x3.5", "1.1x2.4"}

# Rotation applied to the landscape render to map it onto the tape at print time.
# -90 = 90° clockwise.  If a printed label comes out upside-down, flip to 90.
_BROTHER_ROTATE = -90


def is_brother_tape(size_key: str) -> bool:
    return size_key in _BROTHER_TAPE_SIZES


def render_dimensions(size_key: str) -> tuple:
    """(width_in, height_in) to RENDER at — swapped to landscape for Brother tape
    so text reads along the long axis.  Used by the preview so what you see on
    screen matches what prints."""
    w, h = LABEL_SIZES[size_key]
    return (h, w) if is_brother_tape(size_key) else (w, h)


# Built-in size keys, captured before any custom sizes are merged in, so custom
# (user-defined) sizes can be cleanly distinguished and replaced.
_BUILTIN_SIZE_KEYS = set(LABEL_SIZES)


def set_custom_sizes(sizes):
    """Merge user-defined sizes into LABEL_SIZES (in place, so all references see
    them). `sizes` is {name: (width_in, height_in)}. Previously-registered custom
    sizes are removed first, so this fully replaces the custom set."""
    for key in [k for k in LABEL_SIZES if k not in _BUILTIN_SIZE_KEYS]:
        del LABEL_SIZES[key]
    for name, (w_in, h_in) in (sizes or {}).items():
        if name and name not in _BUILTIN_SIZE_KEYS:
            LABEL_SIZES[name] = (float(w_in), float(h_in))


DEFAULT_DPI = 203

# Emoji print darkness (0 = no change, 100 = maximum darkening). Applied in
# _draw_icon after resize. Controlled from the Advanced Settings page.
#
# Stored per-thread: the value is set per render based on the target printer,
# and Flask serves requests on multiple threads, so a shared global would let a
# concurrent /preview and /print stomp on each other's darkness mid-render.
_emoji_darkness_tls = threading.local()
_emoji_outline_tls  = threading.local()


def set_emoji_darkness(pct: int):
    _emoji_darkness_tls.value = max(0, min(100, int(pct)))


def _emoji_darkness() -> int:
    return getattr(_emoji_darkness_tls, "value", 0)


def set_emoji_outline(px: int):
    """Set outline thickness in pixels (0 = off, 1–5 = on)."""
    _emoji_outline_tls.value = max(0, min(5, int(px)))


def _emoji_outline() -> int:
    return getattr(_emoji_outline_tls, "value", 0)

# ── Style constants ───────────────────────────────────────────────────────────

FONT_STYLES   = ["standard", "enhanced", "impact", "serif", "narrow", "mono",
                 "consolas", "bahnschrift", "burbank", "inkfree"]
FONT_WEIGHTS  = ["normal", "bold", "italic", "bold_italic"]
# ── Image-based borders ───────────────────────────────────────────────────────
# Any file named  client/images/border_<name>.png  is auto-detected and added
# as a border option.  Drop a new file in and restart the app.

_IMAGES_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(_IMAGES_DIR, exist_ok=True)

def _scan_image_borders():
    """Return list of (key, label) tuples for every border_*.png/webp/jpg in images/."""
    results = []
    seen = set()
    for ext in (".png", ".webp", ".jpg", ".jpeg"):
        for f in sorted(glob.glob(os.path.join(_IMAGES_DIR, f"border_*{ext}"))):
            stem  = os.path.splitext(os.path.basename(f))[0]   # e.g. "border_ornate"
            key   = stem[len("border_"):]                       # e.g. "ornate"
            if key in seen:
                continue
            seen.add(key)
            # Build a human-readable label: replace hyphens/underscores, title-case
            label = key.replace("-", " ").replace("_", " ").title()
            results.append((key, label))
    return results

_IMAGE_BORDER_ENTRIES = _scan_image_borders()          # [(key, label), ...]
_IMAGE_BORDERS        = [k for k, _ in _IMAGE_BORDER_ENTRIES]

BORDER_STYLES = ["none", "thin", "thick", "double", "dashed", "dotted", "wave",
                 "ticket", "inset", "rounded", "corners"] + _IMAGE_BORDERS
TEXT_CASES    = ["none", "uppercase", "lowercase", "title", "sentence"]

# Style presets — each overrides individual settings when active.
# "windows95" uses a fully custom renderer; others map to existing options.
STYLE_PRESETS = {
    # ── Default ───────────────────────────────────────────────────────────────
    "none":       {"label": "— None (use current settings)"},

    # ── Typography ────────────────────────────────────────────────────────────
    "minimal":    {"label": "○ Minimal",          "font_style": "enhanced", "border": "thin"},
    "bold":       {"label": "◼ Bold",              "font_style": "impact",   "border": "thick"},
    "elegant":    {"label": "✒ Elegant",            "font_style": "serif",    "border": "double"},
    "retro":      {"label": "⌨ Retro Typewriter",  "font_style": "mono",     "border": "dashed"},

    # ── Layouts ───────────────────────────────────────────────────────────────
    "address":    {"label": "📬 Address Label"},
    "price_tag":  {"label": "🏷 Price Tag"},
    "cassette":   {"label": "📼 Cassette"},
    "qr_code":    {"label": "⬛ QR Code"},
    "barcode":    {"label": "▌▏ Barcode"},
    "name_tag":   {"label": "👋 Name Tag"},
    "receipt":    {"label": "🧾 Receipt"},

    # ── Themed ────────────────────────────────────────────────────────────────
    "windows95":  {"label": "🖥 Windows 95"},
    "blueprint":  {"label": "📐 Blueprint"},
    "warning":    {"label": "⚠ Warning"},
    "chalkboard": {"label": "🖍 Chalkboard"},
}

# Ordered groups for the UI dropdown — (group_label, [preset_keys])
# Use None as group_label to render ungrouped (no <optgroup> wrapper)
STYLE_PRESET_GROUPS = [
    (None,         ["none"]),
    ("Typography", ["minimal", "bold", "elegant", "retro"]),
    ("Layouts",    ["address", "price_tag", "cassette", "qr_code", "barcode", "name_tag", "receipt"]),
    ("Themed",     ["windows95", "blueprint", "warning", "chalkboard"]),
]

# Fonts for the Windows 95 style (regular weight, not bold)
_WIN95_FONTS = [
    os.path.join(_USER_FONTS, "W95F.otf"),  # W95FA pixel font
    r"C:\Windows\Fonts\micross.ttf",  # Microsoft Sans Serif (fallback)
    r"C:\Windows\Fonts\arial.ttf",    # Arial (fallback)
]

# Fonts for the Warning style (bold/impact preferred)
_WARNING_FONTS = [
    r"C:\Windows\Fonts\impact.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]

_FILL = {
    "standard":   0.85,
    "enhanced":   0.90,
    "impact":     0.92,
    "serif":      0.85,
    "narrow":     0.92,
    "mono":       0.85,
    "consolas":   0.88,
    "bahnschrift":0.92,
    "burbank":    0.95,
    "inkfree":    0.85,
}

_BURBANK_PATH = os.path.join(_USER_FONTS, "BurbankBigCondensed-Bold.otf")
_W95FA_PATH   = os.path.join(_USER_FONTS, "W95F.otf")

# Nested: font_style → font_weight → [path candidates, in preference order]
# Fonts with only one variant (Impact, Burbank, W95FA) repeat the same path for all weights.
_FONT_MAP = {
    "standard": {
        "normal":      [r"C:\Windows\Fonts\arial.ttf"],
        "bold":        [r"C:\Windows\Fonts\arialbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\ariali.ttf",    r"C:\Windows\Fonts\arial.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\arialbi.ttf",   r"C:\Windows\Fonts\arialbd.ttf"],
    },
    "enhanced": {
        "normal":      [r"C:\Windows\Fonts\segoeui.ttf",   r"C:\Windows\Fonts\arial.ttf"],
        "bold":        [r"C:\Windows\Fonts\segoeuib.ttf",  r"C:\Windows\Fonts\arialbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\segoeuii.ttf",  r"C:\Windows\Fonts\ariali.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\segoeuiz.ttf",  r"C:\Windows\Fonts\arialbi.ttf"],
    },
    "impact": {
        "normal":      [r"C:\Windows\Fonts\impact.ttf",    r"C:\Windows\Fonts\arialbd.ttf"],
        "bold":        [r"C:\Windows\Fonts\impact.ttf",    r"C:\Windows\Fonts\arialbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\impact.ttf",    r"C:\Windows\Fonts\ariali.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\impact.ttf",    r"C:\Windows\Fonts\arialbi.ttf"],
    },
    "serif": {
        "normal":      [r"C:\Windows\Fonts\georgia.ttf",   r"C:\Windows\Fonts\times.ttf"],
        "bold":        [r"C:\Windows\Fonts\georgiab.ttf",  r"C:\Windows\Fonts\timesbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\georgiai.ttf",  r"C:\Windows\Fonts\timesi.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\georgiabi.ttf", r"C:\Windows\Fonts\timesbi.ttf"],
    },
    "narrow": {
        "normal":      [r"C:\Windows\Fonts\arialn.ttf",    r"C:\Windows\Fonts\arial.ttf"],
        "bold":        [r"C:\Windows\Fonts\ARIALNB.TTF",   r"C:\Windows\Fonts\arialbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\arialNI.TTF",   r"C:\Windows\Fonts\ariali.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\arialNBI.TTF",  r"C:\Windows\Fonts\arialbi.ttf"],
    },
    "mono": {
        "normal":      [r"C:\Windows\Fonts\cour.ttf"],
        "bold":        [r"C:\Windows\Fonts\courbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\couri.ttf",     r"C:\Windows\Fonts\cour.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\courbi.ttf",    r"C:\Windows\Fonts\courbd.ttf"],
    },
    "consolas": {
        "normal":      [r"C:\Windows\Fonts\consola.ttf"],
        "bold":        [r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\consola.ttf"],
        "italic":      [r"C:\Windows\Fonts\consolai.ttf", r"C:\Windows\Fonts\consola.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\consolaz.ttf", r"C:\Windows\Fonts\consolab.ttf"],
    },
    # Bahnschrift is a single variable-font file (no static bold/italic faces),
    # so every weight maps to it; condensed Arial Narrow is the closest fallback.
    "bahnschrift": {
        "normal":      [r"C:\Windows\Fonts\bahnschrift.ttf", r"C:\Windows\Fonts\arialn.ttf",   r"C:\Windows\Fonts\arial.ttf"],
        "bold":        [r"C:\Windows\Fonts\bahnschrift.ttf", r"C:\Windows\Fonts\ARIALNB.TTF",  r"C:\Windows\Fonts\arialbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\bahnschrift.ttf", r"C:\Windows\Fonts\arialNI.TTF",  r"C:\Windows\Fonts\ariali.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\bahnschrift.ttf", r"C:\Windows\Fonts\arialNBI.TTF", r"C:\Windows\Fonts\arialbi.ttf"],
    },
    # Ink Free ships as a single handwriting face; fall back to Segoe Script.
    "inkfree": {
        "normal":      [r"C:\Windows\Fonts\Inkfree.ttf", r"C:\Windows\Fonts\segoesc.ttf",  r"C:\Windows\Fonts\arial.ttf"],
        "bold":        [r"C:\Windows\Fonts\Inkfree.ttf", r"C:\Windows\Fonts\segoescb.ttf", r"C:\Windows\Fonts\arialbd.ttf"],
        "italic":      [r"C:\Windows\Fonts\Inkfree.ttf", r"C:\Windows\Fonts\segoesc.ttf",  r"C:\Windows\Fonts\ariali.ttf"],
        "bold_italic": [r"C:\Windows\Fonts\Inkfree.ttf", r"C:\Windows\Fonts\segoescb.ttf", r"C:\Windows\Fonts\arialbi.ttf"],
    },
    "burbank": {
        "normal":      [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
        "bold":        [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
        "italic":      [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
        "bold_italic": [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
    },
}

# ── Icon keyword / emoji data (imported from emoji_data.py) ──────────────────
from emoji_data import _ICON_KEYWORDS, _ICON_EMOJIS   # noqa: E402

# ── DEVMODE constants ─────────────────────────────────────────────────────────

_OFF_FIELDS      = 72
_OFF_PAPERSIZE   = 78
_OFF_PAPERLENGTH = 80
_OFF_PAPERWIDTH  = 82
_DM_PAPERSIZE    = 0x0002
_DM_PAPERLENGTH  = 0x0004
_DM_PAPERWIDTH   = 0x0008
_DMPAPER_USER    = 256
_DM_OUT_BUFFER   = 2

_gdi32    = ctypes.WinDLL("gdi32")
_winspool = ctypes.WinDLL("winspool.drv")

_gdi32.CreateDCW.restype  = ctypes.c_void_p
_gdi32.CreateDCW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p,
                              ctypes.c_wchar_p, ctypes.c_void_p]
_gdi32.DeleteDC.restype   = ctypes.c_bool
_gdi32.DeleteDC.argtypes  = [ctypes.c_void_p]

_winspool.OpenPrinterW.restype  = ctypes.c_bool
_winspool.OpenPrinterW.argtypes = [ctypes.c_wchar_p,
                                   ctypes.POINTER(ctypes.c_void_p),
                                   ctypes.c_void_p]
_winspool.ClosePrinter.restype  = ctypes.c_bool
_winspool.ClosePrinter.argtypes = [ctypes.c_void_p]
_winspool.DocumentPropertiesW.restype  = ctypes.c_long
_winspool.DocumentPropertiesW.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                           ctypes.c_wchar_p, ctypes.c_void_p,
                                           ctypes.c_void_p, ctypes.c_uint32]

# ── Public API ────────────────────────────────────────────────────────────────

def list_printers() -> list[str]:
    if not WIN32_AVAILABLE:
        return []
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )
    return [p[2] for p in printers]


def render_label(
    text: str,
    width_in: float,
    height_in: float,
    dpi: int = DEFAULT_DPI,
    font_style: str = "standard",
    border: str = "none",
    icons: bool = True,
    text_case: str = "none",
    style_preset: str = "none",
    font_weight: str = "bold",
    qr_show_text: bool = True,
    text_align: str = "center",
) -> Image.Image:
    w_px = int(width_in * dpi)
    h_px = int(height_in * dpi)

    # Apply style preset overrides
    if style_preset and style_preset != "none":
        if style_preset == "windows95":
            return _render_win95(text, w_px, h_px, dpi, text_case, icons, font_weight)
        if style_preset == "warning":
            return _render_warning(text, w_px, h_px, dpi, text_case, icons)
        if style_preset == "address":
            return _render_address(text, w_px, h_px, dpi, font_style, border, font_weight)
        if style_preset == "price_tag":
            return _render_price_tag(text, w_px, h_px, dpi, text_case, font_weight)
        if style_preset == "cassette":
            return _render_cassette(text, w_px, h_px, dpi, text_case, font_weight)
        if style_preset == "blueprint":
            return _render_blueprint(text, w_px, h_px, dpi, text_case, icons, font_weight)
        if style_preset == "qr_code":
            return _render_qr_code(text, w_px, h_px, dpi, text_case, font_weight, qr_show_text)
        if style_preset == "barcode":
            return _render_barcode(text, w_px, h_px, dpi, text_case, font_weight, qr_show_text)
        if style_preset == "name_tag":
            return _render_name_tag(text, w_px, h_px, dpi, text_case, font_weight)
        if style_preset == "receipt":
            return _render_receipt(text, w_px, h_px, dpi, text_case, font_weight)
        if style_preset == "chalkboard":
            return _render_chalkboard(text, w_px, h_px, dpi, text_case, icons, font_weight)
        preset = STYLE_PRESETS.get(style_preset, {})
        font_style = preset.get("font_style", font_style)
        border     = preset.get("border",     border)
        text_case  = preset.get("text_case",  text_case)
        icons      = preset.get("icons",      icons)

    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)

    pad  = max(4, int(min(w_px, h_px) * 0.05))

    # Push content inward so it never overlaps the border
    _border_inset = {"thin": 4, "thick": 8, "double": 14, "dashed": 4,
                     "dotted": 4, "wave": 10, "ticket": 12, "inset": 12,
                     "rounded": 6, "corners": 4}
    pad = max(pad, _border_inset.get(border, 0) + 4)
    # Image borders have thick decorative edges — use a generous inset
    if border in _IMAGE_BORDERS:
        pad = max(pad, round(min(w_px, h_px) * 0.18))

    # Suppress icons on long labels — not enough space to look good
    if len(text) > 60:
        icons = False

    # Icon detection uses original text so keywords always match regardless of case setting
    icon = _detect_icon(text) if icons else None

    # Apply case transformation to the display text only
    text = _apply_case(text, text_case)

    if icon:
        if h_px > w_px:
            # Portrait label (e.g. 4x6): stack icon on top, text below — sizing
            # the icon to the WIDTH so it doesn't balloon on a tall label.
            icon_size = int(min(w_px * 0.42, h_px * 0.28))
            icon_x    = (w_px - icon_size) // 2
            icon_y    = pad
            text_x0   = pad
            text_y0   = icon_y + icon_size + pad
        else:
            # Landscape label (e.g. 2x1): icon on the left, text to the right.
            icon_size = int(h_px * 0.55)
            icon_x    = pad
            icon_y    = (h_px - icon_size) // 2
            text_x0   = icon_x + icon_size + pad
            text_y0   = pad
    else:
        text_x0 = pad
        text_y0 = pad

    text_area_w = w_px - text_x0 - pad
    text_area_h = h_px - text_y0 - pad

    fill    = _FILL.get(font_style, 0.85)
    align   = text_align if text_align in ("left", "center", "right") else "center"

    if _has_inline_emoji(text):
        # Literal emoji in the text — render segment-by-segment so they print as
        # (mono) emoji graphics instead of missing-glyph boxes.
        _render_inline_text(img, draw, text, text_x0, text_y0,
                            text_area_w, text_area_h,
                            font_style, fill, font_weight, align)
    else:
        wrapped, font = _fit_text(text, text_area_w, text_area_h, font_style, fill, font_weight)
        joined  = "\n".join(wrapped)
        bb  = draw.multiline_textbbox((0, 0), joined, font=font, align=align)
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        if align == "left":
            x = text_x0
        elif align == "right":
            x = text_x0 + text_area_w - bw
        else:
            x = text_x0 + (text_area_w - bw) / 2 - bb[0]
        y = text_y0 + (text_area_h - bh) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill="black", font=font, align=align)

    if icon:
        _draw_icon(img, icon, icon_x, icon_y, icon_size)

    _draw_border(draw, w_px, h_px, pad, border, dpi)
    if border in _IMAGE_BORDERS:
        img = _overlay_image_border(img, border, w_px, h_px)

    return img


def print_label(
    text: str,
    printer_name: str,
    size_key: str = "2x1",
    dpi: int = DEFAULT_DPI,
    font_style: str = "standard",
    border: str = "none",
    icons: bool = True,
    text_case: str = "none",
    style_preset: str = "none",
    font_weight: str = "bold",
    qr_show_text: bool = True,
    text_align: str = "center",
):
    if not WIN32_AVAILABLE:
        raise RuntimeError("pywin32 is not installed — cannot print")

    # Some printer drivers (especially Bluetooth/USB label printers) require COM
    # to be initialised on the calling thread before winspool/GDI calls work.
    # CoInitializeEx is safe to call multiple times — returns S_FALSE if the
    # thread already has COM, so this is harmless on Flask's request threads too.
    try:
        ctypes.windll.ole32.CoInitializeEx(None, 0)  # COINIT_APARTMENTTHREADED
    except Exception:
        pass

    # Fall back to a safe default if the size was deleted (e.g. a removed custom
    # size that was still selected) rather than crashing the print.
    width_in, height_in = LABEL_SIZES.get(size_key, LABEL_SIZES["2x1"])

    # Create the DC first so we can read the driver's actual physical page
    # dimensions before rendering.  Many drivers ignore DEVMODE paper-size
    # overrides and report their own native dimensions (e.g. a 51×25 mm label
    # reports 408×200 px at 203 DPI, not the nominal 2"×1" = 406×203 px).
    # Rendering at the wrong size causes compression/clipping artefacts.
    #
    # Brother QL drivers auto-detect the installed DK roll — forcing a custom
    # DEVMODE causes the printer to blink red and reject the job.
    _skip_devmode = "brother" in printer_name.lower()
    dm_buf = None if _skip_devmode else _get_devmode_buf(printer_name, width_in, height_in)

    hdc_raw = None
    if dm_buf is not None:
        hdc_raw = _gdi32.CreateDCW("WINSPOOL", printer_name, None, dm_buf)
    if not hdc_raw:
        hdc_raw = _gdi32.CreateDCW("WINSPOOL", printer_name, None, None)
    if not hdc_raw:
        err = ctypes.GetLastError()
        raise RuntimeError(f"CreateDC failed (Windows error {err}) — check printer name and driver")

    hDC = win32ui.CreateDCFromHandle(hdc_raw)

    try:
        off_x = hDC.GetDeviceCaps(112)   # PHYSICALOFFSETX
        off_y = hDC.GetDeviceCaps(113)   # PHYSICALOFFSETY
        dpi_x = hDC.GetDeviceCaps(88)    # LOGPIXELSX
        dpi_y = hDC.GetDeviceCaps(90)    # LOGPIXELSY

        render_dpi = dpi_x or dpi

        # calc_w / calc_h are the physical page dimensions for our label size
        # at the driver's reported DPI, used as the draw-target rect.
        calc_w = int(width_in  * render_dpi)
        calc_h = int(height_in * (dpi_y or dpi))

        if _skip_devmode:
            # Brother QL drivers auto-detect the installed DK roll and bypass
            # DEVMODE.  Different models (and driver versions) present the DC in
            # either portrait (narrow side = X) or landscape (long side = X).
            # Read the physical DC dimensions to tell which we have, then render
            # and orient accordingly so the content always reads along the label.
            dc_phys_w = hDC.GetDeviceCaps(110)   # PHYSICALWIDTH  (device px)
            dc_phys_h = hDC.GetDeviceCaps(111)   # PHYSICALHEIGHT (device px)
            dc_landscape = dc_phys_w >= dc_phys_h

            # Always render landscape (long side as image width, text fills it).
            img = render_label(text, height_in, width_in, dpi,
                               font_style, border, icons, text_case,
                               style_preset, font_weight, qr_show_text,
                               text_align)

            if dc_landscape:
                # DC is already landscape — draw directly, no rotation needed.
                render_w = int(height_in * (dpi_x or dpi))
                render_h = int(width_in  * (dpi_y or dpi))
            else:
                # DC is portrait — rotate landscape image to match.
                img = img.rotate(_BROTHER_ROTATE, expand=True)
                render_w = calc_w
                render_h = calc_h
        else:
            img = render_label(text, width_in, height_in, dpi,
                               font_style, border, icons, text_case,
                               style_preset, font_weight, qr_show_text,
                               text_align)
            render_w = calc_w
            render_h = calc_h

        hDC.StartDoc("Label")
        hDC.StartPage()
        bmp = ImageWin.Dib(img)
        bmp.draw(hDC.GetHandleOutput(),
                 (-off_x, -off_y, render_w - off_x, render_h - off_y))
        hDC.EndPage()
        hDC.EndDoc()
    finally:
        # Always release the device context, even if rendering/printing failed,
        # so GDI handles don't leak across repeated print errors.
        hDC.DeleteDC()

# ── Windows 95 renderer ──────────────────────────────────────────────────────

def _render_win95(text: str, w_px: int, h_px: int, dpi: int, text_case: str,
                  icons: bool = True, font_weight: str = "bold") -> Image.Image:
    """Render a classic Windows 95 raised-button style label."""
    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)

    # Margin between label edge and button edge
    margin = max(8, round(0.09 * min(w_px, h_px)))
    bx1, by1 = margin, margin
    bx2, by2 = w_px - margin - 1, h_px - margin - 1
    bw,  bh  = bx2 - bx1, by2 - by1

    # Gray button face
    draw.rectangle([bx1, by1, bx2, by2], fill="#c0c0c0")

    # Border thickness scaled to DPI
    s = max(2, round(dpi / 64))

    # Outer border: white top/left highlight, dark bottom/right shadow
    draw.line([(bx1,   by1),   (bx2,   by1)  ], fill="#ffffff", width=s)
    draw.line([(bx1,   by1),   (bx1,   by2)  ], fill="#ffffff", width=s)
    draw.line([(bx1,   by2),   (bx2,   by2)  ], fill="#404040", width=s)
    draw.line([(bx2,   by1),   (bx2,   by2)  ], fill="#404040", width=s)

    # Inner border: light gray top/left, medium gray bottom/right
    i = s
    draw.line([(bx1+i, by1+i), (bx2-i, by1+i)], fill="#dfdfdf", width=s)
    draw.line([(bx1+i, by1+i), (bx1+i, by2-i)], fill="#dfdfdf", width=s)
    draw.line([(bx1+i, by2-i), (bx2-i, by2-i)], fill="#808080", width=s)
    draw.line([(bx2-i, by1+i), (bx2-i, by2-i)], fill="#808080", width=s)

    # Content padding inside the button
    pad = s * 2 + i + max(4, int(min(bw, bh) * 0.04))

    # Icon detection (use original text, suppress on long labels)
    icon = _detect_icon(text) if (icons and len(text) <= 60) else None
    if icon:
        icon_size = int(bh * 0.55)
        icon_x    = bx1 + pad
        icon_y    = by1 + (bh - icon_size) // 2
        text_x0   = icon_x + icon_size + pad
    else:
        text_x0   = bx1 + pad

    text_area_w = bx2 - text_x0 - pad
    text_area_h = bh - pad * 2

    display_text = _apply_case(text, text_case)
    font_path    = next((p for p in _WIN95_FONTS if os.path.exists(p)), None)

    if _has_inline_emoji(display_text):
        _render_inline_text(img, draw, display_text, text_x0, by1 + pad,
                            text_area_w, text_area_h, font_path=font_path,
                            fill=0.85, color=(0, 0, 0))
    else:
        words = display_text.split()
        max_n = min(len(words), 5)
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display_text]
        for n in range(1, min(max_n, 5) + 1):
            lines = _split_words(words, n)
            font, size = _largest_font_for("\n".join(lines), text_area_w, text_area_h,
                                           font_path, fill=0.85)
            if size > best_size:
                best_size, best_font, best_lines = size, font, lines

        joined = "\n".join(best_lines)
        stroke = 1 if font_weight in ("bold", "bold_italic") else 0
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center",
                                     stroke_width=stroke)
        x  = text_x0 + (text_area_w - (bb[2] - bb[0])) / 2 - bb[0]
        y  = by1 + (bh - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill="#000000", font=best_font, align="center",
                            stroke_width=stroke, stroke_fill="#000000")

    if icon:
        _draw_icon(img, icon, icon_x, icon_y, icon_size)

    return img


# ── Address renderer ─────────────────────────────────────────────────────────

_ADDR_FONTS = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\calibri.ttf",
]

def _render_address(text: str, w_px: int, h_px: int, dpi: int,
                    font_style: str = "enhanced", border: str = "thin",
                    font_weight: str = "bold") -> Image.Image:
    """Left-aligned address label.  Text arrives pre-formatted with \\n separators
    (one line per address field).  Font style and border honour the user's settings."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    img  = Image.new("RGB", (w_px, h_px), WHITE)
    draw = ImageDraw.Draw(img)

    # Inset text to clear the border (same table used by render_label)
    _border_inset = {"thin": 4, "thick": 8, "double": 14, "dashed": 4,
                     "dotted": 4, "wave": 10, "ticket": 12, "inset": 12,
                     "rounded": 6, "corners": 4}
    inset  = _border_inset.get(border, 0)
    pad_x  = max(10, round(w_px * 0.055)) + inset
    pad_y  = max(6,  round(h_px * 0.07))  + inset
    if border in _IMAGE_BORDERS:
        img_pad = round(min(w_px, h_px) * 0.18)
        pad_x   = max(pad_x, img_pad)
        pad_y   = max(pad_y, img_pad)

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        return img

    avail_w = w_px - pad_x * 2
    avail_h = h_px - pad_y * 2

    # Use the same font map as every other renderer so the user's choice applies
    font_path = _find_font_path(font_style, font_weight)
    if not font_path:
        font_path = next((p for p in _ADDR_FONTS if os.path.exists(p)), None)

    # Find the largest font size where every line fits the width and the
    # whole block fits the height
    best_font = ImageFont.load_default()
    for size in range(8, 300, 2):
        try:
            f = ImageFont.truetype(font_path, size) if font_path else None
            if f is None:
                break
        except OSError:
            break
        bb   = draw.textbbox((0, 0), "Ag", font=f)
        lh   = bb[3] - bb[1]
        gap  = round(lh * 0.28)
        th   = lh * len(lines) + gap * (len(lines) - 1)
        mw   = max(draw.textbbox((0, 0), l, font=f)[2] for l in lines)
        if mw > avail_w * 0.93 or th > avail_h * 0.93:
            break
        best_font = f

    bb  = draw.textbbox((0, 0), "Ag", font=best_font)
    lh  = bb[3] - bb[1]
    gap = round(lh * 0.28)
    th  = lh * len(lines) + gap * (len(lines) - 1)
    y   = pad_y + (avail_h - th) // 2

    for line in lines:
        if _has_inline_emoji(line):
            _render_inline_text(img, draw, line, pad_x, y,
                                avail_w, lh, font_path=font_path,
                                fill=0.95, align="left", color=BLACK)
        else:
            draw.text((pad_x, y), line, fill=BLACK, font=best_font)
        y += lh + gap

    # Draw border using the shared renderer — same pad formula as render_label
    border_pad = max(4, int(min(w_px, h_px) * 0.05))
    _draw_border(draw, w_px, h_px, border_pad, border, dpi)
    if border in _IMAGE_BORDERS:
        img = _overlay_image_border(img, border, w_px, h_px)

    return img


# ── Warning renderer ─────────────────────────────────────────────────────────

def _render_warning(text: str, w_px: int, h_px: int, dpi: int, text_case: str,
                    icons: bool = True) -> Image.Image:
    """Render a hazard-warning label — black & white.

    Layout (top → bottom):
      • Black header — ⚠ emoji on the left, bold "WARNING" text in white
      • White content area — user's label text in black
      • Diagonal black/white hazard stripes at the bottom
    The whole thing is framed with a large-radius rounded border (no visible corners).
    """
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)

    img  = Image.new("RGB", (w_px, h_px), WHITE)
    draw = ImageDraw.Draw(img)

    font_path = next((p for p in _WARNING_FONTS if os.path.exists(p)), None)

    # Same 3 mm corner radius used by all other borders
    r  = max(4, round(3 / 25.4 * dpi))
    bw = max(3, round(dpi / 65))
    m  = bw + 1

    ix1, iy1 = m,           m
    ix2, iy2 = w_px - m - 1, h_px - m - 1
    inner_h  = iy2 - iy1

    # Section heights
    header_h  = round(inner_h * 0.36)
    stripe_h  = round(inner_h * 0.17)
    content_h = inner_h - header_h - stripe_h

    hy2        = iy1 + header_h
    cy1, cy2   = hy2, hy2 + content_h
    sy1, sy2   = cy2, iy2

    # ── Step 1: fill entire shape black (gives header naturally-curved top corners) ──
    draw.rounded_rectangle([0, 0, w_px - 1, h_px - 1], radius=r, fill=BLACK)

    # ── Step 2: punch out the white content + stripe area ────────────────────
    draw.rectangle([ix1, cy1, ix2, iy2], fill=WHITE)

    # ── Step 3: diagonal black stripes in bottom band (/ direction) ──────────
    # Exactly 7 black stripes (7 black + 7 white gaps = 14 units across)
    band_h = sy2 - sy1
    sw     = max(8, round((ix2 - ix1) / 14))
    for x_start in range(ix1 - sw, ix2 + band_h + sw, sw * 2):
        pts = [
            (x_start,               sy1),
            (x_start + sw,          sy1),
            (x_start + sw - band_h, sy2),
            (x_start -      band_h, sy2),
        ]
        draw.polygon(pts, fill=BLACK)

    # ── Step 4: clip everything back to the rounded rect (removes corner bleed) ──
    clip_mask = Image.new("L", (w_px, h_px), 255)
    ImageDraw.Draw(clip_mask).rounded_rectangle(
        [0, 0, w_px - 1, h_px - 1], radius=r, fill=0)
    img.paste(Image.new("RGB", (w_px, h_px), WHITE), mask=clip_mask)
    draw = ImageDraw.Draw(img)   # refresh after paste

    # ── Step 5: header/content divider only (no divider above stripes) ───────
    dw = max(1, bw // 2)
    draw.line([(ix1, hy2), (ix2, hy2)], fill=BLACK, width=dw)

    # ── Step 6: outer border (on top of everything) ───────────────────────────
    draw.rounded_rectangle([0, 0, w_px - 1, h_px - 1], radius=r,
                           outline=BLACK, width=bw)

    # ── Header content ────────────────────────────────────────────────────────
    icon_pad  = max(3, round(header_h * 0.12))
    icon_sz   = header_h - icon_pad * 2
    icon_lx   = ix1 + icon_pad * 2
    icon_ly   = iy1 + icon_pad
    _draw_icon(img, "warning", icon_lx, icon_ly, icon_sz, color=WHITE,
               skip_noto=True, skip_hb=True)

    warn_text   = "WARNING"
    warn_x1     = icon_lx + icon_sz + icon_pad * 2
    warn_area_w = ix2 - warn_x1 - icon_pad
    warn_area_h = header_h - 6
    wfont, _    = _largest_font_for(warn_text, warn_area_w, warn_area_h, font_path, fill=0.68)
    wb  = draw.textbbox((0, 0), warn_text, font=wfont)
    wx  = warn_x1 + (warn_area_w - (wb[2] - wb[0])) / 2 - wb[0]
    wy  = iy1 + (header_h - (wb[3] - wb[1])) / 2 - wb[1]
    draw.text((wx, wy), warn_text, fill=WHITE, font=wfont)

    # ── Body text ─────────────────────────────────────────────────────────────
    pad          = max(4, round(dpi / 60))
    body_h       = cy2 - cy1 - pad * 2
    body_x1      = ix1 + pad
    body_y1      = cy1 + pad
    display_text = _apply_case(text, text_case)
    body_icon    = _detect_icon(text) if (icons and len(text) <= 60) else None

    if body_icon:
        bi_size = int(body_h * 0.72)
        bi_x    = body_x1
        bi_y    = body_y1 + (body_h - bi_size) // 2
        text_x0 = body_x1 + bi_size + pad
    else:
        text_x0 = body_x1

    text_area_w = ix2 - text_x0 - pad
    if _has_inline_emoji(display_text):
        _render_inline_text(img, draw, display_text, text_x0, body_y1,
                            text_area_w, body_h, font_path=font_path,
                            fill=0.85, color=BLACK)
    else:
        words = display_text.split()
        max_n = min(len(words), 5)
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display_text]
        for n in range(1, min(max_n, 5) + 1):
            lines = _split_words(words, n)
            font, size = _largest_font_for("\n".join(lines), text_area_w, body_h,
                                           font_path, fill=0.85)
            if size > best_size:
                best_size, best_font, best_lines = size, font, lines

        joined = "\n".join(best_lines)
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center")
        x  = text_x0 + (text_area_w - (bb[2] - bb[0])) / 2 - bb[0]
        y  = body_y1  + (body_h     - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill=BLACK, font=best_font, align="center")

    if body_icon:
        _draw_icon(img, body_icon, bi_x, bi_y, bi_size)

    return img


# ── Text case transformation ──────────────────────────────────────────────────

def _smart_title(text: str) -> str:
    """Title-case that fixes two problems with str.title():
    - str.title() capitalizes after apostrophes: "what's" → "What'S"  (wrong)
    - str.title() lowercases abbreviations: "USB drive" → "Usb Drive" (wrong)
    This version capitalizes only the very first character of each word and
    leaves ALL-CAPS words (abbreviations) completely untouched.
    """
    def _cap(word: str) -> str:
        if not word:
            return word
        # Leave words that are already all-caps (e.g. USB, FCC, OK) unchanged
        if len(word) > 1 and word.isupper():
            return word
        # Only raise the first character — don't touch the rest
        return word[0].upper() + word[1:].lower()
    return "\n".join(" ".join(_cap(w) for w in line.split()) for line in text.split("\n"))


def _apply_case(text: str, case: str) -> str:
    if case == "uppercase":
        return text.upper()
    if case == "lowercase":
        return text.lower()
    if case == "title":
        return _smart_title(text)
    if case == "sentence":
        # Only capitalize the first character; leave the rest as-is so
        # abbreviations mid-sentence (e.g. "check USB port") are preserved
        return text[0].upper() + text[1:] if text else text
    return text  # "none" — leave as typed

# ── Price Tag renderer ───────────────────────────────────────────────────────

def _render_price_tag(text: str, w_px: int, h_px: int, dpi: int,
                      text_case: str, font_weight: str = "bold") -> Image.Image:
    """Classic retail price-tag style: eyelet hole on the LEFT, text fills the right."""
    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)

    bw = max(3, round(dpi / 65))
    r  = max(10, round(min(w_px, h_px) * 0.14))
    draw.rounded_rectangle([bw//2, bw//2, w_px - bw//2 - 1, h_px - bw//2 - 1],
                            radius=r, outline="black", width=bw)

    # Eyelet column — narrow strip on the left
    eyelet_w = max(round(w_px * 0.14), round(0.22 * dpi))
    hole_r   = max(7, round(min(eyelet_w, h_px) * 0.28))
    hole_cx  = eyelet_w // 2
    hole_cy  = h_px // 2
    draw.ellipse([hole_cx - hole_r, hole_cy - hole_r,
                  hole_cx + hole_r, hole_cy + hole_r],
                 fill="white", outline="black", width=max(2, bw - 1))

    # Vertical divider line between eyelet and text area
    div_x = eyelet_w + max(3, round(w_px * 0.02))
    draw.line([(div_x, bw + r//2), (div_x, h_px - bw - r//2)],
              fill="black", width=max(1, bw // 2))

    # Text area to the right of the divider
    pad         = max(4, round(min(w_px, h_px) * 0.06))
    text_x0     = div_x + pad
    text_area_w = w_px - text_x0 - pad
    text_area_h = h_px - pad * 2

    display_text = _apply_case(text, text_case)
    font_path    = _find_font_path("standard", font_weight)

    if _has_inline_emoji(display_text):
        _render_inline_text(img, draw, display_text, text_x0, pad,
                            text_area_w, text_area_h, font_path=font_path,
                            fill=0.85, color=(0, 0, 0))
    else:
        words = display_text.split()
        max_n = min(len(words), 5)
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display_text]
        for n in range(1, min(max_n, 5) + 1):
            lines = _split_words(words, n)
            font, size = _largest_font_for("\n".join(lines), text_area_w, text_area_h, font_path, 0.85)
            if size > best_size:
                best_size, best_font, best_lines = size, font, lines

        joined = "\n".join(best_lines)
        stroke = 1 if font_weight in ("bold", "bold_italic") else 0
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center", stroke_width=stroke)
        x  = text_x0 + (text_area_w - (bb[2] - bb[0])) / 2 - bb[0]
        y  = (h_px - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill="black", font=best_font, align="center",
                            stroke_width=stroke, stroke_fill="black")
    return img


# ── Cassette Spine renderer ───────────────────────────────────────────────────

def _render_cassette(text: str, w_px: int, h_px: int, dpi: int,
                     text_case: str, font_weight: str = "bold") -> Image.Image:
    """Cassette/VHS spine style: solid black end-blocks, white text area in the centre."""
    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)

    # End blocks — scale with label width but cap at 25 %
    end_w = min(round(w_px * 0.22), round(0.35 * dpi))
    end_w = max(end_w, round(0.15 * dpi))

    draw.rectangle([0, 0, end_w,          h_px - 1], fill="black")
    draw.rectangle([w_px - end_w, 0, w_px - 1, h_px - 1], fill="black")

    # Horizontal white detail lines inside each block — 2px so they print visibly
    detail_lw = max(2, round(dpi / 120))
    for frac in (0.30, 0.55, 0.80):
        y = round(h_px * frac)
        draw.line([(4, y), (end_w - 5, y)],                fill="white", width=detail_lw)
        draw.line([(w_px - end_w + 4, y), (w_px - 5, y)], fill="white", width=detail_lw)

    # Thin vertical divider lines between blocks and text area
    lw = max(1, round(dpi / 150))
    draw.line([(end_w, 0), (end_w, h_px)],            fill="black", width=lw)
    draw.line([(w_px - end_w, 0), (w_px - end_w, h_px)], fill="black", width=lw)

    # Text — narrow/condensed font fits the spine aesthetic
    pad         = max(4, round(h_px * 0.08))
    text_x0     = end_w + pad
    text_area_w = w_px - 2 * (end_w + pad)
    text_area_h = h_px - pad * 2

    display_text = _apply_case(text, text_case)
    font_path    = _find_font_path("narrow", font_weight)

    if _has_inline_emoji(display_text):
        _render_inline_text(img, draw, display_text, text_x0, pad,
                            text_area_w, text_area_h, font_path=font_path,
                            fill=0.90, color=(0, 0, 0))
    else:
        words = display_text.split()
        max_n = min(len(words), 5)
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display_text]
        for n in range(1, min(max_n, 5) + 1):
            lines = _split_words(words, n)
            font, size = _largest_font_for("\n".join(lines), text_area_w, text_area_h, font_path, 0.90)
            if size > best_size:
                best_size, best_font, best_lines = size, font, lines

        joined = "\n".join(best_lines)
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center")
        x  = text_x0 + (text_area_w - (bb[2] - bb[0])) / 2 - bb[0]
        y  = (h_px - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill="black", font=best_font, align="center")

    # Outer border
    draw.rectangle([0, 0, w_px - 1, h_px - 1], outline="black", width=max(2, lw))
    return img


# ── Blueprint renderer ────────────────────────────────────────────────────────

def _render_blueprint(text: str, w_px: int, h_px: int, dpi: int,
                      text_case: str, icons: bool = True,
                      font_weight: str = "bold") -> Image.Image:
    """Engineering blueprint style: black background, white text/grid, corner marks."""
    BG   = (0,   0,   0)    # pure black
    FG   = (255, 255, 255)  # pure white — text, border, corner marks
    GRID = (100, 100, 100)  # mid-grey — visible but doesn't compete with text

    img  = Image.new("RGB", (w_px, h_px), BG)
    draw = ImageDraw.Draw(img)

    # Grid — 3px mid-grey lines: subtle in preview, still visible when printed
    step = max(round(dpi * 0.22), 16)
    for gx in range(step, w_px, step):
        draw.line([(gx, 0), (gx, h_px)], fill=GRID, width=3)
    for gy in range(step, h_px, step):
        draw.line([(0, gy), (w_px, gy)], fill=GRID, width=3)

    # Border
    bw = max(2, round(dpi / 80))
    draw.rectangle([bw//2, bw//2, w_px - bw//2 - 1, h_px - bw//2 - 1],
                   outline=FG, width=bw)

    # Corner tick marks (engineering-drawing style)
    cm = max(8, round(min(w_px, h_px) * 0.13))
    lw = max(2, round(dpi / 80))
    for cx, cy in [(0,0), (w_px-1,0), (0,h_px-1), (w_px-1,h_px-1)]:
        sx = 1 if cx == 0 else -1
        sy = 1 if cy == 0 else -1
        draw.line([(cx, cy), (cx + sx*cm, cy)],  fill=FG, width=lw)
        draw.line([(cx, cy), (cx, cy + sy*cm)],  fill=FG, width=lw)

    # Icon
    pad  = max(8, round(min(w_px, h_px) * 0.09))
    icon = _detect_icon(text) if (icons and len(text) <= 60) else None
    if icon:
        icon_size = int(h_px * 0.55)
        icon_x    = pad
        icon_y    = (h_px - icon_size) // 2
        text_x0   = icon_x + icon_size + pad
    else:
        text_x0   = pad

    text_area_w = w_px - text_x0 - pad
    text_area_h = h_px - pad * 2

    display_text = _apply_case(text, text_case)
    font_path    = _find_font_path("mono", font_weight)

    if _has_inline_emoji(display_text):
        _render_inline_text(img, draw, display_text, text_x0, pad,
                            text_area_w, text_area_h, font_path=font_path,
                            fill=0.85, color=FG)
    else:
        words = display_text.split()
        max_n = min(len(words), 5)
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display_text]
        for n in range(1, min(max_n, 5) + 1):
            lines = _split_words(words, n)
            font, size = _largest_font_for("\n".join(lines), text_area_w, text_area_h, font_path, 0.85)
            if size > best_size:
                best_size, best_font, best_lines = size, font, lines

        joined = "\n".join(best_lines)
        stroke = 1 if font_weight in ("bold", "bold_italic") else 0
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center", stroke_width=stroke)
        x  = text_x0 + (text_area_w - (bb[2] - bb[0])) / 2 - bb[0]
        y  = (h_px - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill=FG, font=best_font, align="center",
                            stroke_width=stroke, stroke_fill=FG)

    if icon:
        _draw_icon(img, icon, icon_x, icon_y, icon_size, color=FG)

    return img


# ── QR Code renderer ──────────────────────────────────────────────────────────

def _render_qr_code(text: str, w_px: int, h_px: int, dpi: int,
                    text_case: str, font_weight: str = "bold",
                    show_text: bool = True) -> Image.Image:
    """QR code label. show_text=False centres the QR and omits the caption."""
    try:
        import qrcode as _qrcode
    except ImportError:
        img  = Image.new("RGB", (w_px, h_px), "white")
        draw = ImageDraw.Draw(img)
        draw.multiline_text((4, 4), "Install qrcode:\npip install qrcode[pil]",
                            fill="black", font=ImageFont.load_default())
        return img

    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)
    pad  = max(4, round(min(w_px, h_px) * 0.04))
    bw   = max(1, round(dpi / 150))

    # Generate QR (always uses raw text as data, regardless of text_case)
    qr = _qrcode.QRCode(version=None,
                        error_correction=_qrcode.constants.ERROR_CORRECT_M,
                        box_size=4, border=1)
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if not show_text:
        # QR centred, no caption
        qr_size = min(w_px - pad * 2, h_px - pad * 2)
        qr_img  = qr_img.resize((qr_size, qr_size), Image.NEAREST)
        img.paste(qr_img, ((w_px - qr_size) // 2, (h_px - qr_size) // 2))
        draw.rectangle([0, 0, w_px - 1, h_px - 1], outline="black", width=bw)
        return img

    if w_px > h_px * 1.5:
        # Landscape — QR on left, caption on right
        qr_size     = min(h_px - pad * 2, round(w_px * 0.45))
        qr_img      = qr_img.resize((qr_size, qr_size), Image.NEAREST)
        img.paste(qr_img, (pad, (h_px - qr_size) // 2))
        text_x0     = pad + qr_size + pad
        text_area_w = w_px - text_x0 - pad
        text_area_h = h_px - pad * 2
        text_y_center = True
        align       = "left"
    else:
        # Portrait / square — QR on top, caption below
        caption_h   = max(round(h_px * 0.22), round(0.18 * dpi))
        qr_size     = min(w_px - pad * 2, h_px - caption_h - pad * 2)
        qr_img      = qr_img.resize((qr_size, qr_size), Image.NEAREST)
        img.paste(qr_img, ((w_px - qr_size) // 2, pad))
        text_x0     = pad
        text_area_w = w_px - pad * 2
        text_area_h = caption_h - pad
        text_y0     = pad + qr_size + pad // 2
        text_y_center = False
        align       = "center"

    draw = ImageDraw.Draw(img)

    display_text = _apply_case(text, text_case)
    font_path    = _find_font_path("enhanced", font_weight)
    cap_y0 = 0 if text_y_center else text_y0
    cap_h  = h_px if text_y_center else text_area_h
    if _has_inline_emoji(display_text):
        _render_inline_text(img, draw, display_text, text_x0, cap_y0,
                            text_area_w, cap_h, font_path=font_path,
                            fill=0.85, align=align, color=(0, 0, 0))
    else:
        words        = display_text.split()
        max_n        = min(len(words), 5)
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display_text]
        for n in range(1, min(max_n, 4) + 1):
            lines = _split_words(words, n)
            font, size = _largest_font_for("\n".join(lines), text_area_w, text_area_h, font_path, 0.85)
            if size > best_size:
                best_size, best_font, best_lines = size, font, lines

        joined = "\n".join(best_lines)
        bb     = draw.multiline_textbbox((0, 0), joined, font=best_font, align=align)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x = text_x0 + (text_area_w - tw) / 2 - bb[0] if align == "center" else text_x0
        y = (h_px - th) / 2 - bb[1] if text_y_center else text_y0
        draw.multiline_text((x, y), joined, fill="black", font=best_font, align=align)

    draw.rectangle([0, 0, w_px - 1, h_px - 1], outline="black", width=bw)
    return img


# ── Barcode renderer ──────────────────────────────────────────────────────────

def _render_barcode(text: str, w_px: int, h_px: int, dpi: int,
                    text_case: str, font_weight: str = "bold",
                    show_text: bool = True) -> Image.Image:
    """Code 128 barcode label. Human-readable caption shown below unless
    show_text is False. Best on wider labels (4x2) where the bars stay scannable."""
    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)
    pad  = max(4, round(min(w_px, h_px) * 0.06))
    bw   = max(1, round(dpi / 150))

    try:
        from barcode import Code128
        from barcode.writer import ImageWriter
    except ImportError:
        draw.multiline_text((pad, pad), "Install python-barcode:\npip install python-barcode",
                            fill="black", font=ImageFont.load_default())
        return img

    # Code 128 covers ASCII only — anything else (emoji, accents) raises on encode
    data = (text or "").strip() or " "
    try:
        bc_img = Code128(data, writer=ImageWriter()).render({
            "write_text": False, "quiet_zone": 1.0,
            "module_height": 15.0, "background": "white", "foreground": "black",
        }).convert("L")
    except Exception:
        draw.multiline_text((pad, pad), "Barcode needs plain\nASCII text",
                            fill="black", font=ImageFont.load_default())
        draw.rectangle([0, 0, w_px - 1, h_px - 1], outline="black", width=bw)
        return img

    cap_h = max(round(h_px * 0.18), round(0.16 * dpi)) if show_text else 0
    bar_w = w_px - pad * 2
    bar_h = h_px - cap_h - pad * 2
    if bar_w > 0 and bar_h > 0:
        img.paste(bc_img.resize((bar_w, bar_h), Image.NEAREST).convert("RGB"), (pad, pad))

    if show_text:
        display   = _apply_case(text, text_case) or data
        font_path = _find_font_path("consolas", font_weight) or _find_font_path("mono", font_weight)
        f, _ = _largest_font_for(display, w_px - pad * 2, max(1, cap_h - pad // 2), font_path, 0.9)
        bb = draw.textbbox((0, 0), display, font=f)
        tx = (w_px - (bb[2] - bb[0])) / 2 - bb[0]
        ty = h_px - cap_h - pad // 2 + (cap_h - (bb[3] - bb[1])) / 2 - bb[1]
        draw.text((tx, ty), display, fill="black", font=f)

    draw.rectangle([0, 0, w_px - 1, h_px - 1], outline="black", width=bw)
    return img


# ── Name Tag renderer ─────────────────────────────────────────────────────────

def _render_name_tag(text: str, w_px: int, h_px: int, dpi: int,
                     text_case: str, font_weight: str = "bold") -> Image.Image:
    """Conference name badge: a black 'HELLO my name is' banner across the top,
    with the name large in the white field below."""
    BLACK = (0, 0, 0); WHITE = (255, 255, 255)
    img  = Image.new("RGB", (w_px, h_px), WHITE)
    draw = ImageDraw.Draw(img)
    bw = max(3, round(dpi / 65))
    r  = max(4, round(3 / 25.4 * dpi))
    banner_h = round(h_px * 0.34)

    # Fill the whole rounded rect black, then punch out the white body so the
    # banner inherits naturally-curved top corners; re-clip to remove corner bleed.
    draw.rounded_rectangle([0, 0, w_px - 1, h_px - 1], radius=r, fill=BLACK)
    draw.rectangle([bw, banner_h, w_px - bw - 1, h_px - bw - 1], fill=WHITE)
    clip = Image.new("L", (w_px, h_px), 255)
    ImageDraw.Draw(clip).rounded_rectangle([0, 0, w_px - 1, h_px - 1], radius=r, fill=0)
    img.paste(Image.new("RGB", (w_px, h_px), WHITE), mask=clip)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, w_px - 1, h_px - 1], radius=r, outline=BLACK, width=bw)
    draw.line([(bw, banner_h), (w_px - bw - 1, banner_h)], fill=BLACK, width=max(1, bw // 2))

    # Banner text — "HELLO" stacked over "my name is", white on black
    bfont = _find_font_path("standard", "bold")
    hf, _ = _largest_font_for("HELLO",      w_px - bw * 4, round(banner_h * 0.5),  bfont, 0.9)
    sf, _ = _largest_font_for("my name is", w_px - bw * 4, round(banner_h * 0.26), bfont, 0.9)
    hb = draw.textbbox((0, 0), "HELLO", font=hf)
    sb = draw.textbbox((0, 0), "my name is", font=sf)
    gap = round(banner_h * 0.06)
    block_h = (hb[3] - hb[1]) + gap + (sb[3] - sb[1])
    y0 = bw + (banner_h - bw - block_h) / 2
    draw.text(((w_px - (hb[2] - hb[0])) / 2 - hb[0], y0 - hb[1]), "HELLO", fill=WHITE, font=hf)
    draw.text(((w_px - (sb[2] - sb[0])) / 2 - sb[0], y0 + (hb[3] - hb[1]) + gap - sb[1]),
              "my name is", fill=WHITE, font=sf)

    # Name in the white field below
    pad     = max(6, round(min(w_px, h_px) * 0.05))
    name    = _apply_case(text, text_case)
    nf_path = _find_font_path("standard", font_weight)
    area_w  = w_px - pad * 2
    area_y0 = banner_h + pad
    area_h  = h_px - area_y0 - pad
    if _has_inline_emoji(name):
        _render_inline_text(img, draw, name, pad, area_y0,
                            area_w, area_h, font_path=nf_path,
                            fill=0.9, color=BLACK)
    else:
        words   = name.split()
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [name]
        for n in range(1, min(len(words), 3) + 1):
            lines = _split_words(words, n)
            f, size = _largest_font_for("\n".join(lines), area_w, area_h, nf_path, 0.9)
            if size > best_size:
                best_size, best_font, best_lines = size, f, lines
        joined = "\n".join(best_lines)
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center")
        x = (w_px - (bb[2] - bb[0])) / 2 - bb[0]
        y = area_y0 + (area_h - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill=BLACK, font=best_font, align="center")
    return img


# ── Receipt renderer ──────────────────────────────────────────────────────────

def _render_receipt(text: str, w_px: int, h_px: int, dpi: int,
                    text_case: str, font_weight: str = "bold") -> Image.Image:
    """Thermal-receipt aesthetic: centered monospace text framed by dashed rules."""
    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)
    pad  = max(6, round(min(w_px, h_px) * 0.08))
    lw   = max(1, round(dpi / 200))

    def dashed_rule(y):
        x = pad
        while x < w_px - pad:
            draw.line([(x, y), (min(x + 10, w_px - pad), y)], fill="black", width=lw)
            x += 16

    top_y, bot_y = pad, h_px - pad
    dashed_rule(top_y)
    dashed_rule(bot_y)

    font_path = _find_font_path("mono", font_weight) or _find_font_path("consolas", font_weight)
    area_w  = w_px - pad * 2
    area_y0 = top_y + pad // 2
    area_h  = bot_y - top_y - pad
    display = _apply_case(text, text_case)
    if _has_inline_emoji(display):
        _render_inline_text(img, draw, display, pad, area_y0,
                            area_w, area_h, font_path=font_path,
                            fill=0.9, color=(0, 0, 0))
    else:
        words   = display.split()
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display]
        for n in range(1, min(len(words), 5) + 1):
            lines = _split_words(words, n)
            f, size = _largest_font_for("\n".join(lines), area_w, area_h, font_path, 0.9)
            if size > best_size:
                best_size, best_font, best_lines = size, f, lines
        joined = "\n".join(best_lines)
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center")
        x = (w_px - (bb[2] - bb[0])) / 2 - bb[0]
        y = area_y0 + (area_h - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill="black", font=best_font, align="center")
    return img


# ── Chalkboard renderer ───────────────────────────────────────────────────────

def _render_chalkboard(text: str, w_px: int, h_px: int, dpi: int,
                       text_case: str, icons: bool = True,
                       font_weight: str = "bold") -> Image.Image:
    """Black chalkboard with white handwriting text and a thin chalk frame.
    Uses Ink Free for the chalk look regardless of the selected font."""
    BG = (0, 0, 0); FG = (255, 255, 255)
    img  = Image.new("RGB", (w_px, h_px), BG)
    draw = ImageDraw.Draw(img)

    fm = max(6, round(min(w_px, h_px) * 0.06))
    fw = max(2, round(dpi / 110))
    rr = max(4, round(min(w_px, h_px) * 0.05))
    draw.rounded_rectangle([fm, fm, w_px - fm - 1, h_px - fm - 1], radius=rr, outline=FG, width=fw)

    pad  = fm + max(6, round(min(w_px, h_px) * 0.05))
    icon = _detect_icon(text) if (icons and len(text) <= 60) else None
    if icon and h_px > w_px:
        # Portrait/tall label: icon on top, text below (size to width so it
        # never overflows a narrow label and forces a negative text area)
        icon_size = int(min(w_px * 0.5, h_px * 0.28))
        icon_x    = (w_px - icon_size) // 2
        icon_y    = pad
        text_x0   = pad
        text_y0   = icon_y + icon_size + pad
    elif icon:
        # Landscape label: icon on the left, text to the right
        icon_size = int(min(h_px * 0.5, w_px * 0.45))
        icon_x    = pad
        icon_y    = (h_px - icon_size) // 2
        text_x0   = icon_x + icon_size + pad
        text_y0   = pad
    else:
        text_x0   = pad
        text_y0   = pad

    text_area_w = max(1, w_px - text_x0 - pad)
    text_area_h = max(1, h_px - text_y0 - pad)
    display   = _apply_case(text, text_case)
    font_path = _find_font_path("inkfree", font_weight) or _find_font_path("enhanced", font_weight)
    if _has_inline_emoji(display):
        _render_inline_text(img, draw, display, text_x0, text_y0,
                            text_area_w, text_area_h, font_path=font_path,
                            fill=0.85, color=FG)
    else:
        words     = display.split()
        best_font, best_size, best_lines = ImageFont.load_default(), 8, [display]
        for n in range(1, min(len(words), 5) + 1):
            lines = _split_words(words, n)
            f, size = _largest_font_for("\n".join(lines), text_area_w, text_area_h, font_path, 0.85)
            if size > best_size:
                best_size, best_font, best_lines = size, f, lines
        joined = "\n".join(best_lines)
        bb = draw.multiline_textbbox((0, 0), joined, font=best_font, align="center")
        x = text_x0 + (text_area_w - (bb[2] - bb[0])) / 2 - bb[0]
        y = text_y0 + (text_area_h - (bb[3] - bb[1])) / 2 - bb[1]
        draw.multiline_text((x, y), joined, fill=FG, font=best_font, align="center")
    if icon:
        _draw_icon(img, icon, icon_x, icon_y, icon_size, color=FG)
    return img


# ── Text fitting ──────────────────────────────────────────────────────────────

def _fit_text(text, max_w, max_h, font_style="standard", fill=0.85, font_weight="bold"):
    font_path = _find_font_path(font_style, font_weight)

    # If the text contains explicit newlines, honour them as forced line breaks
    # and just find the best font size for that fixed arrangement.
    if "\n" in text:
        forced = [l.strip() for l in text.split("\n")]
        font, _ = _largest_font_for("\n".join(forced), max_w, max_h, font_path, fill)
        return forced, font

    words = text.split()
    # Try every split from 1 line up to one-word-per-line; pick the biggest font.
    max_n      = min(len(words), 5)
    best_font  = ImageFont.load_default()
    best_size  = 0
    best_lines = [text]

    for n in range(1, min(max_n, 5) + 1):
        lines = _split_words(words, n)
        font, size = _largest_font_for("\n".join(lines), max_w, max_h, font_path, fill)
        if size > best_size:
            best_size, best_font, best_lines = size, font, lines

    return best_lines, best_font


def _split_words(words, n):
    if n == 1:
        return [" ".join(words)]
    if n >= len(words):
        return list(words)
    # Distribute as evenly as possible — earlier lines get the spare word when
    # the count doesn't divide cleanly.  This prevents all the remainder words
    # piling up on the last line (e.g. "Oh / Baby / It's / Cold Outside").
    base  = len(words) // n
    extra = len(words) % n
    lines, i = [], 0
    for idx in range(n):
        count = base + (1 if idx < extra else 0)
        lines.append(" ".join(words[i:i + count]))
        i += count
    return lines


def _largest_font_for(text, max_w, max_h, font_path, fill=0.85):
    if not font_path:
        return ImageFont.load_default(), 0
    # textbbox only measures — it never draws — so a 1×1 canvas is enough and
    # avoids allocating a large image on every call.
    draw      = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    best, best_size = ImageFont.load_default(), 0
    try:
        best = ImageFont.truetype(font_path, 8)
        best_size = 8
    except Exception:
        pass
    for size in range(8, 400, 2):
        try:
            f = ImageFont.truetype(font_path, size)
        except OSError:
            break
        bb = draw.multiline_textbbox((0, 0), text, font=f, align="center")
        if (bb[2] - bb[0]) > max_w * fill or (bb[3] - bb[1]) > max_h * fill:
            break
        best, best_size = f, size
    return best, best_size


def _find_font_path(font_style="standard", font_weight="bold"):
    style_variants = _FONT_MAP.get(font_style, _FONT_MAP["standard"])
    candidates = style_variants.get(font_weight, style_variants.get("bold", []))
    return next((p for p in candidates if os.path.exists(p)), None)

# ── Inline emoji rendering ─────────────────────────────────────────────────────
# Lets literal emoji typed/pasted into the label text render as (monochrome)
# emoji graphics inline with the words, instead of font "tofu" boxes.  This is
# independent of the keyword auto-icon feature and the icons on/off setting.

_EMOJI_ZWJ    = 0x200D
_EMOJI_VS16   = 0xFE0F
_EMOJI_VS15   = 0xFE0E
_EMOJI_KEYCAP = 0x20E3


def _is_regional(o):
    return 0x1F1E6 <= o <= 0x1F1FF


def _is_skin_tone(o):
    return 0x1F3FB <= o <= 0x1F3FF


def _is_emoji_cp(o):
    """True if a codepoint should be drawn via the emoji pipeline rather than
    the text font."""
    return (
        0x1F300 <= o <= 0x1FAFF or   # pictographs, emoticons, transport, ext-A
        0x1F000 <= o <= 0x1F0FF or   # mahjong / dominoes / cards
        0x2600  <= o <= 0x27BF  or   # misc symbols + dingbats (☕ ✂ ✅ …)
        0x2B00  <= o <= 0x2BFF  or   # arrows / stars block (⬛ ⭐ …)
        0x23E9  <= o <= 0x23FA  or   # media controls, alarm clock, hourglass
        _is_regional(o)         or
        o in (0x231A, 0x231B, 0x2328, 0x24C2, 0x25AA, 0x25AB, 0x25B6,
              0x25C0, 0x2122, 0x2139, 0x203C, 0x2049, 0x2934, 0x2935)
    )


def _has_inline_emoji(text):
    return any(_is_emoji_cp(ord(c)) for c in text)


def _split_text_emoji(s):
    """Split a string into [(kind, value)] tokens, kind ∈ {'text','emoji'}.
    Each 'emoji' token is a single render cluster — ZWJ sequences, flag pairs and
    base+modifier/variation-selector combos are kept together so HarfBuzz can
    shape them into one glyph."""
    out, buf = [], []
    i, n = 0, len(s)

    def flush():
        if buf:
            out.append(("text", "".join(buf)))
            buf.clear()

    while i < n:
        o = ord(s[i])
        if not _is_emoji_cp(o):
            buf.append(s[i])
            i += 1
            continue
        flush()
        start = i
        if _is_regional(o):
            # regional indicators combine in pairs → one flag
            i += 1
            if i < n and _is_regional(ord(s[i])):
                i += 1
            out.append(("emoji", s[start:i]))
            continue
        i += 1
        while i < n:                       # absorb modifiers / VS / ZWJ chains
            oc = ord(s[i])
            if oc in (_EMOJI_VS16, _EMOJI_VS15, _EMOJI_KEYCAP) or _is_skin_tone(oc):
                i += 1
            elif oc == _EMOJI_ZWJ:
                i += 1
                if i < n:                  # pull in the emoji following the ZWJ
                    i += 1
            else:
                break
        out.append(("emoji", s[start:i]))
    flush()
    return out


def _line_tokens(words):
    """Flatten a list of words into render tokens with explicit spaces between."""
    toks = []
    for j, word in enumerate(words):
        if j:
            toks.append(("space", " "))
        toks.extend(_split_text_emoji(word))
    return toks


def _measure_tokens(toks, font, em, space_w):
    w = 0.0
    for kind, val in toks:
        if kind == "emoji":
            w += em
        elif kind == "space":
            w += space_w
        else:
            w += font.getlength(val)
    return w


def _render_inline_text(img, draw, text, x0, y0, area_w, area_h,
                        font_style="standard", fill=0.85, font_weight="bold",
                        align="center", color=(0, 0, 0), font_path=None):
    """Lay out and draw text that contains literal emoji within the given box.
    Mirrors _fit_text's wrap-and-grow behaviour but measures emoji as square
    boxes and paints them with the shared emoji pipeline (_draw_icon).
    font_path overrides font_style/font_weight when provided directly."""
    if font_path is None:
        font_path = _find_font_path(font_style, font_weight)
    if not font_path:
        return

    # Candidate line arrangements: honour explicit newlines, else try 1..5 lines.
    if "\n" in text:
        arrangements = [[ln.split() for ln in text.split("\n")]]
    else:
        words = text.split()
        if not words:
            return
        max_n = min(len(words), 5)
        arrangements = [[w.split() for w in _split_words(words, n)]
                        for n in range(1, max_n + 1)]

    # Tokens are font-independent — build them once, reuse across size probes.
    arr_tokens = [[_line_tokens(w) for w in lines] for lines in arrangements]

    best = None        # (font, idx, em, spacing, ascent, lh)
    best_size = -1
    for size in range(8, 400, 2):
        try:
            font = ImageFont.truetype(font_path, size)
        except OSError:
            break
        ascent, descent = font.getmetrics()
        lh      = ascent + descent
        em      = lh
        spacing = max(2, round(lh * 0.08))
        space_w = font.getlength(" ")

        fit_idx = None
        for idx, toks_lines in enumerate(arr_tokens):
            block_w = max((_measure_tokens(t, font, em, space_w) for t in toks_lines),
                          default=0.0)
            block_h = lh * len(toks_lines) + spacing * (len(toks_lines) - 1)
            if block_w <= area_w * fill and block_h <= area_h * fill:
                fit_idx = idx
                break
        if fit_idx is not None:
            best = (font, fit_idx, em, spacing, ascent, lh)
            best_size = size
        elif best_size >= 0:
            break          # blocks only grow with size — nothing larger will fit

    if best is None:       # fall back to the smallest size, first arrangement
        font = ImageFont.truetype(font_path, 8)
        ascent, descent = font.getmetrics()
        lh = ascent + descent
        best = (font, 0, lh, max(2, round(lh * 0.08)), ascent, lh)

    font, idx, em, spacing, ascent, lh = best
    toks_lines = arr_tokens[idx]
    space_w    = font.getlength(" ")
    block_h    = lh * len(toks_lines) + spacing * (len(toks_lines) - 1)
    y          = y0 + (area_h - block_h) / 2

    for toks in toks_lines:
        line_w = _measure_tokens(toks, font, em, space_w)
        if align == "left":
            lx = x0
        elif align == "right":
            lx = x0 + area_w - line_w
        else:
            lx = x0 + (area_w - line_w) / 2
        baseline = y + ascent
        for kind, val in toks:
            if kind == "emoji":
                _draw_icon(img, val, int(round(lx)), int(round(y)), int(em), color=color)
                lx += em
            elif kind == "space":
                lx += space_w
            else:
                draw.text((lx, baseline), val, font=font, fill=color, anchor="ls")
                lx += font.getlength(val)
        y += lh + spacing

# ── Icon detection & drawing ──────────────────────────────────────────────────

# Emoji font paths — first one found wins (used for Segoe/FreeType path)
_EMOJI_FONT_PATHS = [
    r"C:\Windows\Fonts\seguiemj.ttf",   # Segoe UI Emoji (Windows 10/11)
    r"C:\Windows\Fonts\seguisym.ttf",   # Segoe UI Symbol (fallback)
]

# Noto Color Emoji (Windows Compatible) — CBDT/PNG format, supports country flags
_NOTO_PATH = os.path.join(_USER_FONTS, "NotoColorEmoji_WindowsCompatible.ttf")

# Cache for Noto fonttools objects (loaded once, reused)
_noto_cache = {}

def _render_emoji_noto(emoji_char: str, target_size: int):
    """Render emoji via fonttools PNG extraction from Noto Color Emoji CBDT table.
    Supports country flags and all emoji Noto covers. Returns RGBA PIL image or None.
    """
    if not os.path.exists(_NOTO_PATH):
        return None
    try:
        import uharfbuzz as hb
        import io

        # Load/cache fonttools + raw bytes + HarfBuzz face/font (built once, reused)
        if 'tt' not in _noto_cache:
            from fontTools.ttLib import TTFont
            _noto_cache['tt'] = TTFont(_NOTO_PATH)
            with open(_NOTO_PATH, 'rb') as f:
                _noto_cache['data'] = f.read()
            _noto_cache['strike'] = _noto_cache['tt']['CBDT'].strikeData[0]
            hb_face = hb.Face(_noto_cache['data'])
            hb_font = hb.Font(hb_face)
            hb_font.scale = (109 * 64, 109 * 64)   # Noto's only strike is 109px
            _noto_cache['hb_face'] = hb_face
            _noto_cache['hb_font'] = hb_font

        tt      = _noto_cache['tt']
        strike  = _noto_cache['strike']
        hb_font = _noto_cache['hb_font']

        # Shape with HarfBuzz to resolve ZWJ / flag sequences → glyph ID
        buf = hb.Buffer()
        buf.add_str(emoji_char)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)

        infos = buf.glyph_infos
        if not infos:
            return None

        # For multi-glyph sequences (shouldn't happen after shaping, but be safe)
        glyph_name = tt.getGlyphName(infos[0].codepoint)
        if glyph_name not in strike:
            return None

        raw = strike[glyph_name].imageData
        img = Image.open(io.BytesIO(raw)).convert('RGBA')

        # Resize to target (Noto strike is always 136x128 — crop to square then resize)
        side = min(img.size)
        left = (img.width  - side) // 2
        top  = (img.height - side) // 2
        img  = img.crop((left, top, left + side, top + side))
        img  = img.resize((target_size, target_size), Image.LANCZOS)

        # Convert RGBA → L-mode (white=background, dark=ink) to match Segoe pipeline:
        # composite grayscale emoji over white using alpha as mask
        gray = img.convert('L')
        alpha = img.split()[3]
        bg = Image.new('L', img.size, 255)
        result = Image.composite(gray, bg, alpha)
        return result, alpha

    except Exception:
        return None


# Compiled-pattern caches for _detect_icon, built once on first use.
# Pre-compiling avoids re-escaping + recompiling ~3,000 patterns on every call —
# Python's built-in regex cache only holds 512 entries, so it thrashes here and
# the naive version ends up recompiling on nearly every keystroke (~76 ms/call).
_PHASE1_PATTERNS = None   # list of (compiled \bkeyword\b, keyword_len, icon)
_PHASE2_PATTERNS = None   # list of (icon, [compiled patterns to try, in order])

# User-defined keyword → emoji overrides (set via the Advanced page). These are
# checked BEFORE the built-in keyword maps, so a custom "kitchen → 🍕" wins over
# the built-in match. Each tuple is (compiled \bkeyword\b, keyword_len, emoji);
# the emoji char is returned directly (not an icon_type key) and flows through
# _draw_icon, which falls back to treating an unknown icon_type as a literal emoji.
_CUSTOM_PATTERNS = []   # list of (compiled pattern, keyword_len, emoji_char)


def set_custom_emojis(mapping):
    """Install user keyword→emoji overrides. `mapping` is {keyword: emoji_char}.
    Rebuilds the match list (longest keyword wins among custom entries)."""
    global _CUSTOM_PATTERNS
    patterns = []
    for keyword, emoji in (mapping or {}).items():
        kw = (keyword or "").strip().lower()
        if not kw or not emoji:
            continue
        patterns.append((re.compile(r"\b" + re.escape(kw) + r"\b"), len(kw), emoji))
    _CUSTOM_PATTERNS = patterns


def _match_custom(lower: str):
    """Return the custom emoji for the longest matching keyword, or None."""
    best_len, best_emoji = -1, None
    for pat, klen, emoji in _CUSTOM_PATTERNS:
        if klen > best_len and pat.search(lower):
            best_len, best_emoji = klen, emoji
    return best_emoji


def _build_icon_pattern_cache():
    """Pre-compile every keyword pattern once. ~0.9 MB, ~23x faster detection."""
    global _PHASE1_PATTERNS, _PHASE2_PATTERNS
    phase1, phase2 = [], []
    for keyword, icon in _ICON_KEYWORDS.items():
        k = re.escape(keyword)
        phase1.append((re.compile(r'\b' + k + r'\b'), len(keyword), icon))

        if ' ' in keyword:
            continue  # multi-word keywords are handled in phase 1 only

        # Same inflection rules as before, in the same try-order so the
        # first-match-wins result is identical to the original implementation.
        pats = [re.compile(r'\b' + k + r'e?s\b')]                       # plural
        if keyword.endswith('y'):
            pats.append(re.compile(r'\b' + re.escape(keyword[:-1]) + r'ies\b'))
        if keyword.endswith('fe'):
            pats.append(re.compile(r'\b' + re.escape(keyword[:-2]) + r'ves\b'))
        elif keyword.endswith('f'):
            pats.append(re.compile(r'\b' + re.escape(keyword[:-1]) + r'ves\b'))
        if keyword.endswith('s') and len(keyword) > 3:
            pats.append(re.compile(r'\b' + re.escape(keyword[:-1]) + r'\b'))  # singular
        phase2.append((icon, pats))

    _PHASE1_PATTERNS, _PHASE2_PATTERNS = phase1, phase2


def _detect_icon(text: str):
    if _PHASE1_PATTERNS is None:
        _build_icon_pattern_cache()
    lower = text.lower()

    # Custom user emojis override everything built-in.
    custom = _match_custom(lower)
    if custom:
        return custom

    # Phase 1: direct word-boundary matches — collect ALL matches and return
    # the one with the LONGEST keyword so "polar bear" beats "bear", etc.
    best_len  = -1
    best_icon = None
    for pat, klen, icon in _PHASE1_PATTERNS:
        if pat.search(lower) and klen > best_len:
            best_len  = klen
            best_icon = icon
    if best_icon:
        return best_icon

    # Phase 2: inflection rules (first match wins — compound forms handled above)
    for icon, pats in _PHASE2_PATTERNS:
        for pat in pats:
            if pat.search(lower):
                return icon
    return None


def _render_emoji_shaped(emoji_char: str, font_path: str, target_size: int):
    """Shape and render an emoji (including ZWJ sequences) via HarfBuzz + FreeType.

    Returns an L-mode PIL image (white=background, dark=ink), cropped to the
    inked region, or None if HarfBuzz/FreeType are unavailable or rendering fails.
    """
    try:
        import uharfbuzz as hb
        import freetype as ft_lib
    except ImportError:
        return None
    try:
        with open(font_path, 'rb') as f:
            font_data = f.read()

        # --- Shape with HarfBuzz (resolves ZWJ ligatures to single glyph IDs) ---
        hb_face = hb.Face(font_data)
        hb_font = hb.Font(hb_face)
        hb_font.scale = (target_size * 64, target_size * 64)
        buf = hb.Buffer()
        buf.add_str(emoji_char)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)
        infos    = buf.glyph_infos
        pos_list = buf.glyph_positions

        # Canvas sized to the total advance
        total_adv = sum(p.x_advance >> 6 for p in pos_list)
        canvas_w  = max(total_adv, target_size)
        canvas_h  = target_size + target_size // 2
        baseline  = int(target_size * 0.85)
        result       = Image.new("L", (canvas_w, canvas_h), 255)
        alpha_canvas = Image.new("L", (canvas_w, canvas_h), 0)

        # --- Render each shaped glyph with FreeType ---
        ft_face = ft_lib.Face(font_path)
        ft_face.set_pixel_sizes(0, target_size)
        FT_LOAD_RENDER = 4
        FT_LOAD_COLOR  = 1 << 20

        pen = 0
        for info, pos in zip(infos, pos_list):
            loaded = False
            for flags in (FT_LOAD_RENDER | FT_LOAD_COLOR, FT_LOAD_RENDER):
                try:
                    ft_face.load_glyph(info.codepoint, flags)
                    loaded = True
                    break
                except Exception:
                    pass
            if not loaded:
                pen += pos.x_advance >> 6
                continue

            bm = ft_face.glyph.bitmap
            if bm.width == 0 or bm.rows == 0:
                pen += pos.x_advance >> 6
                continue

            ox   = pen + (pos.x_offset >> 6) + ft_face.glyph.bitmap_left
            oy   = baseline - ft_face.glyph.bitmap_top
            data = bytes(bm.buffer)

            if bm.pixel_mode == ft_lib.FT_PIXEL_MODE_BGRA:
                # Color emoji (CBDT format): bytes are BGRA, Pillow reads as RGBA
                raw           = Image.frombytes('RGBA', (bm.width, bm.rows), data)
                ch0, ch1, ch2, ch3 = raw.split()   # ch0=actual_B, ch2=actual_R
                gray  = Image.merge('RGBA', [ch2, ch1, ch0, ch3]).convert('L')
                alpha = ch3
                result.paste(gray, (ox, oy), mask=alpha)
                alpha_canvas.paste(alpha, (ox, oy))
            elif bm.pixel_mode == ft_lib.FT_PIXEL_MODE_GRAY:
                # Grayscale: 0=transparent, 255=ink — paste black using value as mask
                mask = Image.frombytes('L', (bm.width, bm.rows), data)
                result.paste(Image.new('L', mask.size, 0), (ox, oy), mask=mask)
                alpha_canvas.paste(mask, (ox, oy))

            pen += pos.x_advance >> 6

        diff = ImageChops.difference(result, Image.new("L", result.size, 255))
        bb   = diff.getbbox()
        if not bb:
            return None
        return result.crop(bb), alpha_canvas.crop(bb)

    except Exception:
        return None


def _draw_icon(img, icon_type, x, y, size, color=(0, 0, 0), skip_noto=False, skip_hb=False):
    """Render an emoji into a temp image, crop to actual ink, then paste into img.

    skip_noto=True  — bypass Noto PNG extraction, use HarfBuzz/FreeType instead.
    skip_hb=True    — bypass HarfBuzz/FreeType, use basic Pillow text rendering.
    Both True       — force the Pillow fallback (simple outline, no colour data).
    """
    # Built-in detection returns an icon_type key (looked up here); custom
    # detection returns the emoji char directly, so an unknown key IS the emoji.
    emoji = _ICON_EMOJIS.get(icon_type, icon_type)
    if not emoji:
        return

    # Try Noto Color Emoji first — supports flags + all emoji via PNG extraction
    outline_alpha = None
    noto_result = None if skip_noto else _render_emoji_noto(emoji, size * 2)
    if noto_result is not None:
        emoji_img, outline_alpha = noto_result
    else:
        emoji_img = None

    if emoji_img is None:
        # Fall back to HarfBuzz+FreeType with Segoe UI Emoji
        font_path = next((p for p in _EMOJI_FONT_PATHS if os.path.exists(p)), None)
        if not font_path:
            return
        hb_result = None if skip_hb else _render_emoji_shaped(emoji, font_path, size * 2)
        if hb_result is not None:
            emoji_img, outline_alpha = hb_result

    if emoji_img is None:
        # Fallback: Pillow-based rendering (no ZWJ support but works for simple emoji)
        canvas = size * 4
        tmp    = Image.new("L", (canvas, canvas), 255)
        tdraw  = ImageDraw.Draw(tmp)
        best_font = None
        target    = size * 1.5
        for pt in range(8, 400, 2):
            try:
                f  = ImageFont.truetype(font_path, pt)
                bb = tdraw.textbbox((0, 0), emoji, font=f)
                if (bb[2] - bb[0]) > target or (bb[3] - bb[1]) > target:
                    break
                best_font = f
            except OSError:
                break
        if best_font is None:
            return
        cx, cy = canvas // 2, canvas // 2
        tdraw.text((cx, cy), emoji, font=best_font, fill=0, anchor="mm")
        diff = ImageChops.difference(tmp, Image.new("L", tmp.size, 255))
        ink_bb = diff.getbbox()
        if not ink_bb:
            return
        emoji_img     = tmp.crop(ink_bb)
        outline_alpha = diff.crop(ink_bb)   # diff value = ink opacity

    ew, eh = emoji_img.size

    # Scale to fill 82% of the icon area
    scale = min(size * 0.82 / ew, size * 0.82 / eh)
    if scale != 1.0:
        emoji_img = emoji_img.resize(
            (max(1, int(ew * scale)), max(1, int(eh * scale))),
            Image.LANCZOS,
        )
        ew, eh = emoji_img.size

    # Optional darkness boost: shifts ink pixels toward black while leaving the
    # pure-white background untouched. factor 1.0 = no change; 4.0 = near-black.
    darkness = _emoji_darkness()
    if darkness:
        factor = 1.0 + (darkness / 100) * 3.0
        emoji_img = emoji_img.point(lambda x: max(0, 255 - int((255 - x) * factor)))

    # Optional shape-following outline: dilate the emoji silhouette by outline_px
    # pixels, paint it black first, then paste the emoji on top so light-colored
    # emojis still have a crisp black border even without heavy darkness boosting.
    outline_px = _emoji_outline()
    if outline_px:
        from PIL import ImageFilter
        # Pad canvas so the outline ring isn't clipped at the edges
        pad = outline_px + 2
        padded_w, padded_h = ew + pad * 2, eh + pad * 2
        padded = Image.new("L", (padded_w, padded_h), 255)
        padded.paste(emoji_img, (pad, pad))
        # Use the alpha channel (true silhouette) when available — this correctly
        # handles flags, which have white stripes that would be missed by a gray
        # threshold. Fall back to thresholding if no alpha was captured.
        if outline_alpha is not None:
            alpha_padded = Image.new("L", (padded_w, padded_h), 0)
            scaled_alpha = outline_alpha.resize((ew, eh), Image.LANCZOS)
            alpha_padded.paste(scaled_alpha, (pad, pad))
            silhouette = alpha_padded.point(lambda v: 255 if v > 32 else 0)
        else:
            silhouette = padded.point(lambda v: 255 if v < 240 else 0)
        # Dilate silhouette for ring, subtract to get ring only
        kernel    = outline_px * 2 + 1
        expanded  = silhouette.filter(ImageFilter.MaxFilter(kernel))
        ring_mask = ImageChops.subtract(expanded, silhouette)
        paste_x = x + (size - padded_w) // 2
        paste_y = y + (size - padded_h) // 2
        # 1. Paint only the ring black — interior stays as label background
        black_img = Image.new("RGB", (padded_w, padded_h), (0, 0, 0))
        img.paste(black_img, (paste_x, paste_y), mask=ring_mask)
        # 2. Paint the emoji normally on top (same variable-opacity as no-outline path)
        color_img = Image.new("RGB", (padded_w, padded_h), color)
        img.paste(color_img, (paste_x, paste_y), mask=ImageChops.invert(padded))
        return

    # Paste centered: invert L mask so 255=opaque ink, 0=transparent
    mask      = ImageChops.invert(emoji_img)
    color_img = Image.new("RGB", emoji_img.size, color)
    paste_x   = x + (size - ew) // 2
    paste_y   = y + (size - eh) // 2
    img.paste(color_img, (paste_x, paste_y), mask=mask)

# ── Border drawing ────────────────────────────────────────────────────────────

def _overlay_image_border(img: Image.Image, name: str, w_px: int, h_px: int,
                          margin: int = 4) -> Image.Image:
    """Resize border_<name>.* slightly inset from the label edges, recolour to black,
    and composite.  The margin keeps the design clear of the printer's edge limits."""
    path = next(
        (f for ext in (".png", ".webp", ".jpg", ".jpeg")
         for f in [os.path.join(_IMAGES_DIR, f"border_{name}{ext}")]
         if os.path.exists(f)),
        None,
    )
    if not path:
        return img
    bw = w_px - margin * 2
    bh = h_px - margin * 2
    border = Image.open(path).convert("RGBA").resize((bw, bh), Image.LANCZOS)
    # Force all non-transparent pixels to pure black
    _, _, _, a = border.split()
    black_border = Image.merge("RGBA", [
        Image.new("L", border.size, 0),
        Image.new("L", border.size, 0),
        Image.new("L", border.size, 0),
        a,
    ])
    base = img.convert("RGBA")
    base.alpha_composite(black_border, dest=(margin, margin))
    return base.convert("RGB")


def _draw_border(draw, w, h, pad, style, dpi=203):
    if style == "none":
        return
    p = max(2, pad // 2)
    # 3 mm physical corner radius — matches the label's own rounded corners
    r = max(4, round(3 / 25.4 * dpi))

    if style == "thin":
        draw.rounded_rectangle([p, p, w-p-1, h-p-1], radius=r,
                                outline="black", width=2)

    elif style == "thick":
        draw.rounded_rectangle([p, p, w-p-1, h-p-1], radius=r,
                                outline="black", width=5)

    elif style == "double":
        draw.rounded_rectangle([p,   p,   w-p-1, h-p-1], radius=r,
                                outline="black", width=2)
        draw.rounded_rectangle([p+5, p+5, w-p-6, h-p-6], radius=max(2, r-5),
                                outline="black", width=1)

    elif style == "dashed":
        # Solid rounded arcs at each corner; dashes along the straight edges
        dash, gap, lw = 12, 6, 2
        draw.arc([p,         p,         p+2*r,     p+2*r    ], 180, 270, fill="black", width=lw)
        draw.arc([w-p-2*r-1, p,         w-p-1,     p+2*r    ], 270, 360, fill="black", width=lw)
        draw.arc([p,         h-p-2*r-1, p+2*r,     h-p-1    ],  90, 180, fill="black", width=lw)
        draw.arc([w-p-2*r-1, h-p-2*r-1, w-p-1,    h-p-1    ],   0,  90, fill="black", width=lw)
        # top & bottom straight sections
        for edge_y in (p, h-p-1):
            x = p + r
            while x < w - p - r:
                draw.line([(x, edge_y), (min(x+dash, w-p-r), edge_y)],
                          fill="black", width=lw)
                x += dash + gap
        # left & right straight sections
        for edge_x in (p, w-p-1):
            y = p + r
            while y < h - p - r:
                draw.line([(edge_x, y), (edge_x, min(y+dash, h-p-r))],
                          fill="black", width=lw)
                y += dash + gap

    elif style == "dotted":
        # Round dots tracing the rounded-rect perimeter (companion to dashed)
        dot_r = max(1, round(dpi / 110))
        step  = max(dot_r * 4, 8)
        def _dot(cx, cy):
            draw.ellipse([cx-dot_r, cy-dot_r, cx+dot_r, cy+dot_r], fill="black")
        x = p + r
        while x <= w - p - r:
            _dot(x, p); _dot(x, h - p - 1); x += step
        y = p + r
        while y <= h - p - r:
            _dot(p, y); _dot(w - p - 1, y); y += step
        # quarter-circle corner dots (same arc spans as the dashed corners)
        for cx, cy, a0 in ((p+r, p+r, 180), (w-p-r-1, p+r, 270),
                           (p+r, h-p-r-1, 90), (w-p-r-1, h-p-r-1, 0)):
            for k in range(1, 5):
                a = math.radians(a0 + k * 18)
                _dot(cx + r * math.cos(a), cy + r * math.sin(a))

    elif style == "wave":
        # Scalloped edge — a run of equal semicircle arcs bulging inward on each
        # side. Only full scallops are drawn (centred per edge) so the last one is
        # never squished; any leftover splits evenly into the end margins.
        lw = 2
        span_x = (w - 1) - 2 * p
        span_y = (h - 1) - 2 * p
        d  = max(12, round(min(w, h) / 12))
        nx = max(1, span_x // d)
        ny = max(1, span_y // d)
        ox = p + (span_x - nx * d) // 2          # centring offset on horizontal edges
        oy = p + (span_y - ny * d) // 2          # centring offset on vertical edges
        for i in range(nx):
            x = ox + i * d
            draw.arc([x, p, x + d, p + d], 0, 180, fill="black", width=lw)                  # top
            draw.arc([x, h-p-1-d, x + d, h-p-1], 180, 360, fill="black", width=lw)          # bottom
        for i in range(ny):
            y = oy + i * d
            draw.arc([p, y, p + d, y + d], 270, 450, fill="black", width=lw)                # left
            draw.arc([w-p-1-d, y, w-p-1, y + d], 90, 270, fill="black", width=lw)           # right

    elif style == "ticket":
        # Solid thin frame plus an inner ring of perforation holes (raffle ticket)
        draw.rounded_rectangle([p, p, w-p-1, h-p-1], radius=r, outline="black", width=2)
        gap   = max(6, round(min(w, h) * 0.05))
        dot_r = max(1, round(dpi / 120))
        step  = max(dot_r * 5, 12)
        ix1, iy1, ix2, iy2 = p+gap, p+gap, w-p-gap-1, h-p-gap-1
        def _pdot(cx, cy):
            draw.ellipse([cx-dot_r, cy-dot_r, cx+dot_r, cy+dot_r], fill="black")
        x = ix1
        while x <= ix2:
            _pdot(x, iy1); _pdot(x, iy2); x += step
        y = iy1
        while y <= iy2:
            _pdot(ix1, y); _pdot(ix2, y); y += step

    elif style == "inset":
        # Recessed-panel look: concentric frames with a thickened inner top/left
        # edge reading as a shadow cast into the recess
        gap = max(5, round(dpi / 40))
        ri  = max(2, r - gap)
        draw.rounded_rectangle([p, p, w-p-1, h-p-1], radius=r, outline="black", width=2)
        draw.rounded_rectangle([p+gap, p+gap, w-p-gap-1, h-p-gap-1], radius=ri,
                                outline="black", width=2)
        sw = max(2, round(dpi / 90))
        draw.line([(p+gap+ri, p+gap+1), (w-p-gap-1-ri, p+gap+1)], fill="black", width=sw)
        draw.line([(p+gap+1, p+gap+ri), (p+gap+1, h-p-gap-1-ri)], fill="black", width=sw)

    elif style == "rounded":
        # More pronounced decorative radius — intentionally larger than 3 mm
        big_r = min(w, h) // 6
        draw.rounded_rectangle([p, p, w-p-1, h-p-1], radius=big_r,
                                outline="black", width=2)

    elif style == "corners":
        # Tick marks on the straight edges, clear of the curved corners
        arm = max(8, min(w, h) // 5)
        lw  = 2
        # top-left
        draw.line([(p+r,   p),   (p+r+arm, p)    ], fill="black", width=lw)
        draw.line([(p,     p+r), (p,        p+r+arm)], fill="black", width=lw)
        # top-right
        draw.line([(w-p-r,   p),   (w-p-r-arm, p)    ], fill="black", width=lw)
        draw.line([(w-p-1,   p+r), (w-p-1,     p+r+arm)], fill="black", width=lw)
        # bottom-left
        draw.line([(p+r,   h-p-1), (p+r+arm, h-p-1)  ], fill="black", width=lw)
        draw.line([(p,     h-p-r), (p,        h-p-r-arm)], fill="black", width=lw)
        # bottom-right
        draw.line([(w-p-r,   h-p-1), (w-p-r-arm, h-p-1)  ], fill="black", width=lw)
        draw.line([(w-p-1,   h-p-r), (w-p-1,     h-p-r-arm)], fill="black", width=lw)

# ── DEVMODE / DC helpers ──────────────────────────────────────────────────────

def _get_devmode_buf(printer_name, width_in, height_in):
    try:
        hPrinter = ctypes.c_void_p()
        if not _winspool.OpenPrinterW(printer_name, ctypes.byref(hPrinter), None):
            return None
        try:
            dm_size = _winspool.DocumentPropertiesW(
                None, hPrinter, printer_name, None, None, 0)
            if dm_size <= 0:
                return None
            buf = ctypes.create_string_buffer(dm_size)
            ret = _winspool.DocumentPropertiesW(
                None, hPrinter, printer_name, buf, None, _DM_OUT_BUFFER)
            if ret < 0:
                return None
            fields = struct.unpack_from("<I", buf, _OFF_FIELDS)[0]
            struct.pack_into("<I", buf, _OFF_FIELDS,
                             fields | _DM_PAPERSIZE | _DM_PAPERLENGTH | _DM_PAPERWIDTH)
            struct.pack_into("<h", buf, _OFF_PAPERSIZE,   _DMPAPER_USER)
            struct.pack_into("<h", buf, _OFF_PAPERLENGTH, int(height_in * 254))
            struct.pack_into("<h", buf, _OFF_PAPERWIDTH,  int(width_in  * 254))
            return buf
        finally:
            _winspool.ClosePrinter(hPrinter)
    except Exception:
        return None
