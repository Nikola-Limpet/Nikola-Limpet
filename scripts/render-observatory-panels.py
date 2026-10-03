"""Render restrained profile panels from the night-observatory concept.

SVGs contain no scripts, external fonts, images, or foreignObject elements.
Run from any directory with: python3 scripts/render-observatory-panels.py
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets'
INK = '#0b1120'
CREAM = '#f2ebdf'
BODY = '#cbd5e5'
COOL = '#96b4d8'
RULE = '#35465e'
SERIF = 'Georgia,Times New Roman,serif'
SANS = 'Verdana,sans-serif'


def text(x, y, content, size=17, color=BODY, font=SANS, extra=''):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" '
            f'font-size="{size}" {extra}>{escape(content)}</text>')


def start(width, height, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">',
            f'<title id="title">{escape(title)}</title>',
            f'<rect width="{width}" height="{height}" fill="{INK}"/>']


def star(x, y, scale=1):
    return (f'<path transform="translate({x} {y}) scale({scale})" '
            f'd="M0 -12 L2 -3 L9 -6 L4 0 L12 2 L3 3 L0 12 L-2 3 L-9 6 L-4 0 L-12 -2 L-3 -3 Z" '
            f'fill="{COOL}" opacity=".85"/>')


def constellation(x1, x2, y):
    mid = x1 + (x2 - x1) * .68
    return (f'<path d="M{x1} {y} H{mid - 15} L{mid} {y - 4} L{mid + 15} {y} H{x2}" '
            f'fill="none" stroke="{RULE}" stroke-width="1"/>'
            f'<circle cx="{mid}" cy="{y - 4}" r="2" fill="{COOL}"/>'
            f'<circle cx="{mid + 15}" cy="{y}" r="1.5" fill="{COOL}"/>')


def write(name, parts):
    (OUT / f'{name}.svg').write_text('\n'.join(parts + ['</svg>']) + '\n')


def heading(name, title, label, rule_start, mobile=False):
    w, h = (420, 72) if mobile else (960, 64)
    p = start(w, h, title)
    if mobile:
        p += [star(25, 27, .7), text(46, 35, title, 26, CREAM, SERIF),
              constellation(20, 400, 54)]
    else:
        p += [star(30, 32), text(65, 42, title, 30, CREAM, SERIF),
              constellation(rule_start, 678, 32),
              text(925, 36, label, 10, COOL, extra='text-anchor="end" letter-spacing="2"')]
    write(f'observatory-heading-{name}' + ('-mobile' if mobile else ''), p)


def about(mobile=False):
    w, h = (420, 310) if mobile else (960, 190)
    p = start(w, h, 'About Yuujin and current focus')
    if mobile:
        p += [star(25, 27, .7), text(46, 35, 'About', 26, CREAM, SERIF),
              constellation(144, 400, 27)]
        for y, line in [(76, 'I build web applications and the cloud'),
                        (103, 'infrastructure behind them, with a focus'),
                        (130, 'on clear code and usable interfaces.')]:
            p.append(text(20, y, line))
        p.append(text(20, 174, 'CURRENT FOCUS', 10, COOL, extra='letter-spacing="2.5"'))
        for y, line in [(204, 'React, Vue, and Laravel applications'),
                        (231, 'AWS infrastructure and cloud architecture'),
                        (258, 'Learning distributed systems')]:
            p.append(text(20, y, line, 16 if y == 231 else 17))
        p.append(constellation(20, 400, 291))
    else:
        p += [star(30, 32), text(65, 42, 'About', 30, CREAM, SERIF),
              constellation(157, 925, 32),
              text(65, 87, 'I build web applications and the cloud', 18, BODY, SERIF),
              text(65, 116, 'infrastructure behind them, with a focus', 18, BODY, SERIF),
              text(65, 145, 'on clear code and usable interfaces.', 18, BODY, SERIF),
              text(530, 78, 'CURRENT FOCUS', 10, COOL, extra='letter-spacing="2.5"'),
              text(530, 108, 'React, Vue, and Laravel applications', 16),
              text(530, 134, 'AWS infrastructure and cloud architecture', 16),
              text(530, 160, 'Learning distributed systems', 16)]
    write('observatory-about' + ('-mobile' if mobile else ''), p)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for mobile in (False, True):
        about(mobile)
        for args in [('toolkit', 'Toolkit', 'TOOLS I WORK WITH', 181),
                     ('certifications', 'AWS certified', 'CLOUD CREDENTIALS', 263),
                     ('activity', 'Activity', 'GITHUB CONTRIBUTIONS', 193)]:
            heading(*args, mobile=mobile)
