"""Build labeled SVG icon rows from the vendored Devicon artwork."""
from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape
ROOT=Path(__file__).resolve().parents[1]
NS='http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
GROUPS={
'frontend':[('react','React'),('nextjs','Next.js'),('vuejs','Vue'),('typescript','TypeScript'),('javascript','JavaScript'),('tailwindcss','Tailwind')],
'backend':[('laravel','Laravel'),('php','PHP'),('go','Go'),('nodejs','Node.js'),('python','Python')],
'data':[('postgresql','PostgreSQL'),('mysql','MySQL'),('mongodb','MongoDB'),('sqlite','SQLite'),('prisma','Prisma')],
'cloud':[('amazonwebservices','AWS'),('cloudflare','Cloudflare'),('docker','Docker'),('linux','Linux'),('git','Git')],
}
for group,items in GROUPS.items():
    parts=[f'<svg xmlns="{NS}" width="600" height="94" viewBox="0 0 600 94" role="img"><title>{escape(", ".join(label for _,label in items))}</title>']
    for i,(name,label) in enumerate(items):
        x=i*100
        parts.append(f'<rect x="{x+22}" y="2" width="56" height="56" rx="14" fill="#e5eaf3"/>')
        icon=ET.fromstring((ROOT/f'assets/icons/{name}.svg').read_text())
        icon.attrib.update(x=str(x+32),y='12',width='36',height='36')
        parts.append(ET.tostring(icon,encoding='unicode'))
        parts.append(f'<rect x="{x+1}" y="64" width="98" height="23" rx="6" fill="#18243a"/><text x="{x+50}" y="79" text-anchor="middle" fill="#e2e8f2" font-family="Verdana,sans-serif" font-size="11">{escape(label)}</text>')
    parts.append('</svg>')
    (ROOT/f'assets/toolkit-{group}.svg').write_text(''.join(parts)+'\n')
