"""Build the profile's night-sky body headings, bio panel, and contact footer."""
from pathlib import Path
from night_style import panel,text
OUT=Path(__file__).resolve().parents[1]/'assets'
for name,title,kicker in [
    ('toolkit','My toolkit','TOOLS I WORK WITH'),
    ('certifications','AWS certified','CLOUD CREDENTIALS'),
    ('activity','Keeping the streak going','A LITTLE EVERY DAY'),
]:
    p=panel(960,100,title)
    p+=[text(30,30,kicker,12,'#a7b5dc',extra='letter-spacing="2"'),text(28,70,title,30,'#f0edff',font='Georgia,serif'),'</svg>']
    (OUT/f'night-section-{name}.svg').write_text(''.join(p)+'\n')
p=panel(680,270,'From interface to infrastructure')
p+=[text(28,40,'From interface to infrastructure',27,'#f0edff',font='Georgia,serif'),
    text(28,78,'I build web applications and the cloud infrastructure',18),
    text(28,105,'behind them, with a focus on clear code and usable interfaces.',18),
    text(28,148,'CURRENT FOCUS',11,'#b3bce6',extra='letter-spacing="2"'),
    text(28,179,'React, Vue, and Laravel applications',18),
    text(28,211,'AWS infrastructure and cloud architecture',18),
    text(28,243,'Learning distributed systems',18),'</svg>']
(OUT/'night-about.svg').write_text(''.join(p)+'\n')
p=panel(960,160,"Have a product in mind? Let's talk on LinkedIn.")
p+=[text(30,34,'LET\'S BUILD SOMETHING USEFUL',12,'#b9c7e9',extra='letter-spacing="2"'),
    text(28,80,'Have a product in mind?',32,'#f0edff',font='Georgia,serif'),
    text(30,123,"Let's talk on LinkedIn →",19,'#c0d4ff'),'</svg>']
(OUT/'night-footer.svg').write_text(''.join(p)+'\n')
# Compact variants retain readable text when GitHub renders on a phone.
for name,title,kicker in [
    ('toolkit','My toolkit','TOOLS I WORK WITH'),
    ('certifications','AWS certified','CLOUD CREDENTIALS'),
    ('activity','Keeping the streak going','A LITTLE EVERY DAY'),
]:
    p=panel(420,94,title)
    p+=[text(20,29,kicker,11,'#a7b5dc',extra='letter-spacing="1.5"'),text(20,65,title,25,'#f0edff',font='Georgia,serif'),'</svg>']
    (OUT/f'night-section-{name}-mobile.svg').write_text(''.join(p)+'\n')
p=panel(420,338,'From interface to infrastructure')
for x,y,content,size,color,font in [
    (22,35,'From interface',26,'#f0edff','Georgia,serif'),
    (22,66,'to infrastructure',26,'#f0edff','Georgia,serif'),
    (22,105,'I build web applications and the cloud',17,'#dce4f4','Verdana,sans-serif'),
    (22,132,'infrastructure behind them, with a focus',17,'#dce4f4','Verdana,sans-serif'),
    (22,159,'on clear code and usable interfaces.',17,'#dce4f4','Verdana,sans-serif'),
    (22,202,'CURRENT FOCUS',11,'#b3bce6','Verdana,sans-serif'),
    (22,234,'React, Vue, and Laravel applications',17,'#dce4f4','Verdana,sans-serif'),
    (22,263,'AWS infrastructure and cloud architecture',16,'#dce4f4','Verdana,sans-serif'),
    (22,292,'Learning distributed systems',17,'#dce4f4','Verdana,sans-serif'),
]:p.append(text(x,y,content,size,color,font))
p.append('</svg>');(OUT/'night-about-mobile.svg').write_text(''.join(p)+'\n')
p=panel(420,160,"Have a product in mind? Let's talk on LinkedIn.")
p+=[text(20,30,"LET'S BUILD SOMETHING USEFUL",10,'#b9c7e9',extra='letter-spacing="1"'),text(20,75,'Have a product in mind?',28,'#f0edff',font='Georgia,serif'),text(20,119,"Let's talk on LinkedIn →",18,'#c0d4ff'),'</svg>']
(OUT/'night-footer-mobile.svg').write_text(''.join(p)+'\n')
