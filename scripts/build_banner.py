#!/usr/bin/env python3
"""Create a self-contained PNG banner using the public redp4w GitHub avatar.

The avatar is embedded, so GitHub need not fetch an image inside an SVG.
Edit the PALETTE, text labels and watermark opacity to maintain the design.
"""
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "assets" / "hero.png"
AVATAR_URL = "https://avatars.githubusercontent.com/u/168608062?v=4&s=400"
SIZE = (1120, 265)
BG, GRID, GREEN, RED = "#0b191a", "#244137", "#b0ff69", "#ff5b6e"
CYAN, TEXT, MUTED = "#70e0d7", "#edfff4", "#9cbeb1"


def font(size, bold=False):
    family = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + family, size)
    except OSError:
        return ImageFont.load_default()


def main():
    request = Request(AVATAR_URL, headers={"User-Agent": "redp4w-banner"})
    with urlopen(request, timeout=30) as response:
        data = response.read(2_000_001)
        content_type = response.headers.get_content_type()
    if len(data) > 2_000_000 or not content_type.startswith("image/"):
        raise ValueError("Unexpected GitHub avatar response")

    image = Image.new("RGBA", SIZE, BG)
    draw = ImageDraw.Draw(image)
    for x in range(0, SIZE[0], 25):
        draw.line((x, 0, x, SIZE[1]), fill=GRID, width=1)
    for y in range(0, SIZE[1], 25):
        draw.line((0, y, SIZE[0], y), fill=GRID, width=1)

    # Gentle radial transparency for the actual account avatar.
    avatar_size = 244
    avatar = Image.open(BytesIO(data)).convert("RGBA").resize(
        (avatar_size, avatar_size), Image.Resampling.LANCZOS
    )
    alpha = Image.new("L", (avatar_size, avatar_size), 0)
    pixels = alpha.load()
    center = avatar_size / 2
    for y in range(avatar_size):
        for x in range(avatar_size):
            distance = ((x-center)**2 + (y-center)**2)**0.5 / center
            pixels[x, y] = int(75 * max(0, min(1, (1.0-distance)/0.55)))
    avatar.putalpha(alpha)
    image.alpha_composite(avatar, (824, 12))

    # Terminal header and split-color alias: red in white; p4w in red.
    draw = ImageDraw.Draw(image)
    draw.line((34, 52, 1086, 52), fill="#34554b", width=1)
    for x, c in [(53, GREEN), (73, CYAN), (93, "#416456")]:
        draw.ellipse((x-5, 23, x+5, 33), fill=c)
    draw.text((119, 21), "~/redp4w/security-notes", font=font(13), fill=MUTED)
    heading = font(49, bold=True)
    x, y = 49, 74
    for part, color in [(">_ ", GREEN), ("red", TEXT), ("p4w", RED)]:
        draw.text((x, y), part, font=heading, fill=color)
        x += draw.textlength(part, font=heading)
    draw.rounded_rectangle((50, 134, 480, 137), radius=1, fill=GREEN)
    draw.text((52, 150), "SECURITY FIELD NOTES", font=font(20), fill=TEXT)
    draw.text((52, 184), "BLUE TEAM / OFFENSIVE LEARNING / RESEARCH", font=font(14), fill=MUTED)
    draw.text((52, 225), "$ learn --investigate --document --defend", font=font(13), fill=CYAN)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"Updated {OUT.name}: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
