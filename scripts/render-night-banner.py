"""Render a 24-second night-sky banner from generated animal walk cycles.

Requires Pillow and DejaVu fonts. Override FONT_DIR if needed.
Run: python scripts/render-night-banner.py
"""
from pathlib import Path
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
FONT_DIR = Path(os.environ.get('FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
W, H, COUNT = 960, 280, 240
bg = Image.new('RGB', (W, H), '#0d1426')
d = ImageDraw.Draw(bg)
d.rounded_rectangle((1, 1, W-2, H-2), 18, outline='#303e5a', width=2)
rng = random.Random(13)
stars = []
for _ in range(100):
    x, y = rng.randrange(20, W-20), rng.randrange(12, 214)
    if 34 < x < 510 and 42 < y < 183:
        continue
    d.point((x, y), fill=rng.choice(['#576787', '#8c9fbe', '#c1c9d6']))
    if len(stars) < 12 and x > 530:
        stars.append((x, y, rng.random()*math.tau))
d.ellipse((826, 40, 862, 76), fill='#eee4c4')
d.ellipse((837, 34, 870, 67), fill='#0d1426')
# Distant hills leave a clear path for the animals.
d.polygon([(0,244),(140,206),(300,243),(470,215),(680,239),(820,205),(960,241),(960,280),(0,280)],fill='#141f34')
d.polygon([(0,263),(215,239),(360,262),(585,237),(780,259),(960,234),(960,280),(0,280)],fill='#1a293b')
d.line((20,253,940,253),fill='#42536a')
serif=ImageFont.truetype(str(FONT_DIR/'DejaVuSerif.ttf'),54)
mono=ImageFont.truetype(str(FONT_DIR/'DejaVuSansMono.ttf'),14)
small=ImageFont.truetype(str(FONT_DIR/'DejaVuSansMono.ttf'),11)
d.text((44,36),'PHNOM PENH / CAMBODIA',font=small,fill='#9caecd')
d.text((40,66),'Yuujin',font=serif,fill='#f0e8d0')
d.text((44,140),'full stack developer',font=mono,fill='#c2cce0')

def load_cycle(name, size, flip=False):
    sheet=Image.open(ASSETS/f'{name}-walk-sheet.png').convert('RGBA')
    sprites=[]
    for i in range(8):
        col,row=i%4,i//4
        tile=sheet.crop((round(col*sheet.width/4),round(row*sheet.height/2),round((col+1)*sheet.width/4),round((row+1)*sheet.height/2)))
        bounds=tile.getchannel('A').point(lambda a:255 if a>80 else 0).getbbox()
        if bounds is None:
            raise ValueError(f'Empty sprite: {name}, frame {i}')
        tile=tile.crop(bounds)
        tile.thumbnail(size,Image.Resampling.LANCZOS)
        sprites.append(ImageOps.mirror(tile) if flip else tile)
    return sprites

animals=[(load_cycle('fox',(118,78)),0,False),
         (load_cycle('rabbit',(74,71)),80,False),
         (load_cycle('cat',(94,78)),160,False)]
frames=[]
for n in range(COUNT):
    frame=bg.copy();draw=ImageDraw.Draw(frame)
    for x,y,phase in stars:
        brightness=(1+math.sin(math.tau*n/80+phase))/2
        v=round(85+145*brightness)
        draw.point((x,y),fill=(v,v,min(v+22,255)))
        if brightness>0.92:
            draw.line((x-2,y,x+2,y),fill='#778caf')
            draw.line((x,y-2,x,y+2),fill='#778caf')
    for start in (18,98,178):
        t=n-start
        if 0<=t<13:
            x=570+t*24;y=18+t*8
            for j in range(36):
                fade=1-j/36
                color=tuple(round(a+(b-a)*fade) for a,b in zip((13,20,38),(207,222,246)))
                draw.line((x-j*3,y-j,x-j*3+3,y-j+1),fill=color,width=1)
            draw.ellipse((x-1,y-1,x+1,y+1),fill='#fff1d4')
    for sprites,offset,reverse in animals:
        progress=((n+offset)%COUNT)/COUNT
        x=round(-132+(W+264)*progress)
        if reverse:x=W-x-118
        sprite=sprites[n%8]
        frame.paste(sprite,(x,252-sprite.height),sprite)
    frames.append(frame)
# A shared palette keeps star and animal colors stable.
palette_source=bg.copy()
for row,(sprites,_,_) in enumerate(animals):
    for i,sprite in enumerate(sprites):palette_source.paste(sprite,(i*120,row*85),sprite)
palette=palette_source.quantize(colors=256)
encoded=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
encoded[0].save(ASSETS/'night-animals.gif',save_all=True,append_images=encoded[1:],duration=100,loop=0,optimize=True,disposal=1)
frames[104].save(ASSETS/'night-animals-still.png')
print(f'Saved {COUNT} frames, 24 seconds, three animal cycles.')
