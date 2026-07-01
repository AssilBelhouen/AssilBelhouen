"""Original neofetch-style profile artwork; no third-party artwork is copied."""
import argparse
from html import escape
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BG,WHITE,GREEN,MUTED='#0D1410','#DCE6DF','#00FF88','#859189'

def portrait(path,columns=44):
    image=ImageOps.fit(Image.open(path).convert('RGB'),(1254,1254))
    mask=Image.new('L',image.size)
    ImageDraw.Draw(mask).polygon([(440,180),(495,119),(650,106),(741,135),(790,223),
        (810,385),(831,423),(827,487),(802,520),(775,535),(770,650),(801,717),
        (912,772),(1070,825),(1190,880),(1254,1090),(1254,1254),(0,1254),
        (97,907),(234,835),(355,768),(465,695),(477,579),(450,538),(419,522),
        (400,455),(403,421),(424,406),(409,324),(420,241)],fill=255)
    crop=(280,90,980,1010)
    rows=round((crop[3]-crop[1])/(crop[2]-crop[0])*columns*.5)
    gray=ImageEnhance.Contrast(ImageOps.grayscale(image.crop(crop))).enhance(1.12)
    gray=gray.resize((columns,rows),Image.Resampling.LANCZOS)
    mask=mask.crop(crop).resize((columns,rows),Image.Resampling.LANCZOS)
    ramp=' .,:;i!+tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    return [''.join(ramp[min(len(ramp)-1,int((1-gray.getpixel((x,y))/255)*(len(ramp)-1)))]
        if mask.getpixel((x,y))>150 else ' ' for x in range(columns)) for y in range(rows)]

def text(x,y,value,size=17,color=WHITE,weight='400'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(value)}</text>'

def base(w,h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
        '<title id="title">Assil Belhouene — terminal profile</title>',
        '<desc id="desc">Compact monochrome ASCII portrait beside a neofetch-style summary of Assil’s engineering profile.</desc>',
        f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>',
        '<g font-family="Consolas, Liberation Mono, monospace">']

def ascii_text(lines,x,y,cell=8,line=16,size=14):
    return ''.join(text(x+col*cell,y+row*line,char,size) for row,chars in enumerate(lines)
        for col,char in enumerate(chars) if char!=' ')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--photo',required=True)
    parser.add_argument('--preview-dir'); args=parser.parse_args()
    lines=portrait(args.photo); assets=ROOT/'assets'; assets.mkdir(exist_ok=True)
    (assets/'portrait.txt').write_text('\n'.join(row.rstrip() for row in lines)+'\n',encoding='ascii')
    parts=base(1100,620)
    parts += [text(30,40,'assil@cloud:~$ neofetch',16,GREEN),
        '<path d="M30 61H1070" stroke="#26382D"/>',ascii_text(lines,30,111),
        text(435,112,'assil@cloud',22,GREEN,'700'),text(435,141,'----------------------------------------',16,MUTED)]
    fields=[('Name','Assil Belhouene'),('Role','Cloud / DevOps / Full-Stack'),
        ('Based in','Kelibia, Tunisia'),('Cloud','AWS / Azure / OpenStack'),
        ('Platform','Kubernetes / Talos / Docker'),('Delivery','CI/CD / GitOps / Automation'),
        ('Languages','Go / Java / TypeScript / Python'),('Education','ESPRIT · Cloud Computing, 2026')]
    for i,(label,value) in enumerate(fields):
        y=175+i*29
        parts += [text(435,y,label+':',16,GREEN),text(550,y,value,16)]
    parts += [text(435,440,'-- Selected work -----------------------',15,MUTED),
        text(435,470,'Forginet / Gamax / Veridia / Gravitech',16),
        text(435,514,'I engineer systems that keep shipping.',18,WHITE,'700'),
        text(435,551,'Design → Automate → Operate with evidence',15,MUTED)]
    for i,color in enumerate(['#355443','#538466','#859189','#B0C9B9',GREEN,WHITE]):
        parts.append(f'<rect x="{435+i*28}" y="577" width="28" height="15" fill="{color}"/>')
    parts += ['</g></svg>']; (assets/'hero.svg').write_text('\n'.join(parts),encoding='utf-8')
    parts=base(432,820)
    parts += [text(28,40,'assil@cloud:~$ neofetch',16,GREEN),ascii_text(lines,40,90),
        text(28,600,'assil@cloud',21,GREEN,'700'),text(28,634,'Cloud / DevOps / Full-Stack',17),
        text(28,667,'Kelibia, Tunisia',16,MUTED),text(28,700,'AWS / Azure / OpenStack',16),
        text(28,746,'I engineer systems',20,WHITE,'700'),
        text(28,775,'that keep shipping.',20,GREEN,'700'),'</g></svg>']
    (assets/'hero-mobile.svg').write_text('\n'.join(parts),encoding='utf-8')
    if args.preview_dir:
        folder=Path(args.preview_dir); folder.mkdir(parents=True,exist_ok=True)
        font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
        for columns in (44,52):
            rows=portrait(args.photo,columns)
            canvas=Image.new('RGB',(columns*9+40,len(rows)*18+40),BG); draw=ImageDraw.Draw(canvas)
            for y,row in enumerate(rows): draw.text((20,20+y*18),row,fill=WHITE,font=font)
            canvas.save(folder/f'neofetch-{columns}.png')
    print(f'Generated compact {len(lines[0])} by {len(lines)} monochrome ASCII portrait.')

if __name__=='__main__': main()
