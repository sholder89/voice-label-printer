import json
import logging
import os
import time
import urllib.request
import urllib.error

logger = logging.getLogger()
logger.setLevel(logging.INFO)

WEBHOOK_URL  = os.environ["WEBHOOK_URL"]    # e.g. https://your-relay-server.com/webhook
SETTINGS_URL = os.environ["SETTINGS_URL"]   # e.g. https://your-relay-server.com/settings
LABEL_TOKEN  = os.environ["LABEL_TOKEN"]    # shared secret — sent as X-Token header, not in URL

# How many times to retry a failed request before giving up
_MAX_RETRIES = 2
_RETRY_DELAY = 1.0
_TIMEOUT     = 8

# ── Alexa Interaction Model — intents to add/update in the developer console ──
#
# NEW INTENTS:
#
#   ChangeStylePresetIntent
#     Slots:  presetName  (custom slot type: LIST_OF_PRESETS)
#     Sample utterances:
#       set style to {presetName}
#       use {presetName} style
#       change style to {presetName}
#       switch to {presetName} style
#       apply {presetName} style
#       {presetName} style
#     Slot values for LIST_OF_PRESETS:
#       none, off, no style, normal, default, clear
#       bold
#       elegant
#       retro, retro typewriter, typewriter
#       minimal
#       warning, caution
#       address, address label, mailing
#       windows 95, windows ninety five
#
#   ChangeSizeIntent
#     Slots:  labelSize  (custom slot type: LIST_OF_SIZES)
#     Sample utterances:
#       set size to {labelSize}
#       use {labelSize} labels
#       change size to {labelSize}
#       switch to {labelSize}
#       {labelSize} label size
#     Slot values for LIST_OF_SIZES:
#       two by one, two by one inch, small label
#       four by two, four by two inch, large label
#       four by six, four by six inch, shipping label
#       three by two, three by two inch
#       two by half, two by half inch, tiny label
#       one by three and a half, address label, brother address, twenty nine by ninety
#       one by two and a half, brother short, twenty nine by sixty two
#
#   ToggleIconsIntent
#     Slots:  onOff  (AMAZON.OnOff built-in)
#     Sample utterances:
#       turn icons {onOff}
#       turn {onOff} icons
#       set icons {onOff}
#       icons {onOff}
#       emoji {onOff}
#       turn {onOff} emoji
#       auto icons {onOff}
#
#   ChangeAlignmentIntent
#     Slots:  textAlign  (custom slot type: TextAlign)
#     Sample utterances:
#       set alignment to {textAlign}
#       change alignment to {textAlign}
#       align {textAlign}
#       set text alignment to {textAlign}
#       {textAlign} align
#       {textAlign} alignment
#     Slot values for TextAlign:
#       left, left align, left aligned, align left
#       center, centred, centered, centre, middle
#       right, right align, right aligned, align right
#
# UPDATED INTENTS:
#
#   ChangeFontIntent — add Burbank slot values:
#     burbank, burbank big, burbank big condensed, big condensed
# ──────────────────────────────────────────────────────────────────────────────


# ── Friendly names Alexa might say → canonical values ─────────────────────────

_FONT_MAP = {
    "standard":             "standard",
    "enhanced":             "enhanced",
    "impact":               "impact",
    "serif":                "serif",
    "narrow":               "narrow",
    "mono":                 "mono",
    "monospace":            "mono",
    "courier":              "mono",
    "consolas":             "consolas",
    "console":              "consolas",
    "bahnschrift":          "bahnschrift",
    "bonn schrift":         "bahnschrift",
    "ink free":             "inkfree",
    "inkfree":              "inkfree",
    "handwriting":          "inkfree",
    "handwritten":          "inkfree",
    "burbank":              "burbank",
    "burbank big":          "burbank",
    "burbank big condensed":"burbank",
    "big condensed":        "burbank",
}

_BORDER_MAP = {
    "none":      "none",
    "off":       "none",
    "no border": "none",
    "thin":      "thin",
    "thick":     "thick",
    "double":    "double",
    "dashed":    "dashed",
    "dotted":    "dotted",
    "dots":      "dotted",
    "wave":      "wave",
    "wavy":      "wave",
    "scallop":   "wave",
    "scalloped": "wave",
    "ticket":    "ticket",
    "perforated":"ticket",
    "inset":     "inset",
    "recessed":  "inset",
    "3d":        "inset",
    "rounded":   "rounded",
    "corners":   "corners",
    "corner":    "corners",
}

_CASE_MAP = {
    "none":          "none",
    "normal":        "none",
    "default":       "none",
    "as typed":      "none",
    "uppercase":     "uppercase",
    "upper":         "uppercase",
    "all caps":      "uppercase",
    "caps":          "uppercase",
    "capital":       "uppercase",
    "all uppercase": "uppercase",
    "lowercase":     "lowercase",
    "lower":         "lowercase",
    "all lowercase": "lowercase",
    "title":         "title",
    "title case":    "title",
    "titlecase":     "title",
    "sentence":      "sentence",
    "sentence case": "sentence",
}

_PRESET_MAP = {
    "none":                  "none",
    "off":                   "none",
    "no style":              "none",
    "normal":                "none",
    "default":               "none",
    "clear":                 "none",
    "clear style":           "none",
    "bold":                  "bold",
    "elegant":               "elegant",
    "retro":                 "retro",
    "retro typewriter":      "retro",
    "typewriter":            "retro",
    "minimal":               "minimal",
    "warning":               "warning",
    "caution":               "warning",
    "address":               "address",
    "address label":         "address",
    "mailing":               "address",
    "mailing label":         "address",
    "windows 95":            "windows95",
    "windows ninety five":   "windows95",
    "windows95":             "windows95",
    "ninety five":           "windows95",
    "price tag":             "price_tag",
    "price label":           "price_tag",
    "tag":                   "price_tag",
    "cassette":              "cassette",
    "cassette spine":        "cassette",
    "tape":                  "cassette",
    "blueprint":             "blueprint",
    "blue print":            "blueprint",
    "technical":             "blueprint",
    "qr code":               "qr_code",
    "qr":                    "qr_code",
    "q r code":              "qr_code",
    "scan code":             "qr_code",
    "barcode":               "barcode",
    "bar code":              "barcode",
    "code 128":              "barcode",
    "name tag":              "name_tag",
    "name badge":            "name_tag",
    "badge":                 "name_tag",
    "hello my name is":      "name_tag",
    "receipt":               "receipt",
    "chalkboard":            "chalkboard",
    "chalk board":           "chalkboard",
    "blackboard":            "chalkboard",
}

_SIZE_MAP = {
    "two by one":            "2x1",
    "two by one inch":       "2x1",
    "2 by 1":                "2x1",
    "2x1":                   "2x1",
    "small label":           "2x1",
    "four by two":           "4x2",
    "four by two inch":      "4x2",
    "4 by 2":                "4x2",
    "4x2":                   "4x2",
    "large label":           "4x2",
    "four by six":           "4x6",
    "four by six inch":      "4x6",
    "4 by 6":                "4x6",
    "4x6":                   "4x6",
    "shipping label":        "4x6",
    "three by two":          "3x2",
    "three by two inch":     "3x2",
    "3 by 2":                "3x2",
    "3x2":                   "3x2",
    "two by half":           "2x0.5",
    "two by half inch":      "2x0.5",
    "two by point five":     "2x0.5",
    "tiny label":            "2x0.5",
    # Brother QL 29 mm continuous tape
    "one by three and a half":  "1.1x3.5",
    "1.1x3.5":                  "1.1x3.5",
    "address label":            "1.1x3.5",
    "brother address":          "1.1x3.5",
    "twenty nine by ninety":    "1.1x3.5",
    "one by two and a half":    "1.1x2.4",
    "1.1x2.4":                  "1.1x2.4",
    "brother short":            "1.1x2.4",
    "twenty nine by sixty two": "1.1x2.4",
}

# ── Human-readable confirmations ──────────────────────────────────────────────

_FONT_LABELS = {
    "standard": "standard", "enhanced": "enhanced", "impact": "impact",
    "serif": "serif",       "narrow": "narrow",      "mono": "mono",
    "consolas": "Consolas", "bahnschrift": "Bahnschrift", "inkfree": "Ink Free",
    "burbank": "Burbank",
}
_BORDER_LABELS = {
    "none": "off",     "thin": "thin",       "thick": "thick",
    "double": "double","dashed": "dashed",    "dotted": "dotted",
    "wave": "wave",    "ticket": "ticket",   "inset": "inset",
    "rounded": "rounded", "corners": "corners",
}
_CASE_LABELS = {
    "none": "normal",           "uppercase": "all caps",
    "lowercase": "all lowercase","title": "title case",
    "sentence": "sentence case",
}
_PRESET_LABELS = {
    "none":       "no style",
    "bold":       "bold",
    "elegant":    "elegant",
    "retro":      "retro typewriter",
    "minimal":    "minimal",
    "warning":    "warning",
    "address":    "address label",
    "windows95":  "Windows 95",
    "price_tag":  "price tag",
    "cassette":   "cassette",
    "blueprint":  "blueprint",
    "qr_code":    "QR code",
    "barcode":    "barcode",
    "name_tag":   "name tag",
    "receipt":    "receipt",
    "chalkboard": "chalkboard",
}

_WEIGHT_MAP = {
    "normal":      "normal",
    "regular":     "normal",
    "light":       "normal",
    "bold":        "bold",
    "italic":      "italic",
    "italics":     "italic",
    "bold italic":  "bold_italic",
    "bold italics": "bold_italic",
    "bold and italic": "bold_italic",
}

_WEIGHT_LABELS = {
    "normal":     "normal",
    "bold":       "bold",
    "italic":     "italic",
    "bold_italic": "bold italic",
}
_SIZE_LABELS = {
    "2x1":     "two by one",
    "4x2":     "four by two",
    "4x6":     "four by six",
    "3x2":     "three by two",
    "2x0.5":   "two by half",
    "1.1x3.5": "Brother address label",
    "1.1x2.4": "Brother short label",
}

_ALIGN_MAP = {
    "left":          "left",
    "left align":    "left",
    "left aligned":  "left",
    "align left":    "left",
    "center":        "center",
    "centred":       "center",
    "centered":      "center",
    "centre":        "center",
    "middle":        "center",
    "align center":  "center",
    "right":         "right",
    "right align":   "right",
    "right aligned": "right",
    "align right":   "right",
}

_ALIGN_LABELS = {
    "left":   "left aligned",
    "center": "centered",
    "right":  "right aligned",
}


# ── Lambda entry point ────────────────────────────────────────────────────────

def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event))

    req_type = event["request"]["type"]

    if req_type == "LaunchRequest":
        return _respond(
            "Label printer ready. You can print a label, or change the style, "
            "font, border, text case, size, or toggle icons.",
            end=False,
        )

    if req_type == "IntentRequest":
        return _handle_intent(event["request"]["intent"])

    if req_type == "SessionEndedRequest":
        return _respond("Goodbye!")

    return _respond("Sorry, I didn't understand that.")


def _handle_intent(intent):
    logger.info("Intent: %s", json.dumps(intent))
    name = intent["name"]

    # ── Print ──────────────────────────────────────────────────────────────────
    if name == "PrintLabelIntent":
        text = intent.get("slots", {}).get("labelText", {}).get("value", "").strip()
        logger.info("Label text: %r", text)
        if not text:
            return _respond("I didn't catch what you wanted to print. Please try again.", end=False)
        try:
            _post_webhook(text)
            return _respond(f"Printing: {text}")
        except Exception as e:
            logger.error("Webhook failed after retries: %s", e)
            return _respond("Sorry, I couldn't reach the printer. Please try again.")

    # ── Font ───────────────────────────────────────────────────────────────────
    if name == "ChangeFontIntent":
        raw = _slot_value(intent, "fontStyle")
        val = _FONT_MAP.get(raw.lower()) if raw else None
        if not val:
            return _respond(
                "I didn't recognise that font. Available fonts are: "
                "standard, enhanced, impact, serif, narrow, mono, Consolas, "
                "Bahnschrift, Ink Free, and Burbank.",
                end=False,
            )
        try:
            _post_setting("font_style", val)
            return _respond(f"Font changed to {_FONT_LABELS[val]}.")
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Border ─────────────────────────────────────────────────────────────────
    if name == "ChangeBorderIntent":
        raw = _slot_value(intent, "borderStyle")
        val = _BORDER_MAP.get(raw.lower()) if raw else None
        if not val and raw:
            val = _BORDER_MAP.get(raw.lower().replace("-", " "))
        if val is None:
            return _respond(
                "I didn't recognise that border style. Options are: "
                "none, thin, thick, double, dashed, dotted, wave, ticket, "
                "inset, rounded, and corners.",
                end=False,
            )
        try:
            _post_setting("border", val)
            msg = "Border turned off." if val == "none" else f"Border set to {_BORDER_LABELS[val]}."
            return _respond(msg)
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Text case ──────────────────────────────────────────────────────────────
    if name == "ChangeTextCaseIntent":
        raw = _slot_value(intent, "textCase")
        val = _CASE_MAP.get(raw.lower()) if raw else None
        if val is None:
            return _respond(
                "I didn't recognise that text case. Options are: "
                "normal, all caps, all lowercase, title case, and sentence case.",
                end=False,
            )
        try:
            _post_setting("text_case", val)
            return _respond(f"Text case set to {_CASE_LABELS[val]}.")
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Text alignment ─────────────────────────────────────────────────────────
    if name == "ChangeAlignmentIntent":
        raw = _slot_value(intent, "textAlign")
        val = _ALIGN_MAP.get(raw.lower()) if raw else None
        if val is None:
            return _respond(
                "I didn't recognise that alignment. Options are: left, center, and right.",
                end=False,
            )
        try:
            _post_setting("text_align", val)
            return _respond(f"Text alignment set to {_ALIGN_LABELS[val]}.")
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Font weight ────────────────────────────────────────────────────────────
    if name == "ChangeFontWeightIntent":
        raw = _slot_value(intent, "fontWeight")
        val = _WEIGHT_MAP.get(raw.lower()) if raw else None
        if not val:
            return _respond(
                "I didn't recognise that font weight. Options are: "
                "normal, bold, italic, and bold italic.",
                end=False,
            )
        try:
            _post_setting("font_weight", val)
            return _respond(f"Font weight set to {_WEIGHT_LABELS[val]}.")
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Style preset ───────────────────────────────────────────────────────────
    if name == "ChangeStylePresetIntent":
        raw = _slot_value(intent, "presetName")
        val = _PRESET_MAP.get(raw.lower()) if raw else None
        if val is None:
            return _respond(
                "I didn't recognise that style. Available styles are: "
                "bold, elegant, retro, minimal, warning, address label, "
                "price tag, cassette, blueprint, QR code, barcode, name tag, "
                "receipt, chalkboard, Windows 95, or none to clear.",
                end=False,
            )
        try:
            _post_setting("style_preset", val)
            label = _PRESET_LABELS[val]
            msg = "Style cleared." if val == "none" else f"Style set to {label}."
            return _respond(msg)
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Label size ─────────────────────────────────────────────────────────────
    if name == "ChangeSizeIntent":
        raw = _slot_value(intent, "labelSize")
        val = _SIZE_MAP.get(raw.lower()) if raw else None
        if val is None:
            return _respond(
                "I didn't recognise that size. Available sizes are: "
                "two by one, four by two, four by six, three by two, two by half, "
                "and the Brother tape sizes: address label and brother short.",
                end=False,
            )
        try:
            _post_setting("size", val)
            return _respond(f"Label size set to {_SIZE_LABELS[val]}.")
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Icons toggle ───────────────────────────────────────────────────────────
    if name == "ToggleIconsIntent":
        raw = _slot_value(intent, "onOff")
        if raw is None:
            return _respond("Did you want to turn icons on or off?", end=False)
        enable = raw.lower() in ("on", "yes", "true", "enable", "enabled", "activate")
        try:
            _post_setting("icons", "true" if enable else "false")
            return _respond("Auto icons turned on." if enable else "Auto icons turned off.")
        except Exception as e:
            logger.error("Settings failed: %s", e)
            return _respond("Sorry, I couldn't update the setting. Please try again.")

    # ── Built-ins ──────────────────────────────────────────────────────────────
    if name == "AMAZON.HelpIntent":
        return _respond(
            "You can say: print Hello World. "
            "Or change settings: set style to bold, set font to impact, "
            "set font weight to italic, set border to thick, "
            "set text case to all caps, set size to four by two, or turn icons off.",
            end=False,
        )

    if name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
        return _respond("Goodbye!")

    return _respond("Sorry, I didn't understand that.")


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _slot_value(intent, slot_name):
    """Return the spoken slot value, or None if absent."""
    slot = intent.get("slots", {}).get(slot_name, {})
    # Prefer entity resolution canonical value if present
    resolutions = slot.get("resolutions", {}).get("resolutionsPerAuthority", [])
    for res in resolutions:
        if res.get("status", {}).get("code") == "ER_SUCCESS_MATCH":
            values = res.get("values", [])
            if values:
                return values[0]["value"]["name"]
    return slot.get("value")


def _post_webhook(text):
    data = json.dumps({"value1": text}).encode()
    _request(WEBHOOK_URL, data)


def _post_setting(key, value):
    data = json.dumps({"key": key, "value": value}).encode()
    _request(SETTINGS_URL, data)


def _request(url, data):
    """POST with retries. Raises on final failure."""
    last_err = None
    for attempt in range(_MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent":   "AlexaLabelPrinter/1.0",
                    "X-Token":      LABEL_TOKEN,
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
                resp.read()
            logger.info("Request to %s succeeded on attempt %d", url, attempt + 1)
            return
        except Exception as e:
            last_err = e
            logger.warning("Request attempt %d/%d failed: %s", attempt + 1, _MAX_RETRIES + 1, e)
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)
    raise last_err


def _respond(speech, end=True):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": speech},
            "shouldEndSession": end,
        },
    }
