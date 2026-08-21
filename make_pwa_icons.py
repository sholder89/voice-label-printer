"""Generate the PWA / home-screen icon set from one square source image.

    python make_pwa_icons.py path/to/icon.png

Writes into client/static/icons/. The source should be square and at least
512x512; anything with transparency is flattened onto BG_COLOR so it doesn't
show through on iOS, which composites home-screen icons on white otherwise.

Maskable icons get extra padding: Android crops them to whatever shape the
launcher uses (circle, squircle, rounded square), and artwork drawn to the edge
loses its corners. The safe zone is the middle 80%.
"""
import os
import sys
from PIL import Image

OUT_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client", "static", "icons")
BG_COLOR = (59, 130, 246)      # --accent, so a transparent source still reads as the app

# (filename, pixel size, maskable) — maskable variants are inset for launcher cropping
TARGETS = [
    ("icon-192.png",            192, False),
    ("icon-512.png",            512, False),
    ("icon-maskable-192.png",   192, True),
    ("icon-maskable-512.png",   512, True),
    ("apple-touch-icon.png",    180, False),   # iOS home screen
]


def build(src_path):
    src = Image.open(src_path).convert("RGBA")
    if src.width != src.height:
        side = min(src.width, src.height)
        left = (src.width - side) // 2
        top  = (src.height - side) // 2
        src  = src.crop((left, top, left + side, top + side))
        print(f"  cropped to square: {side}x{side}")

    os.makedirs(OUT_DIR, exist_ok=True)
    for name, size, maskable in TARGETS:
        canvas = Image.new("RGBA", (size, size), BG_COLOR + (255,))
        # Maskable art lives in the middle 80%; plain icons get a small margin
        # so the glyph doesn't touch the rounded corners iOS applies.
        inner = round(size * (0.80 if maskable else 0.92))
        art   = src.resize((inner, inner), Image.LANCZOS)
        off   = (size - inner) // 2
        canvas.paste(art, (off, off), art)
        canvas.convert("RGB").save(os.path.join(OUT_DIR, name), "PNG", optimize=True)
        print(f"  {name:26s} {size}x{size}{'  (maskable)' if maskable else ''}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: python {os.path.basename(__file__)} <square-source-image>")
    if not os.path.isfile(sys.argv[1]):
        sys.exit(f"no such file: {sys.argv[1]}")
    print(f"source: {sys.argv[1]}")
    build(sys.argv[1])
    print(f"\nwrote {len(TARGETS)} icons to {OUT_DIR}")
