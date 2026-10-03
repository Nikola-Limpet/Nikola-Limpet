"""Compose editable SVG content over the generated continuous body background.

Run: uv run --with pillow --with cairosvg python scripts/render-observatory-body.py
The SVG sources stay editable; PNG exports avoid nested-image SVG restrictions.
"""
from pathlib import Path
from io import BytesIO
import xml.etree.ElementTree as ET
from PIL import Image
import os

# Keep Linux font aliases from silently substituting unrelated user fonts.
config=Path(__file__).with_name("observatory-fonts.conf")
if Path("/usr/share/fonts/truetype/dejavu").is_dir():
    os.environ.setdefault("FONTCONFIG_FILE",str(config))
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
BACKGROUND=Image.open(ASSETS/'observatory-body-background.png').convert('RGBA')

def foreground(name):
    svg=ET.parse(ASSETS/name).getroot()
    width,height=map(int,(svg.get('width'),svg.get('height')))
    # Remove only the root's full-size ink rectangle; retain all icon fills.
    for child in list(svg):
        if child.tag==f'{{{NS}}}rect' and child.get('width')==str(width) and child.get('height')==str(height) and child.get('fill')=='#0b1120':
            svg.remove(child)
    # Resolve portable fonts explicitly; system aliases may map to monospace.
    for element in svg.iter():
        family=element.get('font-family','')
        if 'Georgia' in family or 'Times' in family:
            element.set('font-family','DejaVu Serif')
        elif 'Verdana' in family or 'sans-serif' in family:
            element.set('font-family','DejaVu Sans')
    png=cairosvg.svg2png(bytestring=ET.tostring(svg),output_width=width*2,output_height=height*2)
    return Image.open(BytesIO(png)).convert('RGBA'),width,height

for mobile in (False,True):
    suffix='-mobile' if mobile else ''
    names=[f'observatory-about{suffix}.svg',f'observatory-heading-toolkit{suffix}.svg',f'toolkit-atlas{suffix}.svg',f'observatory-heading-certifications{suffix}.svg']
    layers=[foreground(name) for name in names]
    width=layers[0][1];height=sum(layer[2] for layer in layers)
    # Use a continuous top-to-bottom field, including the lower forest silhouettes.
    bg=BACKGROUND.resize((width*2,height*2),Image.Resampling.LANCZOS)
    # The artwork stays at the edges; a light ink wash protects text contrast.
    bg=Image.alpha_composite(bg,Image.new('RGBA',bg.size,(5,10,22,48)))
    y=0
    for layer,_,h in layers:
        bg.alpha_composite(layer,(0,y*2));y+=h
    bg.convert('RGB').save(ASSETS/f'observatory-body{suffix}.png',optimize=True)
    # Activity keeps the same border atmosphere while stats remain live below it.
    layer,w,h=foreground(f'observatory-heading-activity{suffix}.svg')
    backdrop=BACKGROUND.crop((0,round(BACKGROUND.height*.58),BACKGROUND.width,round(BACKGROUND.height*.72))).resize((w*2,h*2),Image.Resampling.LANCZOS)
    backdrop=Image.alpha_composite(backdrop,Image.new('RGBA',backdrop.size,(5,10,22,48)))
    backdrop.alpha_composite(layer)
    backdrop.convert('RGB').save(ASSETS/f'observatory-activity{suffix}.png',optimize=True)
    print(f'{suffix or "desktop"}: continuous body {width}×{height}, exported at 2×')
