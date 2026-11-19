#!/usr/bin/env python3
"""Compose the gta6-meme-x-01 meme: Vice City base scene + make.fun ghost in the
driver's seat + bold meme text. Output: meme.jpg (2048x1152) + a 480px preview."""
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets/media-generation-vice-city-base-0-1cdad1bb-c6ed-46d7-9e4b-b6acec1c3348.jpg"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets/mark-1024.png"
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme.jpg"
PREVIEW = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme-preview-480.jpg"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MAGENTA = (255, 46, 154)

img = Image.open(BASE).convert("RGB")
W, H = img.size  # 2048 x 1152

# 1. Ghost in the driver's seat: 280px tall, bottom at y=765, centred x=1500,
# so its lower third sits in the cabin, head above the windshield.
ghost = Image.open(GHOST).convert("RGBA")
gh = 280
gw = int(ghost.width * gh / ghost.height)
ghost = ghost.resize((gw, gh), Image.LANCZOS)
img.paste(ghost, (1500 - gw // 2, 765 - gh), ghost)

d = ImageDraw.Draw(img)

def text_center(y, s, font, fill, stroke_w, stroke_fill=(0, 0, 0)):
    bbox = d.textbbox((0, 0), s, font=font, stroke_width=stroke_w)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) / 2, y), s, font=font, fill=fill,
           stroke_width=stroke_w, stroke_fill=stroke_fill)

# 2. Top line.
f_top = ImageFont.truetype(FONT_BOLD, 90)
text_center(36, "WAITED 13 YEARS FOR GTA 6", f_top, (255, 255, 255), 8)

# 3. Bottom line.
f_bot = ImageFont.truetype(FONT_BOLD, 84)
text_center(1005, "CALLED IN SICK. SO DID MY BOSS.", f_bot, (255, 255, 255), 8)

# 4. make.fun wordmark, bottom-left corner, magenta (clear of the centred
# bottom line, which starts around x=250).
f_mark = ImageFont.truetype(FONT_BOLD, 40)
mark = "make.fun"
d.text((40, 1092), mark, font=f_mark, fill=MAGENTA,
       stroke_width=5, stroke_fill=(0, 0, 0))

img.save(OUT, "JPEG", quality=90)
img.resize((480, 270), Image.LANCZOS).save(PREVIEW, "JPEG", quality=85)
print("saved", OUT, img.size)
