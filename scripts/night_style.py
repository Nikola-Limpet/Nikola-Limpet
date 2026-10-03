"""Shared SVG night-sky styling for the profile's static panels."""
from html import escape
import random


def panel(width, height, title):
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title>',f'''<defs>
<linearGradient id="sky" x2="1" y2="0.5"><stop stop-color="#091226"/><stop offset="0.55" stop-color="#19204b"/><stop offset="1" stop-color="#301548"/></linearGradient>
<radialGradient id="glow"><stop stop-color="#638ee1" stop-opacity="0.36"/><stop offset="1" stop-color="#638ee1" stop-opacity="0"/></radialGradient>
<clipPath id="bounds"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16"/></clipPath>
</defs><g clip-path="url(#bounds)"><rect width="{width}" height="{height}" fill="url(#sky)"/>
<ellipse cx="{width*0.15}" cy="{height*1.12}" rx="{width*0.3}" ry="{height*0.8}" fill="url(#glow)"/>''']
    rng=random.Random(width+height)
    for _ in range(width//18):
        x,y=rng.randrange(12,width-12),rng.randrange(8,height-8)
        # Keep the left text area quiet and put most stars above the content.
        if y>height*0.32 and x<width*0.65:continue
        parts.append(f'<circle cx="{x}" cy="{y}" r="{rng.choice([0.6,0.8,1])}" fill="#d5dcf7" opacity="{rng.choice([0.35,0.5,0.7])}"/>')
    for x,y in [(width*0.83,height*0.26),(width*0.92,height*0.69)]:
        parts.append(f'<path d="M{x-3} {y}h6M{x} {y-3}v6" stroke="#a8b8e6" stroke-width="0.8" opacity="0.6"/>')
    parts.append(f'</g><rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="16" fill="none" stroke="#354064"/>')
    return parts


def text(x,y,content,size=18,color='#dce4f4',font='Verdana,sans-serif',extra=''):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" {extra}>{escape(content)}</text>'
