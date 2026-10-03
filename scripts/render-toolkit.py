"""Render the responsive night-observatory toolkit from vendored Devicon SVGs."""
from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape

ROOT = Path(__file__).resolve().parents[1]
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
GROUPS = {
    'frontend': [('react', 'React'), ('nextjs', 'Next.js'), ('vuejs', 'Vue'), ('typescript', 'TypeScript'), ('javascript', 'JavaScript'), ('tailwindcss', 'Tailwind')],
    'backend': [('laravel', 'Laravel'), ('php', 'PHP'), ('go', 'Go'), ('nodejs', 'Node.js'), ('python', 'Python')],
    'data': [('postgresql', 'PostgreSQL'), ('mysql', 'MySQL'), ('mongodb', 'MongoDB'), ('sqlite', 'SQLite'), ('prisma', 'Prisma')],
    'cloud': [('amazonwebservices', 'AWS'), ('cloudflare', 'Cloudflare'), ('docker', 'Docker'), ('linux', 'Linux'), ('git', 'Git')],
}
LABELS = {
    'frontend': ('Interfaces', 'React Native · TanStack · Redux · Vite'),
    'backend': ('APIs & services', 'Express · Flask'),
    'data': ('Data', 'Drizzle'),
    'cloud': ('Cloud & tools', 'Railway · Bash'),
}


def text(x, y, value, size=15, color='#e9e4de', **attrs):
    attr = ' '.join(f'{key.replace("_", "-")}="{escape(str(value), quote=True)}"' for key, value in attrs.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {attr}>{escape(value)}</text>'


def icon(name, x, y, size=27):
    node = ET.fromstring((ROOT / f'assets/icons/{name}.svg').read_text())
    # Prefix gradient IDs so each vendored icon remains independent in the atlas.
    ids = {el.attrib['id']: f'{name}-{el.attrib["id"]}' for el in node.iter() if 'id' in el.attrib}
    for el in node.iter():
        for key, value in list(el.attrib.items()):
            if key == 'id':
                el.set(key, ids[value])
            else:
                for old, new in ids.items():
                    value = value.replace(f'url(#{old})', f'url(#{new})')
                el.set(key, value)
        # Monochrome wordmarks use the atlas's pale ink to retain contrast.
        if name in ('prisma', 'amazonwebservices') and el.get('fill') in ('#2d3748', '#252f3e'):
            el.set('fill', '#d6dcec')
    node.attrib.update(x=str(x), y=str(y), width=str(size), height=str(size))
    backdrop = ''
    if name in ('nextjs', 'linux'):
        backdrop = f'<circle cx="{x+size/2}" cy="{y+size/2}" r="{size/2+2}" fill="#33405a"/>'
    return backdrop + ET.tostring(node, encoding='unicode')


def render(mobile=False):
    width, height = (420, 840) if mobile else (960, 400)
    description = '; '.join(LABELS[key][0] + ': ' + ', '.join(label for _, label in items) + '; ' + LABELS[key][1] for key, items in GROUPS.items())
    parts = [f'<svg xmlns="{NS}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">Toolkit</title>', f'<desc id="desc">{escape(description)}</desc>',
             f'<rect width="{width}" height="{height}" fill="#0b1120"/>',
             '<g font-family="Georgia, Times New Roman, serif">']
    row_height = 210 if mobile else 100
    for row, (group, items) in enumerate(GROUPS.items()):
        y = row * row_height
        title, extras = LABELS[group]
        parts.append(f'<path d="M20 {y+.5}H{width-20}" stroke="#2b3448"/>')
        if mobile:
            parts.append(text(22, y+29, title, 18))
            for i, (name, label) in enumerate(items):
                x, top = 22+(i % 3)*128, y+51+(i//3)*50
                parts.append(icon(name, x, top, 25))
                parts.append(text(x+34, top+18, label, 14))
            extra_lines = ['React Native · TanStack', 'Redux · Vite'] if group == 'frontend' else [extras]
            for i, line in enumerate(extra_lines):
                parts.append(text(22, y+170+i*21, line, 14, '#aeb4d1', font_family='Verdana, sans-serif'))
        else:
            parts.append(text(24, y+39, title, 18))
            parts.append(text(24, y+65, f'0{row+1}', 11, '#929bbc', font_family='Verdana, sans-serif', letter_spacing=2))
            for i, (name, label) in enumerate(items):
                x = 200+i*123
                parts.append(icon(name, x, y+23))
                parts.append(text(x+36, y+42, label, 14))
            parts.append(text(200, y+77, extras, 13, '#aeb4d1', font_family='Verdana, sans-serif'))
    parts += [f'<path d="M20 {height-.5}H{width-20}" stroke="#2b3448"/>', '</g></svg>']
    target = ROOT / ('assets/toolkit-atlas-mobile.svg' if mobile else 'assets/toolkit-atlas.svg')
    target.write_text(''.join(parts)+'\n')


if __name__ == '__main__':
    render()
    render(mobile=True)
