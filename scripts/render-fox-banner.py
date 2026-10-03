"""Assemble the generated walk-cycle sprites into a looping README banner.

Requires Pillow. Run: python scripts/render-fox-banner.py
Override FONT_DIR for systems without the DejaVu fonts in the default path.
"""
from pathlib import Path
import os
import random
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
FONT_DIR = Path(os.environ.get('FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
W, H, COUNT = 960, 260, 200
bg = Image.new('RGB', (W, H), '#20291f')
d = ImageDraw.Draw(bg)
d.rounded_rectangle((1, 1, W-2, H-2), radius=18, outline='#46533c', width=2)
rng = random.Random(13)
for _ in range(85):
    x, y = rng.randrange(24, W-24), rng.randrange(15, 210)
    if 42 < x < 520 and 45 < y < 180:
        continue
    color = rng.choice(['#687052', '#8b8b63', '#4c5b42'])
    d.line((x, y, x+2, y), fill=color)
# Small crescent and a quiet woodland floor.
d.ellipse((806, 40, 842, 76), fill='#d9d9b9')
d.ellipse((816, 34, 850, 68), fill='#20291f')
d.line((28, 229, W-28, 229), fill='#4b583e')
for x in range(30, W-25, 19):
    h = rng.randrange(3, 10)
    d.line((x-3, 230, x, 230-h, x+2, 230), fill='#5b684a')
serif = ImageFont.truetype(str(FONT_DIR/'DejaVuSerif.ttf'), 51)
mono = ImageFont.truetype(str(FONT_DIR/'DejaVuSansMono.ttf'), 13)
small = ImageFont.truetype(str(FONT_DIR/'DejaVuSansMono.ttf'), 11)
d.text((44, 36), 'PHNOM PENH / CAMBODIA', font=small, fill='#a8b69a')
d.text((40, 65), 'Yuujin', font=serif, fill='#eee7cb')
d.text((44, 132), 'full stack developer', font=mono, fill='#c6cfb3')

sheet = Image.open(ASSETS/'fox-walk-sheet.png').convert('RGBA')
sprites = []
for i in range(8):
    col, row = i % 4, i // 4
    tile = sheet.crop((round(col*sheet.width/4), round(row*sheet.height/2),
                       round((col+1)*sheet.width/4), round((row+1)*sheet.height/2)))
    # Disregard faint alpha dust when finding the animal's baseline.
    bounds = tile.getchannel('A').point(lambda a: 255 if a > 80 else 0).getbbox()
    tile = tile.crop(bounds)
    tile.thumbnail((126, 83), Image.Resampling.LANCZOS)
    sprites.append(tile)
frames = []
for n in range(COUNT):
    frame = bg.copy()
    sprite = sprites[n % 8]
    # Leave and re-enter fully off-canvas for a continuous looping journey.
    x = round(-132 + (W + 264)*n/COUNT)
    frame.paste(sprite, (x, 228-sprite.height), sprite)
    frames.append(frame)
# One shared palette prevents color flicker between GIF frames.
palette_source = bg.copy()
for i, sprite in enumerate(sprites):
    palette_source.paste(sprite, ((i%6)*145, (i//6)*90), sprite)
palette = palette_source.quantize(colors=256)
encoded = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
encoded[0].save(ASSETS/'woodland-fox.gif', save_all=True, append_images=encoded[1:],
                duration=100, loop=0, optimize=True, disposal=1)
frames[100].save(ASSETS/'woodland-fox-still.png')
print(f'Saved {COUNT} frames / 20 seconds to {ASSETS / "woodland-fox.gif"}')
