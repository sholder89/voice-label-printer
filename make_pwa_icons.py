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
from PIL import Image, ImageChops, ImageDraw

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


def _trim_border(src):
    """Crop off a flat border around the artwork.

    Exported icon art often carries a margin — commonly black, where a
    transparent background was flattened on save. Left in place it becomes a
    dark frame around every generated icon, so if all four corners agree on a
    colour, crop to the region that differs from it.
    """
    w, h = src.size
    corners = [src.getpixel(p)[:3] for p in
               ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2))]
    spread = max(max(c[i] for c in corners) - min(c[i] for c in corners)
                 for i in range(3))
    if spread > 12:
        return src                      # corners disagree: no uniform border

    flat = Image.new("RGB", src.size, corners[0])
    diff = ImageChops.difference(src.convert("RGB"), flat).convert("L")
    box  = diff.point(lambda v: 255 if v > 18 else 0).getbbox()
    if not box:
        return src
    # Refuse to trim so much that we'd be cropping into the subject.
    if (box[2] - box[0]) < w * 0.6 or (box[3] - box[1]) < h * 0.6:
        return src
    if box == (0, 0, w, h):
        return src
    print(f"  trimmed {corners[0]} border -> {box[2] - box[0]}x{box[3] - box[1]}")
    return src.crop(box)


def _backdrop(src):
    """Pick the colour to sit behind the artwork.

    App-icon artwork usually arrives as a rounded tile. Padding it out with an
    unrelated colour leaves wedges in the corners, so sample what the tile
    itself uses.

    Only the middle half of each edge is sampled: the corners are exactly where
    the rounding lives, and including them lets a flat corner colour outvote the
    tile, since a gradient's votes are split across many shades while the
    corners agree on one. A per-channel median finishes the job.
    """
    w, h = src.size
    inset = max(1, round(min(w, h) * 0.04))
    samples = []
    for span, vertical in ((w, False), (h, True)):
        lo, hi = round(span * 0.25), round(span * 0.75)
        step = max(1, (hi - lo) // 48)
        for i in range(lo, hi, step):
            pts = ((inset, i), (w - 1 - inset, i)) if vertical else                   ((i, inset), (i, h - 1 - inset))
            for x, y in pts:
                r, g, b, a = src.getpixel((x, y))
                if a > 250:
                    samples.append((r, g, b))
    if not samples:
        return FALLBACK_BG
    return tuple(sorted(s[c] for s in samples)[len(samples) // 2] for c in range(3))


def _fill_corners(src, bg):
    """Repaint the flat area outside a rounded tile's corners.

    Artwork saved without alpha bakes whatever was behind it into the corners,
    usually black. Full-bleed icons would then carry dark wedges that iOS's own
    rounding doesn't quite cover.

    Recolouring every dark pixel would eat the subject — this printer is black —
    so flood fill inward from each corner instead. That only reaches pixels
    connected to the corner, and stops dead at the tile edge.
    """
    img = src.convert("RGB")
    w, h = img.size
    filled = False
    for corner in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        px = img.getpixel(corner)
        if sum(px) > 150 or px == bg:
            continue                    # not a dark surround, or already right
        ImageDraw.floodfill(img, corner, bg, thresh=70)
        filled = True
    if filled:
        print(f"  repainted corner surround -> #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}")
    return img.convert("RGBA")


def build(src_path):
    src = Image.open(src_path).convert("RGBA")
    src = _trim_border(src)
    if src.width != src.height:
        side = min(src.width, src.height)
        left = (src.width - side) // 2
        top  = (src.height - side) // 2
        src  = src.crop((left, top, left + side, top + side))
        print(f"  cropped to square: {side}x{side}")

    bg = _backdrop(src)
    print(f"  backdrop sampled from source: #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}")
    src = _fill_corners(src, bg)

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
