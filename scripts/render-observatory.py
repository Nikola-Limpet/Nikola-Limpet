"""Render the imagegen observatory landscape with editable text and walk cycles.

Requires Pillow and DejaVu fonts. Override FONT_DIR if needed.
Run: python scripts/render-observatory.py
"""
from pathlib import Path
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
FONT_DIR = Path(os.environ.get('FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
W, H, COUNT = 960, 320, 240
bg = Image.open(ASSETS/'observatory-landscape.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
d = ImageDraw.Draw(bg)
# The generated artwork supplies the landscape. Text and animation stay editable.
serif=ImageFont.truetype(str(FONT_DIR/'DejaVuSerif.ttf'),60)
body=ImageFont.truetype(str(FONT_DIR/'DejaVuSans.ttf'),19)
small=ImageFont.truetype(str(FONT_DIR/'DejaVuSansMono.ttf'),12)
d.text((38,60),'Yuujin',font=serif,fill='#f4ecdb',stroke_width=1,stroke_fill='#0b1120')
d.text((40,136),'Full stack developer',font=body,fill='#e0e5f0',stroke_width=1,stroke_fill='#0b1120')
d.text((40,174),'Phnom Penh, Cambodia',font=small,fill='#b3c6e6',stroke_width=1,stroke_fill='#0b1120')
stars=[(612,38,0),(707,72,1),(900,102,2),(494,25,3),(765,28,4)]

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

animals=[(load_cycle('fox',(98,65)),0,False),
         (load_cycle('rabbit',(61,59)),80,False),
         (load_cycle('cat',(78,65)),160,False)]
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
        frame.paste(sprite,(x,294-sprite.height),sprite)
    frames.append(frame)
# A shared palette keeps star and animal colors stable.
palette_source=bg.copy()
for row,(sprites,_,_) in enumerate(animals):
    for i,sprite in enumerate(sprites):palette_source.paste(sprite,(i*120,row*85),sprite)
palette=palette_source.quantize(colors=256)
encoded=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
encoded[0].save(ASSETS/'observatory-hero.gif',save_all=True,append_images=encoded[1:],duration=100,loop=0,optimize=True,disposal=1)
frames[104].save(ASSETS/'observatory-hero-still.png')
print(f'Saved {COUNT} frames, 24 seconds, three animal cycles.')

# A compact panorama closes the page after the live quote.
footer=Image.open(ASSETS/'observatory-landscape.png').convert('RGB')
footer=ImageOps.fit(footer,(960,200),method=Image.Resampling.LANCZOS,centering=(0.5,0.67))
draw=ImageDraw.Draw(footer)
headline=ImageFont.truetype(str(FONT_DIR/'DejaVuSerif.ttf'),31)
link=ImageFont.truetype(str(FONT_DIR/'DejaVuSans.ttf'),19)
draw.text((32,55),'Have a product in mind?',font=headline,fill='#f4ecdb',stroke_width=1,stroke_fill='#0b1120')
draw.text((34,108),"Let's talk on LinkedIn →",font=link,fill='#b9d5ff',stroke_width=1,stroke_fill='#0b1120')
footer.save(ASSETS/'observatory-footer.webp',quality=90)
# Mobile footer keeps the CTA readable without tiny scaled lettering.
compact=ImageOps.fit(Image.open(ASSETS/'observatory-landscape.png').convert('RGB'),(420,180),method=Image.Resampling.LANCZOS,centering=(0.35,0.65))
draw=ImageDraw.Draw(compact)
draw.text((20,45),'Have a product in mind?',font=ImageFont.truetype(str(FONT_DIR/'DejaVuSerif.ttf'),26),fill='#f4ecdb',stroke_width=1,stroke_fill='#0b1120')
draw.text((22,100),"Let's talk on LinkedIn →",font=ImageFont.truetype(str(FONT_DIR/'DejaVuSans.ttf'),18),fill='#b9d5ff',stroke_width=1,stroke_fill='#0b1120')
compact.save(ASSETS/'observatory-footer-mobile.webp',quality=90)
# A separate mobile animation keeps the identity text readable on narrow screens.
mobile_bg=ImageOps.fit(Image.open(ASSETS/'observatory-landscape.png').convert('RGB'),(420,260),method=Image.Resampling.LANCZOS,centering=(0.55,0.5))
draw=ImageDraw.Draw(mobile_bg)
draw.text((20,28),'Yuujin',font=ImageFont.truetype(str(FONT_DIR/'DejaVuSerif.ttf'),40),fill='#f4ecdb',stroke_width=1,stroke_fill='#0b1120')
draw.text((22,83),'Full stack developer',font=ImageFont.truetype(str(FONT_DIR/'DejaVuSans.ttf'),16),fill='#e0e5f0',stroke_width=1,stroke_fill='#0b1120')
draw.text((22,112),'Phnom Penh, Cambodia',font=ImageFont.truetype(str(FONT_DIR/'DejaVuSansMono.ttf'),11),fill='#b3c6e6',stroke_width=1,stroke_fill='#0b1120')
mobile_frames=[]
for n in range(COUNT):
    frame=mobile_bg.copy();draw=ImageDraw.Draw(frame)
    t=n%80
    if 18<=t<31:
        x=210+(t-18)*13;y=14+(t-18)*4
        draw.line((x-32,y-10,x,y),fill='#b5c6e7',width=1)
        draw.point((x,y),fill='#fff1d4')
    for sprites,offset,_ in animals:
        sprite=sprites[n%8]
        sprite=sprite.resize((round(sprite.width*.72),round(sprite.height*.72)),Image.Resampling.LANCZOS)
        x=round(-90+600*((n+offset)%COUNT)/COUNT)
        frame.paste(sprite,(x,244-sprite.height),sprite)
    mobile_frames.append(frame)
mobile_encoded=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in mobile_frames]
mobile_encoded[0].save(ASSETS/'observatory-hero-mobile.gif',save_all=True,append_images=mobile_encoded[1:],duration=100,loop=0,optimize=True,disposal=1)
