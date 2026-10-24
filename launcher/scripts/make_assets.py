#!/usr/bin/env python3
"""Generates the TV Livre icon, large icon and splash screen (requires Pillow).

The mark is a TV outline with a play triangle on a green rounded square.
Re-run after changing colors: python launcher/scripts/make_assets.py
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "assets")
GREEN_LIGHT = (31, 199, 126)   # #1fc77e
GREEN_DARK = (14, 122, 75)     # #0e7a4b
BG_CENTER = (23, 29, 51)       # matches --bg-gradient in index.html
BG_EDGE = (4, 6, 10)
SS = 4  # supersampling factor for smooth edges


def gradient(size, top, bottom):
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            px[x, y] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return img


def mark(size):
    """The app icon at `size` px: rounded green square with a white TV + play glyph."""
    big = size * SS
    base = gradient(big, GREEN_LIGHT, GREEN_DARK).convert("RGBA")
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, big - 1, big - 1], radius=big * 0.22, fill=255)
    base.putalpha(mask)

    d = ImageDraw.Draw(base)
    w = big * 0.06
    # TV body
    left, top, right, bottom = big * 0.2, big * 0.25, big * 0.8, big * 0.66
    d.rounded_rectangle([left, top, right, bottom], radius=big * 0.05, outline="white", width=round(w))
    # Stand
    d.line([(big * 0.38, big * 0.77), (big * 0.62, big * 0.77)], fill="white", width=round(w))
    d.line([(big * 0.5, bottom), (big * 0.5, big * 0.77)], fill="white", width=round(w))
    # Play triangle
    cx, cy, r = big * 0.515, (top + bottom) / 2, big * 0.1
    d.polygon([(cx - r * 0.8, cy - r), (cx - r * 0.8, cy + r), (cx + r, cy)], fill="white")
    return base.resize((size, size), Image.LANCZOS)


def font(size, bold=False):
    for name in (["segoeuib.ttf", "seguisb.ttf"] if bold else ["segoeui.ttf"]) + ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]:
        for folder in ("C:/Windows/Fonts", "/usr/share/fonts/truetype/dejavu"):
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    sys.exit("[!] No TTF font found (Segoe UI or DejaVu).")


def splash():
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), BG_EDGE)
    px = img.load()
    cx, cy, maxd = w / 2, -0.1 * h, (w ** 2 + h ** 2) ** 0.5 * 0.75
    for y in range(h):
        for x in range(w):
            t = min(((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / maxd, 1)
            px[x, y] = tuple(round(BG_CENTER[i] + (BG_EDGE[i] - BG_CENTER[i]) * t) for i in range(3))
    icon = mark(220)
    img.paste(icon, ((w - 220) // 2, 330), icon)
    d = ImageDraw.Draw(img)
    for text, f, y, color in (("TV Livre", font(96, bold=True), 600, (245, 245, 247)),
                              ("Sua TV, sem anúncios", font(36), 730, (170, 176, 190))):
        tw = d.textlength(text, font=f)
        d.text(((w - tw) / 2, y), text, font=f, fill=color)
    return img


if __name__ == "__main__":
    mark(80).save(os.path.join(ASSETS, "icon.png"))
    mark(130).save(os.path.join(ASSETS, "largeIcon.png"))
    splash().save(os.path.join(ASSETS, "splash.png"), optimize=True)
    print(f"[+] Assets written to {ASSETS}")
