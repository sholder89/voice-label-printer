"""Label rendering and printing via Windows GDI."""
import ctypes
import glob
import os
import re
import struct
from PIL import Image, ImageChops, ImageDraw, ImageFont

try:
    import win32print
    import win32ui
    from PIL import ImageWin
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# ── Label sizes ───────────────────────────────────────────────────────────────

LABEL_SIZES = {
    "2x1":   (2.0, 1.0),
    "4x2":   (4.0, 2.0),
    "4x6":   (4.0, 6.0),
    "3x2":   (3.0, 2.0),
    "2x0.5": (2.0, 0.5),
}

DEFAULT_DPI = 203

# ── Style constants ───────────────────────────────────────────────────────────

FONT_STYLES   = ["standard", "enhanced", "impact", "serif", "narrow", "mono", "burbank"]
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

BORDER_STYLES = ["none", "thin", "thick", "double", "dashed", "rounded", "corners"] + _IMAGE_BORDERS
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

    # ── Themed ────────────────────────────────────────────────────────────────
    "windows95":  {"label": "🖥 Windows 95"},
    "blueprint":  {"label": "📐 Blueprint"},
    "warning":    {"label": "⚠ Warning"},
}

# Ordered groups for the UI dropdown — (group_label, [preset_keys])
# Use None as group_label to render ungrouped (no <optgroup> wrapper)
STYLE_PRESET_GROUPS = [
    (None,         ["none"]),
    ("Typography", ["minimal", "bold", "elegant", "retro"]),
    ("Layouts",    ["address", "price_tag", "cassette", "qr_code"]),
    ("Themed",     ["windows95", "blueprint", "warning"]),
]

# Fonts for the Windows 95 style (regular weight, not bold)
_WIN95_FONTS = [
    r"C:\Users\Steve\AppData\Local\Microsoft\Windows\Fonts\W95F.otf",  # W95FA pixel font
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
    "standard": 0.85,
    "enhanced": 0.90,
    "impact":   0.92,
    "serif":    0.85,
    "narrow":   0.92,
    "mono":     0.85,
    "burbank":  0.95,
}

_BURBANK_PATH = r"C:\Users\Steve\AppData\Local\Microsoft\Windows\Fonts\BurbankBigCondensed-Bold.otf"
_W95FA_PATH   = r"C:\Users\Steve\AppData\Local\Microsoft\Windows\Fonts\W95F.otf"

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
    "burbank": {
        "normal":      [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
        "bold":        [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
        "italic":      [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
        "bold_italic": [_BURBANK_PATH, r"C:\Windows\Fonts\impact.ttf"],
    },
}

# ── Icon keyword / emoji data (imported from emoji_data.py) ──────────────────
from emoji_data import _ICON_KEYWORDS, _ICON_EMOJIS   # noqa: E402

# Legacy copy kept for reference only — overridden by the import above.
_ICON_KEYWORDS_LEGACY = {
    # ── Ham Radio ────────────────────────────────────────────────────────────

    # Antenna / feedline / RF hardware → 📡
    "antenna":          "antenna",
    "antennas":         "antenna",
    "yagi":             "antenna",
    "beam":             "antenna",
    "dipole":           "antenna",
    "vertical":         "antenna",
    "wire antenna":     "antenna",
    "loop":             "antenna",
    "magnetic loop":    "antenna",
    "quad":             "antenna",
    "moxon":            "antenna",
    "coax":             "antenna",
    "coaxial":          "antenna",
    "feedline":         "antenna",
    "feed line":        "antenna",
    "pl-259":           "antenna",
    "so-239":           "antenna",
    "bnc":              "antenna",
    "n connector":      "antenna",
    "sma":              "antenna",
    "connector":        "antenna",
    "connectors":       "antenna",
    "balun":            "antenna",
    "choke":            "antenna",
    "ferrite":          "antenna",
    "counterpoise":     "antenna",
    "radials":          "antenna",
    "rotator":          "antenna",
    "rotor":            "antenna",
    "tower":            "antenna",
    "mast":             "antenna",
    "guy wire":         "antenna",
    "swr":              "antenna",
    "vswr":             "antenna",
    "dummy load":       "antenna",
    "rf":               "antenna",
    "feedthrough":      "antenna",
    "lightning arrestor": "antenna",

    # Radio / transceiver / operating gear → 📻
    "radio":            "radio",
    "ham radio":        "radio",
    "transceiver":      "radio",
    "rig":              "radio",
    "hf":               "radio",
    "vhf":              "radio",
    "uhf":              "radio",
    "handheld":         "radio",
    "ht":               "radio",
    "walkie talkie":    "radio",
    "receiver":         "radio",
    "transmitter":      "radio",
    "sdr":              "radio",
    "scanner":          "radio",
    "repeater":         "radio",
    "shack":            "radio",
    "amplifier":        "radio",
    "linear":           "radio",
    "power supply":     "radio",
    "antenna tuner":    "radio",
    "atu":              "radio",
    "tuner":            "radio",
    "microphone":       "radio",
    "headset":          "radio",
    "keyer":            "radio",
    "paddle":           "radio",
    "morse key":        "radio",
    "cw":               "radio",
    "morse":            "radio",
    "logbook":          "radio",
    "log book":         "radio",
    "qsl":              "radio",
    "qso":              "radio",
    "dx":               "radio",
    "dxing":            "radio",
    "contest":          "radio",
    "field day":        "radio",
    "emcomm":           "radio",
    "ares":             "radio",
    "races":            "radio",
    "aprs":             "radio",
    "packet":           "radio",
    "tnc":              "radio",
    "ft8":              "radio",
    "ft4":              "radio",
    "wspr":             "radio",
    "psk31":            "radio",
    "rtty":             "radio",
    "dstar":            "radio",
    "dmr":              "radio",
    "fusion":           "radio",
    "wires-x":          "radio",
    "allstar":          "radio",
    "echolink":         "radio",
    "40m":              "radio",
    "20m":              "radio",
    "80m":              "radio",
    "160m":             "radio",
    "10m":              "radio",
    "6m":               "radio",
    "2m":               "radio",
    "70cm":             "radio",
    "callsign":         "radio",
    "propagation":      "radio",
    "grounding":        "radio",
    "ground":           "radio",
    "rf ground":        "radio",

    # Warning / fragile
    "fragile":          "warning",
    "glass":            "warning",
    "breakable":        "warning",
    "handle with care": "warning",
    "caution":          "warning",
    "careful":          "warning",
    "danger":           "warning",
    "hazard":           "warning",
    "warning":          "warning",
    "alert":            "warning",
    "toxic":            "warning",
    "poison":           "warning",
    "do not drop":      "warning",
    "unsafe":           "warning",
    "risk":             "warning",

    # Cold / frozen / winter
    "cold":             "snowflake",
    "frozen":           "snowflake",
    "freeze":           "snowflake",
    "refrigerate":      "snowflake",
    "keep cold":        "snowflake",
    "keep frozen":      "snowflake",
    "ice":              "snowflake",
    "chill":            "snowflake",
    "winter":           "snowflake",
    "snow":             "snowflake",
    "blizzard":         "snowflake",
    "frost":            "snowflake",
    "freezer":          "snowflake",
    "icy":              "snowflake",
    "arctic":           "snowflake",
    "glacier":          "snowflake",
    "chilled":          "snowflake",
    "december":         "snowflake",
    "january":          "snowflake",
    "february":         "snowflake",

    # Summer / sun
    "summer":           "summer",
    "sun":              "summer",
    "sunny":            "summer",
    "sunshine":         "summer",
    "beach":            "summer",
    "pool":             "summer",
    "june":             "summer",
    "july":             "summer",
    "august":           "summer",
    "tropical":         "summer",
    "swimsuit":         "summer",
    "sunscreen":        "summer",
    "outdoor":          "summer",

    # Fall / autumn
    "fall":             "autumn",
    "autumn":           "autumn",
    "leaves":           "autumn",
    "harvest":          "autumn",
    "october":          "autumn",
    "november":         "autumn",
    "september":        "autumn",
    "pumpkin":          "autumn",
    "maple":            "autumn",
    "acorn":            "autumn",

    # Spring
    "spring":           "spring",
    "flowers":          "spring",
    "bloom":            "spring",
    "garden":           "spring",
    "seeds":            "spring",
    "planting":         "spring",
    "april":            "spring",
    "march":            "spring",
    "easter":           "spring",
    "rain":             "spring",
    "fresh":            "spring",
    "blossom":          "spring",

    # Electric / tech
    "electric":         "lightning",
    "electronics":      "lightning",
    "battery":          "lightning",
    "charger":          "lightning",
    "power":            "lightning",
    "wires":            "lightning",
    "cord":             "lightning",
    "plug":             "lightning",
    "outlet":           "lightning",
    "extension cord":   "lightning",
    "generator":        "lightning",
    "solar":            "lightning",
    "voltage":          "lightning",

    # Kitchen / cooking
    "kitchen":          "kitchen",
    "cooking":          "kitchen",
    "spices":           "kitchen",
    "utensils":         "kitchen",
    "pots":             "kitchen",
    "pans":             "kitchen",
    "bakeware":         "kitchen",
    "cutlery":          "kitchen",
    "cookware":         "kitchen",
    "appliances":       "kitchen",

    # Bedroom / sleep
    "bedroom":          "bedroom",
    "bed":              "bedroom",
    "sleep":            "bedroom",
    "pillow":           "bedroom",
    "blanket":          "bedroom",
    "linens":           "bedroom",
    "mattress":         "bedroom",
    "sheets":           "bedroom",
    "duvet":            "bedroom",
    "comforter":        "bedroom",
    "quilt":            "bedroom",
    "nightstand":       "bedroom",

    # Bathroom
    "bathroom":         "bathroom",
    "bath":             "bathroom",
    "shower":           "bathroom",
    "toilet":           "bathroom",
    "towel":            "bathroom",
    "sink":             "bathroom",
    "soap":             "bathroom",
    "shampoo":          "bathroom",
    "conditioner":      "bathroom",
    "toothbrush":       "bathroom",
    "hygiene":          "bathroom",
    "grooming":         "bathroom",
    "skincare":         "bathroom",

    # Books / office
    "book":             "books",
    "books":            "books",
    "library":          "books",
    "reading":          "books",
    "documents":        "books",
    "files":            "books",
    "paperwork":        "books",
    "office":           "books",
    "school":           "books",
    "notebook":         "books",
    "journal":          "books",
    "notes":            "books",
    "study":            "books",
    "homework":         "books",
    "textbook":         "books",
    "manual":           "books",
    "instructions":     "books",
    "magazine":         "books",
    "binder":           "books",
    "folder":           "books",

    # Tools / garage
    "tools":            "tools",
    "garage":           "tools",
    "hardware":         "tools",
    "workshop":         "tools",
    "repair":           "tools",
    "hammer":           "tools",
    "screwdriver":      "tools",
    "drill":            "tools",
    "wrench":           "tools",
    "pliers":           "tools",
    "saw":              "tools",
    "nails":            "tools",
    "screws":           "tools",
    "bolts":            "tools",
    "nuts":             "tools",
    "sandpaper":        "tools",
    "painting supplies":"tools",
    "plumbing":         "tools",

    # Medicine / health
    "bandages":         "firstaid",
    "first aid":        "firstaid",
    "band-aid":         "firstaid",
    "wound":            "firstaid",
    "injury":           "firstaid",
    "medicine":         "medicine",
    "medication":       "medicine",
    "pharmacy":         "medicine",
    "health":           "medicine",
    "vitamins":         "medicine",
    "pills":            "medicine",
    "supplements":      "medicine",
    "prescription":     "medicine",
    "medical":          "medicine",

    # Mail / shipping
    "mail":             "mail",
    "letter":           "mail",
    "envelope":         "mail",
    "shipping":         "mail",
    "return":           "mail",
    "send":             "mail",
    "package":          "mail",
    "postage":          "mail",
    "parcel":           "mail",
    "outgoing":         "mail",
    "incoming":         "mail",

    # Money / finance
    "money":            "money",
    "cash":             "money",
    "bills":            "money",
    "finance":          "money",
    "receipt":          "money",
    "invoice":          "money",
    "taxes":            "money",
    "budget":           "money",
    "savings":          "money",
    "wallet":           "money",
    "coins":            "money",
    "bank":             "money",

    # Music — specific instruments first
    "guitar":           "guitar",
    "acoustic":         "guitar",
    "electric guitar":  "guitar",
    "bass guitar":      "guitar",
    "ukulele":          "guitar",
    "piano":            "piano",
    "keyboard":         "piano",
    "organ":            "piano",
    "synthesizer":      "piano",
    "drums":            "drums",
    "drumkit":          "drums",
    "percussion":       "drums",
    "trumpet":          "trumpet",
    "trombone":         "trumpet",
    "horn":             "trumpet",
    "violin":           "violin",
    "cello":            "violin",
    "viola":            "violin",
    "fiddle":           "violin",
    "microphone":       "microphone",
    "singing":          "microphone",
    "vocals":           "microphone",
    "mic":              "microphone",
    "karaoke":          "microphone",
    "music":            "music",
    "records":          "music",
    "vinyl":            "music",
    "headphones":       "music",
    "speakers":         "music",
    "amp":              "music",
    "studio":           "music",
    "playlist":         "music",
    "album":            "music",

    # Sports — specific first, generic fallback last
    "baseball":         "baseball",
    "softball":         "baseball",
    "basketball":       "basketball",
    "football":         "football",
    "nfl":              "football",
    "soccer":           "sports",
    "tennis":           "tennis",
    "pickleball":       "tennis",
    "golf":             "golf",
    "bowling":          "bowling",
    "volleyball":       "volleyball",
    "skiing":           "skiing",
    "snowboarding":     "skiing",
    "swimming":         "swimming",
    "cycling":          "cycling",
    "biking":           "cycling",
    "boxing":           "boxing",
    "mma":              "boxing",
    "wrestling":        "boxing",
    "running":          "running",
    "jogging":          "running",
    "marathon":         "running",
    "yoga":             "yoga",
    "pilates":          "yoga",
    "gym":              "gym",
    "weights":          "gym",
    "weightlifting":    "gym",
    "fitness":          "gym",
    "workout":          "gym",
    "exercise":         "gym",
    "camping":          "camping",
    "hiking":           "camping",
    "backpacking":      "camping",
    "surfing":          "surfing",
    "skateboarding":    "surfing",
    "karate":           "martial_arts",
    "martial arts":     "martial_arts",
    "judo":             "martial_arts",
    "taekwondo":        "martial_arts",
    "hockey":           "sports",
    "sports":           "sports",

    # Trash / recycle
    "trash":            "trash",
    "garbage":          "trash",
    "recycle":          "trash",
    "junk":             "trash",
    "dispose":          "trash",
    "donate":           "trash",
    "waste":            "trash",
    "discard":          "trash",
    "toss":             "trash",
    "throw away":       "trash",

    # Hot / fire
    "hot":              "fire",
    "fire":             "fire",
    "heat":             "fire",
    "warm":             "fire",
    "spicy":            "fire",
    "candles":          "fire",
    "matches":          "fire",
    "lighter":          "fire",
    "flammable":        "fire",

    # Camera / photos
    "photos":           "camera",
    "pictures":         "camera",
    "camera":           "camera",
    "memories":         "camera",
    "photography":      "camera",
    "prints":           "camera",
    "negatives":        "camera",
    "albums":           "camera",
    "videos":           "camera",
    "footage":          "camera",

    # Clothes
    "clothes":          "clothes",
    "clothing":         "clothes",
    "shirts":           "clothes",
    "pants":            "clothes",
    "jackets":          "clothes",
    "laundry":          "clothes",
    "wardrobe":         "clothes",
    "shoes":            "clothes",
    "socks":            "clothes",
    "underwear":        "clothes",
    "dresses":          "clothes",
    "suits":            "clothes",
    "coats":            "clothes",
    "hats":             "clothes",
    "accessories":      "clothes",
    "uniforms":         "clothes",
    "seasonal clothes": "clothes",

    # Holidays — specific emojis per occasion
    "christmas":        "christmas",
    "xmas":             "christmas",
    "ornaments":        "christmas",
    "halloween":        "halloween",
    "trick or treat":   "halloween",
    "costumes":         "halloween",
    "birthday":         "birthday",
    "cake":             "birthday",
    "graduation":       "graduation",
    "graduate":         "graduation",
    "diploma":          "graduation",
    "wedding":          "wedding",
    "bride":            "wedding",
    "groom":            "wedding",
    "anniversary":      "wedding",
    "valentine":        "valentine",
    "valentines":       "valentine",
    "thanksgiving":     "thanksgiving",
    "turkey":           "thanksgiving",
    "gift":             "gift",
    "gifts":            "gift",
    "presents":         "gift",
    "wrapping":         "gift",
    "party":            "gift",
    "celebration":      "gift",
    "holiday":          "gift",
    "decorations":      "gift",
    "seasonal":         "gift",
    "lights":           "gift",

    # Baby / kids
    "baby":             "baby",
    "kids":             "baby",
    "children":         "baby",
    "toys":             "baby",
    "diapers":          "baby",
    "infant":           "baby",
    "toddler":          "baby",
    "nursery":          "baby",
    "stroller":         "baby",
    "formula":          "baby",
    "wipes":            "baby",
    "playroom":         "baby",
    "backpack":         "baby",
    "school supplies":  "baby",

    # Pets — specific animals first
    "dog":              "dog",
    "puppy":            "dog",
    "dogs":             "dog",
    "cat":              "cat",
    "kitten":           "cat",
    "cats":             "cat",
    "bird":             "bird",
    "parakeet":         "bird",
    "canary":           "bird",
    "fish":             "fish",
    "aquarium":         "fish",
    "tank":             "fish",
    "rabbit":           "rabbit",
    "bunny":            "rabbit",
    "hamster":          "hamster",
    "guinea pig":       "hamster",
    "gerbil":           "hamster",
    "snake":            "snake",
    "turtle":           "turtle",
    "tortoise":         "turtle",
    "lizard":           "lizard",
    "gecko":            "lizard",
    "iguana":           "lizard",
    "parrot":           "parrot",
    "cockatiel":        "parrot",
    "macaw":            "parrot",
    "pet":              "pet",
    "animal":           "pet",
    "pet food":         "pet",
    "pet supplies":     "pet",
    "treats":           "pet",
    "leash":            "pet",
    "collar":           "pet",
    "litter":           "pet",
    "kennel":           "pet",

    # Gaming
    "chess":            "chess",
    "checkers":         "chess",
    "games":            "gaming",
    "gaming":           "gaming",
    "console":          "gaming",
    "controller":       "gaming",
    "playstation":      "gaming",
    "xbox":             "gaming",
    "nintendo":         "gaming",
    "pc gaming":        "gaming",
    "steam":            "gaming",
    "boardgames":       "gaming",
    "cards":            "gaming",
    "dice":             "gaming",

    # Art / craft
    "art":              "art",
    "craft":            "art",
    "paint":            "art",
    "drawing":          "art",
    "supplies":         "art",
    "brushes":          "art",
    "canvas":           "art",
    "sketchbook":       "art",
    "markers":          "art",
    "colored pencils":  "art",
    "yarn":             "art",
    "knitting":         "art",
    "sewing":           "art",
    "fabric":           "art",
    "scrapbook":        "art",

    # Food / dining
    "food":             "food",
    "lunch":            "food",
    "dinner":           "food",
    "breakfast":        "food",
    "snacks":           "food",
    "groceries":        "food",
    "meal prep":        "food",
    "leftovers":        "food",
    "recipe":           "food",
    "baking":           "food",
    "pantry":           "food",

    # Drinks / coffee
    "coffee":           "coffee",
    "tea":              "coffee",
    "drinks":           "coffee",
    "beverages":        "coffee",
    "mugs":             "coffee",
    "espresso":         "coffee",
    "cafe":             "coffee",

    # Travel
    "travel":           "travel",
    "vacation":         "travel",
    "trip":             "travel",
    "flight":           "travel",
    "luggage":          "travel",
    "passport":         "travel",
    "suitcase":         "travel",
    "hotel":            "travel",
    "abroad":           "travel",

    # Home / house
    "home":             "home",
    "house":            "home",
    "living room":      "home",
    "dining room":      "home",
    "basement":         "home",
    "attic":            "home",
    "closet":           "home",
    "storage":          "home",
    "moving":           "home",

    # Cleaning / chores
    "cleaning":         "cleaning",
    "clean":            "cleaning",
    "chores":           "cleaning",
    "supplies":         "cleaning",
    "mop":              "cleaning",
    "vacuum":           "cleaning",
    "laundry":          "cleaning",
    "detergent":        "cleaning",
    "bleach":           "cleaning",
    "broom":            "cleaning",

    # Car / automotive
    "car":              "car",
    "auto":             "car",
    "automotive":       "car",
    "vehicle":          "car",
    "truck":            "car",
    "oil":              "car",
    "tires":            "car",
    "motor":            "car",
    "engine":           "car",
    "parts":            "car",

    # Lock / security / private
    "private":          "lock",
    "confidential":     "lock",
    "secure":           "lock",
    "locked":           "lock",
    "password":         "lock",
    "secret":           "lock",
    "do not open":      "lock",
    "personal":         "lock",
    "sensitive":        "lock",

    # Star / important / favorite
    "important":        "star",
    "priority":         "star",
    "favorite":         "star",
    "urgent":           "star",
    "vip":              "star",
    "featured":         "star",
    "top":              "star",
    "best":             "star",

    # Time / schedule / clock
    "time":             "time",
    "clock":            "time",
    "timer":            "time",
    "alarm":            "time",
    "watch":            "time",
    "schedule":         "time",
    "deadline":         "time",
    "appointment":      "time",
    "reminder":         "time",
    "due":              "time",
    "weekly":           "time",
    "daily":            "time",
    "monthly":          "time",
    "calendar":         "time",
    "countdown":        "time",
    "date":             "time",
    "annual":           "time",
    "hourly":           "time",
    "stopwatch":        "time",
    "hourglass":        "time",

    # Phone / contact
    "phone":            "phone",
    "contact":          "phone",
    "call":             "phone",
    "mobile":           "phone",
    "telephone":        "phone",
    "number":           "phone",
    "cell":             "phone",
    "smartphone":       "phone",
    "iphone":           "phone",
    "android":          "phone",
    "text":             "phone",
    "voicemail":        "phone",

    # Science / lab
    "science":          "science",
    "lab":              "science",
    "experiment":       "science",
    "chemistry":        "science",
    "research":         "science",
    "samples":          "science",
    "specimens":        "science",
    "biology":          "science",
    "physics":          "science",
    "astronomy":        "science",
    "geology":          "science",
    "laboratory":       "science",
    "data":             "science",
    "analysis":         "science",

    # Recycle / eco / green
    "eco":              "recycle",
    "green":            "recycle",
    "compost":          "recycle",
    "biodegradable":    "recycle",
    "reusable":         "recycle",
    "sustainable":      "recycle",
    "recycle":          "recycle",
    "recyclable":       "recycle",
    "environment":      "recycle",
    "conservation":     "recycle",
    "zero waste":       "recycle",
    "organic waste":    "recycle",
    "cardboard":        "recycle",
    "aluminum":         "recycle",

    # Computer / tech
    "computer":         "computer",
    "laptop":           "computer",
    "tech":             "computer",
    "software":         "computer",
    "server":           "computer",
    "backup":           "computer",
    "hard drive":       "computer",
    "usb":              "computer",
    "keyboard":         "computer",
    "monitor":          "computer",
    "desktop":          "computer",
    "tablet":           "computer",
    "ipad":             "computer",
    "programming":      "computer",
    "coding":           "computer",
    "developer":        "computer",
    "wifi":             "computer",
    "network":          "computer",
    "router":           "computer",
    "internet":         "computer",

    # Star / important / favorite
    "important":        "star",
    "priority":         "star",
    "favorite":         "star",
    "vip":              "star",
    "featured":         "star",
    "top":              "star",
    "best":             "star",
    "highlighted":      "star",
    "special":          "star",
    "premium":          "star",
    "number one":       "star",
    "winner":           "star",
    "award":            "star",
    "gold":             "star",

    # Lock / security / private
    "private":          "lock",
    "confidential":     "lock",
    "secure":           "lock",
    "locked":           "lock",
    "password":         "lock",
    "secret":           "lock",
    "do not open":      "lock",
    "personal":         "lock",
    "sensitive":        "lock",
    "classified":       "lock",
    "restricted":       "lock",
    "protected":        "lock",
    "safe":             "lock",
    "vault":            "lock",
    "do not touch":     "lock",

    # Travel
    "travel":           "travel",
    "vacation":         "travel",
    "trip":             "travel",
    "flight":           "travel",
    "luggage":          "travel",
    "passport":         "travel",
    "suitcase":         "travel",
    "hotel":            "travel",
    "abroad":           "travel",
    "cruise":           "travel",
    "road trip":        "travel",
    "backpacking":      "travel",
    "tourism":          "travel",
    "itinerary":        "travel",
    "boarding":         "travel",
    "international":    "travel",

    # Home / house / moving
    "home":             "home",
    "house":            "home",
    "living room":      "home",
    "dining room":      "home",
    "basement":         "home",
    "attic":            "home",
    "closet":           "home",
    "storage":          "home",
    "moving":           "home",
    "guest room":       "home",
    "patio":            "home",
    "furniture":        "home",
    "decor":            "home",

    # Cleaning / chores
    "cleaning":         "cleaning",
    "clean":            "cleaning",
    "chores":           "cleaning",
    "mop":              "cleaning",
    "vacuum":           "cleaning",
    "detergent":        "cleaning",
    "bleach":           "cleaning",
    "broom":            "cleaning",
    "sponge":           "cleaning",
    "disinfect":        "cleaning",
    "sanitize":         "cleaning",
    "organize":         "cleaning",
    "declutter":        "cleaning",
    "tidy":             "cleaning",
    "windex":           "cleaning",
    "scrub":            "cleaning",

    # Car / automotive
    "car":              "car",
    "auto":             "car",
    "automotive":       "car",
    "vehicle":          "car",
    "truck":            "car",
    "oil":              "car",
    "tires":            "car",
    "motor":            "car",
    "engine":           "car",
    "van":              "car",
    "suv":              "car",
    "gas":              "car",
    "fuel":             "car",
    "brakes":           "car",
    "transmission":     "car",
    "windshield":       "car",
    "registration":     "car",
    "insurance":        "car",
    "maintenance":      "car",
    "detailing":        "car",

    # Food — specific first
    "pizza":            "pizza",
    "cookies":          "cookies",
    "cookie":           "cookies",
    "bread":            "bread",
    "sourdough":        "bread",
    "rolls":            "bread",
    "breakfast":        "breakfast",
    "eggs":             "breakfast",
    "pancakes":         "breakfast",
    "waffles":          "breakfast",
    "lunch":            "food",
    "dinner":           "food",
    "snacks":           "food",
    "groceries":        "food",
    "meal prep":        "food",
    "leftovers":        "food",
    "recipe":           "food",
    "baking":           "food",
    "brunch":           "food",
    "dessert":          "food",
    "pasta":            "food",
    "soup":             "food",
    "salad":            "food",
    "sandwich":         "food",
    "meal":             "food",
    "snack":            "food",
    "treat":            "food",

    # Coffee / drinks
    "coffee":           "coffee",
    "tea":              "coffee",
    "drinks":           "coffee",
    "beverages":        "coffee",
    "mugs":             "coffee",
    "espresso":         "coffee",
    "cafe":             "coffee",
    "latte":            "coffee",
    "cappuccino":       "coffee",
    "chai":             "coffee",
    "hot chocolate":    "coffee",
    "juice":            "coffee",
    "smoothie":         "coffee",
    "water":            "coffee",
    "thermos":          "coffee",

    # Music (additions) — violin/trumpet/microphone/singing/radio kept above with specific icons
    "saxophone":        "music",
    "choir":            "music",
    "band":             "music",
    "concert":          "music",
    "podcast":          "music",

    # Sports (additions) — specific-icon sports kept above; new ones added here
    "hockey":           "sports",
    "climbing":         "sports",

    # Fire (additions)
    "fireplace":        "fire",
    "campfire":         "fire",
    "barbecue":         "fire",
    "grill":            "fire",
    "bbq":              "fire",
    "stove":            "fire",
    "oven":             "fire",
    "furnace":          "fire",

    # Camera (additions)
    "film":             "camera",
    "slides":           "camera",
    "portraits":        "camera",
    "digital":          "camera",
    "screenshot":       "camera",
    "video":            "camera",
    "recording":        "camera",
    "footage":          "camera",
    "wedding photos":   "camera",
    "vacation photos":  "camera",

    # Clothes (additions)
    "sweaters":         "clothes",
    "hoodies":          "clothes",
    "jeans":            "clothes",
    "shorts":           "clothes",
    "skirts":           "clothes",
    "ties":             "clothes",
    "belts":            "clothes",
    "gloves":           "clothes",
    "scarves":          "clothes",
    "boots":            "clothes",
    "sneakers":         "clothes",
    "swimwear":         "clothes",

    # Holiday (additions) — valentine/graduation/anniversary/wedding kept above with specific icons
    "new year":         "gift",
    "hanukkah":         "gift",
    "festive":          "gift",
    "fourth of july":   "gift",

    # Baby (additions)
    "preschool":        "baby",
    "daycare":          "baby",
    "bottle":           "baby",
    "pacifier":         "baby",
    "crib":             "baby",
    "highchair":        "baby",
    "playpen":          "baby",

    # Pet (additions) — specific animals kept above; new care/housing terms here
    "vet":              "pet",
    "flea":             "pet",
    "crate":            "pet",
    "cage":             "pet",

    # Gaming (additions) — chess kept above with specific icon
    "retro":            "gaming",
    "arcade":           "gaming",
    "lego":             "gaming",
    "puzzle":           "gaming",
    "poker":            "gaming",

    # Art (additions)
    "watercolor":       "art",
    "sculpture":        "art",
    "pottery":          "art",
    "ceramics":         "art",
    "origami":          "art",
    "jewelry":          "art",
    "embroidery":       "art",
    "crochet":          "art",
    "quilting":         "art",
    "woodworking":      "art",

    # Money (additions)
    "budget":           "money",
    "savings":          "money",
    "wallet":           "money",
    "coins":            "money",
    "bank":             "money",
    "paycheck":         "money",
    "expense":          "money",
    "payment":          "money",
    "checks":           "money",
    "checkbook":        "money",
    "credit":           "money",
    "debit":            "money",

    # Mail (additions)
    "package":          "mail",
    "postage":          "mail",
    "parcel":           "mail",
    "delivery":         "mail",
    "courier":          "mail",
    "outgoing":         "mail",
    "incoming":         "mail",
}

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
        preset = STYLE_PRESETS.get(style_preset, {})
        font_style = preset.get("font_style", font_style)
        border     = preset.get("border",     border)
        text_case  = preset.get("text_case",  text_case)
        icons      = preset.get("icons",      icons)

    img  = Image.new("RGB", (w_px, h_px), "white")
    draw = ImageDraw.Draw(img)

    pad  = max(4, int(min(w_px, h_px) * 0.05))

    # Push content inward so it never overlaps the border
    _border_inset = {"thin": 4, "thick": 8, "double": 14, "dashed": 4, "rounded": 6, "corners": 4}
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
        icon_size = int(h_px * 0.55)
        icon_x    = pad
        icon_y    = (h_px - icon_size) // 2
        text_x0   = icon_x + icon_size + pad
    else:
        text_x0   = pad

    text_area_w = w_px - text_x0 - pad
    text_area_h = h_px - pad * 2

    fill    = _FILL.get(font_style, 0.85)
    wrapped, font = _fit_text(text, text_area_w, text_area_h, font_style, fill, font_weight)
    joined  = "\n".join(wrapped)

    bb = draw.multiline_textbbox((0, 0), joined, font=font, align="center")
    x  = text_x0 + (text_area_w - (bb[2] - bb[0])) / 2 - bb[0]
    y  = (h_px - (bb[3] - bb[1])) / 2 - bb[1]
    draw.multiline_text((x, y), joined, fill="black", font=font, align="center")

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

    width_in, height_in = LABEL_SIZES[size_key]
    img = render_label(text, width_in, height_in, dpi, font_style, border, icons, text_case, style_preset, font_weight, qr_show_text)

    dm_buf  = _get_devmode_buf(printer_name, width_in, height_in)

    # Try with custom DEVMODE (correct paper size); fall back to driver default
    hdc_raw = None
    if dm_buf is not None:
        hdc_raw = _gdi32.CreateDCW("WINSPOOL", printer_name, None, dm_buf)
    if not hdc_raw:
        hdc_raw = _gdi32.CreateDCW("WINSPOOL", printer_name, None, None)
    if not hdc_raw:
        err = ctypes.GetLastError()
        raise RuntimeError(f"CreateDC failed (Windows error {err}) — check printer name and driver")

    hDC = win32ui.CreateDCFromHandle(hdc_raw)

    off_x    = hDC.GetDeviceCaps(112)
    off_y    = hDC.GetDeviceCaps(113)
    dpi_x    = hDC.GetDeviceCaps(88)
    dpi_y    = hDC.GetDeviceCaps(90)
    target_w = int(width_in  * dpi_x)
    target_h = int(height_in * dpi_y)

    hDC.StartDoc("Label")
    hDC.StartPage()
    bmp = ImageWin.Dib(img)
    bmp.draw(hDC.GetHandleOutput(),
             (-off_x, -off_y, target_w - off_x, target_h - off_y))
    hDC.EndPage()
    hDC.EndDoc()
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

    words = display_text.split()
    max_n = max(1, (len(words) + 2) // 3)
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
    _border_inset = {"thin": 4, "thick": 8, "double": 14, "dashed": 4, "rounded": 6, "corners": 4}
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
    _draw_icon(img, "warning", icon_lx, icon_ly, icon_sz, color=WHITE)

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
    words = display_text.split()
    max_n = max(1, (len(words) + 2) // 3)
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
    return " ".join(_cap(w) for w in text.split())


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

    words = display_text.split()
    max_n = max(1, (len(words) + 2) // 3)
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

    words = display_text.split()
    max_n = max(1, (len(words) + 2) // 3)
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
    GRID = (255, 255, 255)  # pure white — guaranteed uninked lines on thermal

    img  = Image.new("RGB", (w_px, h_px), BG)
    draw = ImageDraw.Draw(img)

    # Grid — pure white 2px lines so they print as definite uninked stripes
    step = max(round(dpi * 0.22), 16)
    for gx in range(step, w_px, step):
        draw.line([(gx, 0), (gx, h_px)], fill=GRID, width=2)
    for gy in range(step, h_px, step):
        draw.line([(0, gy), (w_px, gy)], fill=GRID, width=2)

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

    words = display_text.split()
    max_n = max(1, (len(words) + 2) // 3)
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
    words        = display_text.split()
    max_n        = max(1, (len(words) + 1) // 2)
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


# ── Text fitting ──────────────────────────────────────────────────────────────

def _fit_text(text, max_w, max_h, font_style="standard", fill=0.85, font_weight="bold"):
    font_path = _find_font_path(font_style, font_weight)
    words     = text.split()
    # Aim for at least ~3 words per line — stops single-word lines winning the
    # "biggest font" contest just because one short word fits a huge size.
    # (len+2)//3 is ceiling(len/3): 1-3 words→1 line, 4-6→2, 7-9→3, etc.
    max_n      = max(1, (len(words) + 2) // 3)
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
    scratch   = Image.new("RGB", (max_w * 2, max_h * 2))
    draw      = ImageDraw.Draw(scratch)
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

# ── Icon detection & drawing ──────────────────────────────────────────────────

# Legacy emoji dict — overridden by emoji_data import above.
_ICON_EMOJIS_LEGACY = {
    # Warning / safety
    "warning":      "⚠",
    "snowflake":    "❄",
    "lightning":    "⚡",
    # Seasons
    "summer":       "\U00002600",   # ☀
    "autumn":       "\U0001F342",   # 🍂
    "spring":       "\U0001F338",   # 🌸
    # Home / rooms
    "kitchen":      "\U0001F374",   # 🍴
    "bedroom":      "\U0001F6CF",   # 🛏
    "bathroom":     "\U0001F6BF",   # 🚿
    "home":         "\U0001F3E0",   # 🏠
    # Work / study
    "books":        "\U0001F4DA",   # 📚
    "tools":        "\U0001F527",   # 🔧
    "computer":     "\U0001F4BB",   # 💻
    "science":      "\U0001F9EA",   # 🧪
    # Health
    "medicine":     "\U0001F48A",   # 💊
    "firstaid":     "\U0001FA79",   # 🩹
    # Communication
    "mail":         "\U0001F4E7",   # 📧
    "phone":        "\U0001F4F1",   # 📱
    # Finance
    "money":        "\U0001F4B0",   # 💰
    # Music — specific instruments
    "music":        "\U0001F3B5",   # 🎵 (generic)
    "guitar":       "\U0001F3B8",   # 🎸
    "piano":        "\U0001F3B9",   # 🎹
    "drums":        "\U0001F941",   # 🥁
    "trumpet":      "\U0001F3BA",   # 🎺
    "violin":       "\U0001F3BB",   # 🎻
    "microphone":   "\U0001F3A4",   # 🎤
    # Sports — specific
    "sports":       "\U000026BD",   # ⚽ (generic / soccer)
    "baseball":     "\U000026BE",   # ⚾
    "basketball":   "\U0001F3C0",   # 🏀
    "football":     "\U0001F3C8",   # 🏈
    "tennis":       "\U0001F3BE",   # 🎾
    "golf":         "\U000026F3",   # ⛳
    "bowling":      "\U0001F3B3",   # 🎳
    "volleyball":   "\U0001F3D0",   # 🏐
    "skiing":       "\U0001F3BF",   # 🎿
    "swimming":     "\U0001F3CA",   # 🏊
    "cycling":      "\U0001F6B4",   # 🚴
    "boxing":       "\U0001F94A",   # 🥊
    "running":      "\U0001F3C3",   # 🏃
    "yoga":         "\U0001F9D8",   # 🧘
    "gym":          "\U0001F3CB",   # 🏋
    "camping":      "\U000026FA",   # ⛺
    "surfing":      "\U0001F3C4",   # 🏄
    "martial_arts": "\U0001F94B",   # 🥋
    # Misc activity
    "trash":        "\U0001F5D1",   # 🗑
    "fire":         "\U0001F525",   # 🔥
    "camera":       "\U0001F4F7",   # 📷
    "clothes":      "\U0001F455",   # 👕
    # Holidays — specific
    "christmas":    "\U0001F384",   # 🎄
    "halloween":    "\U0001F383",   # 🎃
    "birthday":     "\U0001F382",   # 🎂
    "graduation":   "\U0001F393",   # 🎓
    "wedding":      "\U0001F492",   # 💒
    "valentine":    "\U0001F49D",   # 💝
    "thanksgiving": "\U0001F983",   # 🦃
    "gift":         "\U0001F381",   # 🎁 (generic gifts/presents)
    # Pets — specific
    "pet":          "\U0001F43E",   # 🐾 (generic)
    "dog":          "\U0001F415",   # 🐕
    "cat":          "\U0001F408",   # 🐈
    "bird":         "\U0001F426",   # 🐦
    "fish":         "\U0001F420",   # 🐠
    "rabbit":       "\U0001F430",   # 🐰
    "hamster":      "\U0001F439",   # 🐹
    "snake":        "\U0001F40D",   # 🐍
    "turtle":       "\U0001F422",   # 🐢
    "parrot":       "\U0001F99C",   # 🦜
    "lizard":       "\U0001F98E",   # 🦎
    # Gaming
    "gaming":       "\U0001F3AE",   # 🎮
    "chess":        "\U0000265F",   # ♟
    # Art
    "art":          "\U0001F3A8",   # 🎨
    # Food — generic + specific
    "food":         "\U0001F37D",   # 🍽
    "pizza":        "\U0001F355",   # 🍕
    "birthday_cake":"\U0001F382",   # 🎂
    "cookies":      "\U0001F36A",   # 🍪
    "bread":        "\U0001F35E",   # 🍞
    "breakfast":    "\U0001F373",   # 🍳
    "coffee":       "\U00002615",   # ☕
    # Travel / transport
    "travel":       "\U00002708",   # ✈
    "car":          "\U0001F697",   # 🚗
    # Other
    "cleaning":     "\U0001F9F9",   # 🧹
    "lock":         "\U0001F512",   # 🔒
    "star":         "\U00002B50",   # ⭐
    "time":         "\U000023F0",   # ⏰
    "recycle":      "\U0000267B",   # ♻
    "baby":         "\U0001F476",   # 👶
    # Ham radio
    "radio":        "\U0001F4FB",   # 📻
    "antenna":      "\U0001F4E1",   # 📡
}

# Emoji font paths — first one found wins
_EMOJI_FONT_PATHS = [
    r"C:\Windows\Fonts\seguiemj.ttf",   # Segoe UI Emoji (Windows 10/11)
    r"C:\Windows\Fonts\seguisym.ttf",   # Segoe UI Symbol (fallback)
]


def _detect_icon(text: str):
    lower = text.lower()
    for keyword, icon in _ICON_KEYWORDS.items():
        k = re.escape(keyword)
        # 1. Exact word-boundary match  ("wrench", "sharks")
        if re.search(r'\b' + k + r'\b', lower):
            return icon
        if ' ' not in keyword:
            # 2. Forward — singular keyword, plural text
            #    -s / -es:  shark→sharks, wrench→wrenches, tomato→tomatoes
            if re.search(r'\b' + k + r'e?s\b', lower):
                return icon
            #    -y → -ies:  butterfly→butterflies
            if keyword.endswith('y') and re.search(
                    r'\b' + re.escape(keyword[:-1]) + r'ies\b', lower):
                return icon
            #    -fe → -ves:  knife→knives
            if keyword.endswith('fe') and re.search(
                    r'\b' + re.escape(keyword[:-2]) + r'ves\b', lower):
                return icon
            #    -f → -ves:  leaf→leaves, wolf→wolves
            elif keyword.endswith('f') and re.search(
                    r'\b' + re.escape(keyword[:-1]) + r'ves\b', lower):
                return icon
            # 3. Reverse — plural keyword, singular text
            #    -s:   "screws" keyword matches "screw" in text
            #    also handles "bees"→"bee", "nails"→"nail", "tools"→"tool", etc.
            if keyword.endswith('s') and len(keyword) > 3 and re.search(
                    r'\b' + re.escape(keyword[:-1]) + r'\b', lower):
                return icon
    return None


def _draw_icon(img, icon_type, x, y, size, color=(0, 0, 0)):
    """Render an emoji into a temp image, crop to actual ink, then paste into img."""
    emoji = _ICON_EMOJIS.get(icon_type)
    if not emoji:
        return

    font_path = next((p for p in _EMOJI_FONT_PATHS if os.path.exists(p)), None)
    if not font_path:
        return

    # Render onto a large temp canvas (grayscale, white bg) to find true ink bounds
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

    # Draw centered on the temp canvas
    cx, cy = canvas // 2, canvas // 2
    tdraw.text((cx, cy), emoji, font=best_font, fill=0, anchor="mm")

    # Find the actual ink bounding box (non-white pixels)
    diff = ImageChops.difference(tmp, Image.new("L", tmp.size, 255))
    ink_bb = diff.getbbox()
    if not ink_bb:
        return

    # Crop to just the ink
    emoji_img = tmp.crop(ink_bb)
    ew, eh    = emoji_img.size

    # Scale to fill 82% of the icon area
    scale = min(size * 0.82 / ew, size * 0.82 / eh)
    if scale != 1.0:
        emoji_img = emoji_img.resize(
            (max(1, int(ew * scale)), max(1, int(eh * scale))),
            Image.LANCZOS,
        )
        ew, eh = emoji_img.size

    # Paste centered in the icon box using the grayscale as a mask so the
    # emoji renders cleanly on any background (white labels, Win95 gray, etc.)
    # In L mode: 0 = ink, 255 = background.  Invert so 255 = opaque ink, 0 = transparent.
    mask      = ImageChops.invert(emoji_img)
    color_img = Image.new("RGB", emoji_img.size, color)
    paste_x   = x + (size - ew) // 2
    paste_y   = y + (size - eh) // 2
    img.paste(color_img, (paste_x, paste_y), mask=mask)

# ── Border drawing ────────────────────────────────────────────────────────────

def _overlay_image_border(img: Image.Image, name: str, w_px: int, h_px: int) -> Image.Image:
    """Resize border_<name>.* to the label size, recolour to black, and composite."""
    path = next(
        (f for ext in (".png", ".webp", ".jpg", ".jpeg")
         for f in [os.path.join(_IMAGES_DIR, f"border_{name}{ext}")]
         if os.path.exists(f)),
        None,
    )
    if not path:
        return img
    border = Image.open(path).convert("RGBA").resize((w_px, h_px), Image.LANCZOS)
    # Force all non-transparent pixels to pure black
    _, _, _, a = border.split()
    black_border = Image.merge("RGBA", [
        Image.new("L", border.size, 0),
        Image.new("L", border.size, 0),
        Image.new("L", border.size, 0),
        a,
    ])
    result = Image.alpha_composite(img.convert("RGBA"), black_border)
    return result.convert("RGB")


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
