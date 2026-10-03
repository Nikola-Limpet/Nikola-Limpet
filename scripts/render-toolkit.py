"""Build labeled SVG icon rows from the vendored Devicon artwork."""
from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape
from night_style import panel,text
ROOT=Path(__file__).resolve().parents[1]
NS='http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
GROUPS={
'frontend':[('react','React'),('nextjs','Next.js'),('vuejs','Vue'),('typescript','TypeScript'),('javascript','JavaScript'),('tailwindcss','Tailwind')],
'backend':[('laravel','Laravel'),('php','PHP'),('go','Go'),('nodejs','Node.js'),('python','Python')],
'data':[('postgresql','PostgreSQL'),('mysql','MySQL'),('mongodb','MongoDB'),('sqlite','SQLite'),('prisma','Prisma')],
'cloud':[('amazonwebservices','AWS'),('cloudflare','Cloudflare'),('docker','Docker'),('linux','Linux'),('git','Git')],
}
LABELS={
'frontend':('Interfaces','React Native · TanStack · Redux · Vite'),
'backend':('APIs & services','Express · Flask'),
'data':('Data','Drizzle'),
'cloud':('Cloud & tools','Railway · Bash'),
}
for group,items in GROUPS.items():
    title,extras=LABELS[group]
    parts=panel(680,190,title+': '+', '.join(label for _,label in items)+'; '+extras)
    parts.append(text(26,35,title,23,'#f0edff',font='Georgia,serif'))
    for i,(name,label) in enumerate(items):
        x=28+i*104
        parts.append(f'<rect x="{x+17}" y="54" width="56" height="56" rx="14" fill="#dce3f3"/>')
        icon=ET.fromstring((ROOT/f'assets/icons/{name}.svg').read_text())
        icon.attrib.update(x=str(x+27),y='64',width='36',height='36')
        parts.append(ET.tostring(icon,encoding='unicode'))
        parts.append(text(x+45,131,label,12,extra='text-anchor="middle"'))
    parts.append(text(28,171,extras,13,'#b6c5e6'))
    parts.append('</svg>')
    (ROOT/f'assets/toolkit-{group}.svg').write_text(''.join(parts)+'\n')
# Two rows of three icons keep labels legible at phone width.
for group,items in GROUPS.items():
    title,extras=LABELS[group]
    parts=panel(390,292,title+': '+', '.join(label for _,label in items)+'; '+extras)
    parts.append(text(20,34,title,24,'#f0edff',font='Georgia,serif'))
    for i,(name,label) in enumerate(items):
        x=20+(i%3)*119;y=55+(i//3)*92
        parts.append(f'<rect x="{x+24}" y="{y}" width="56" height="56" rx="14" fill="#dce3f3"/>')
        icon=ET.fromstring((ROOT/f'assets/icons/{name}.svg').read_text())
        icon.attrib.update(x=str(x+34),y=str(y+10),width='36',height='36')
        parts.append(ET.tostring(icon,encoding='unicode'))
        parts.append(text(x+52,y+76,label,13,extra='text-anchor="middle"'))
    parts.append(text(20,267,extras,12,'#b6c5e6'))
    parts.append('</svg>')
    (ROOT/f'assets/toolkit-{group}-mobile.svg').write_text(''.join(parts)+'\n')
