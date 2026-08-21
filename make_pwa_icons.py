"""Generate the PWA / home-screen icon set from one square source image.

    python make_pwa_icons.py path/to/icon.png

Writes into client/static/icons/. The source should be square and at least
512x512. Transparency is flattened — iOS composites home-screen icons onto
white otherwise — using a colour sampled from the artwork itself, so a rounded
tile on a transparent background doesn't end up with mismatched corners.

Maskable icons get extra padding: Android crops them to whatever shape the
launcher uses (circle, squircle, rounded square), and artwork drawn to the edge
loses its corners. The safe zone is the middle 80%.
"""
import os
import sys
from PIL import Image

OUT_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client", "static", "icons")
FALLBACK_BG = (59, 130, 246)    # --accent, used only if the source gives no clue

# (filename, pixel size, maskable) — maskable variants are inset for launcher cropping
TARGETS = [
    ("icon-192.png",            192, False),
    ("icon-512.png",            512, False),
    ("icon-maskable-192.png",   192, True),
    ("icon-maskable-512.png",   512, True),
    ("apple-touch-icon.png",    180, False),   # iOS home screen
]


def _backdrop(src):
    """Pick the colour to sit behind the artwork.

    App-icon artwork usually arrives as a rounded tile on transparency. Padding
    that out with an unrelated colour leaves wedges in the corners, so sample
    what the tile itself uses: the most common opaque colour along the edge
    midpoints, which sit inside the rounding but outside the subject.
    """
    w, h = src.size
    step = max(1, w // 64)
    samples = []
    for i in range(step, w - step, step):
        for x, y in ((i, step), (i, h - 1 - step), (step, i), (w - 1 - step, i)):
            r, g, b, a = src.getpixel((x, y))
            if a > 250:
                # Round off so a gradient still agrees on one representative shade
                samples.append((r // 8 * 8, g // 8 * 8, b // 8 * 8))
    if not samples:
        return FALLBACK_BG
    return max(set(samples), key=samples.count)


def build(src_path):
    src = Image.open(src_path).convert("RGBA")
    if src.width != src.height:
        side = min(src.width, src.height)
        left = (src.width - side) // 2
        top  = (src.height - side) // 2
        src  = src.crop((left, top, left + side, top + side))
        print(f"  cropped to square: {side}x{side}")

    bg = _backdrop(src)
    print(f"  backdrop sampled from source: #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}")

    os.makedirs(OUT_DIR, exist_ok=True)
    for name, size, maskable in TARGETS:
        canvas = Image.new("RGBA", (size, size), bg + (255,))
        # Maskable art has to survive the launcher cropping it to a circle or
        # squircle, so it sits in the middle 80%. Everything else is full bleed:
        # the artwork already carries its own shape, and iOS masks it anyway.
        inner = round(size * 0.80) if maskable else size
        art   = src.resize((inner, inner), Image.LANCZOS)
        off   = (size - inner) // 2
        canvas.paste(art, (off, off), art)
        canvas.convert("RGB").save(os.path.join(OUT_DIR, name), "PNG", optimize=True)
        print(f"  {name:26s} {size}x{size}{'  (maskable, 80% inset)' if maskable else ''}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: python {os.path.basename(__file__)} <square-source-image>")
    if not os.path.isfile(sys.argv[1]):
        sys.exit(f"no such file: {sys.argv[1]}")
    print(f"source: {sys.argv[1]}")
    build(sys.argv[1])
    print(f"\nwrote {len(TARGETS)} icons to {OUT_DIR}")
