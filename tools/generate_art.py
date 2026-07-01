"""Rebuild the ASCII artwork locally; the source photograph is never copied.

Usage: python tools/generate_art.py --photo /path/to/portrait.png
Requires Pillow 12.3.0. Run from any directory.
"""
import argparse
from html import escape
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG, GREEN, WHITE, MUTED = '#070A08', '#00FF88', '#F5FFF8', '#859189'

def portrait(photo, columns=88):
    image = Image.open(photo).convert('RGB')
    if image.size != (1254, 1254):
        image = ImageOps.fit(image, (1254, 1254))
    # Manual silhouette follows the supplied photo; excludes the studio wall.
    mask = Image.new('L', image.size)
    ImageDraw.Draw(mask).polygon([(440,180),(495,119),(650,106),(741,135),
        (790,223),(810,385),(831,423),(827,487),(802,520),(775,535),
        (770,650),(801,717),(912,772),(1070,825),(1190,880),(1254,1090),
        (1254,1254),(0,1254),(97,907),(234,835),(355,768),(465,695),
        (477,579),(450,538),(419,522),(400,455),(403,421),(424,406),
        (409,324),(420,241)], fill=255)
    box = (290, 80, 960, 970)
    rows = round((box[3]-box[1])/(box[2]-box[0])*columns*0.50)
    gray = ImageEnhance.Contrast(ImageOps.grayscale(image.crop(box))).enhance(1.05)
    gray = gray.resize((columns, rows), Image.Resampling.LANCZOS)
    silhouette = mask.crop(box).resize((columns, rows), Image.Resampling.LANCZOS)
    # Gentle punctuation and natural light values avoid the negative-film look.
    ramp = ' .,:;+=ox%'
    lines, tones = [], []
    for y in range(rows):
        chars, colors = [], []
        for x in range(columns):
            darkness = 1-gray.getpixel((x,y))/255
            alpha = silhouette.getpixel((x,y))/255
            char = ramp[min(len(ramp)-1, int((0.10+(1-darkness)*.75)*(len(ramp)-1)))] if alpha>.55 else ' '
            chars.append(char)
            light = (1-darkness)**.8
            colors.append('#%02x%02x%02x' % (int(44+light*173),int(91+light*149),int(67+light*155)))
        lines.append(''.join(chars)); tones.append(colors)
    return lines, tones

def svg_text(x,y,text,size=18,color=WHITE,weight='400'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(text)}</text>'

def ascii_svg(lines,tones,x,y,cell=4,line=8):
    parts=[]
    for row, chars in enumerate(lines):
        # Explicit positions keep character cells stable across fallback fonts.
        for col,char in enumerate(chars):
            if char!=' ':
                parts.append(svg_text(x+col*cell,y+row*line,char,line,tones[row][col]))
    return ''.join(parts)

def shell(width,height,title,description):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
        f'<rect width="{width}" height="{height}" rx="18" fill="{BG}"/>',
        '<g font-family="Consolas, Liberation Mono, monospace">']

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--photo',required=True)
    parser.add_argument('--preview-dir'); args=parser.parse_args()
    assets=ROOT/'assets'; assets.mkdir(exist_ok=True)
    lines,tones=portrait(args.photo)
    (assets/'portrait.txt').write_text('\n'.join(line.rstrip() for line in lines)+'\n',encoding='ascii')
    parts=shell(1200,680,'Assil Belhouene | Cloud, DevOps & Full-Stack Engineer',
        'Terminal-inspired engineering profile with a green ASCII portrait of Assil wearing glasses and a blazer.')
    for x in range(24,1200,40): parts.append(f'<path d="M{x} 64V680" stroke="#122219" stroke-width="1"/>')
    for y in range(64,680,40): parts.append(f'<path d="M0 {y}H1200" stroke="#122219" stroke-width="1"/>')
    parts+=['<path d="M0 64H1200" stroke="#26382D"/>','<circle cx="32" cy="32" r="5" fill="#00FF88"/>',
        svg_text(48,38,'assil.cloud',17,WHITE),svg_text(910,38,'~/profile  /  whoami',14,MUTED),
        svg_text(46,117,'ENGINEERING PROFILE  /  01',14,GREEN),
        svg_text(46,178,'$ whoami',20,MUTED),svg_text(46,258,"Hi, I'm Assil.",48,WHITE,'700'),
        svg_text(46,321,'I engineer systems',35,WHITE,'700'),
        svg_text(46,371,'that keep shipping',35,GREEN,'700'),
        '<rect x="448" y="343" width="18" height="33" fill="#00FF88"/>',
        svg_text(46,427,'Cloud / DevOps / Full-Stack',20,MUTED),
        '<path d="M46 463H650" stroke="#26382D"/>',
        svg_text(46,506,'DESIGN  →  AUTOMATE  →  OPERATE',17,GREEN),
        svg_text(46,544,'From visual workflows to dependable platforms.',17,WHITE),
        svg_text(46,620,'Kelibia, Tunisia  ·  AWS / Azure / OpenStack',15,MUTED),
        '<rect x="725" y="104" width="432" height="562" rx="12" fill="#0B120E" stroke="#26382D"/>',
        svg_text(747,137,'$ render portrait --ascii',13,MUTED),
        ascii_svg(lines,tones,765,164),svg_text(747,650,'ASSIL BELHOUENE  /  ASCII EDITION',12,GREEN),
        '</g></svg>']
    (assets/'hero.svg').write_text('\n'.join(parts),encoding='utf-8')
    parts=shell(432,650,'Assil Belhouene — ASCII portrait','A portrait built entirely from ASCII characters, converted from the supplied photo.')
    parts += [svg_text(22,38,'$ whoami',16,GREEN),svg_text(22,72,'Assil Belhouene',24,WHITE,'700'),
        svg_text(22,105,'Cloud / DevOps / Full-Stack',14,MUTED),ascii_svg(lines,tones,40,148),
        svg_text(22,615,'I engineer systems that keep shipping.',13,GREEN),'</g></svg>']
    (assets/'hero-mobile.svg').write_text('\n'.join(parts),encoding='utf-8')
    if args.preview_dir:
        folder=Path(args.preview_dir); folder.mkdir(parents=True,exist_ok=True)
        font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
        for cols in (68,88):
            ls,ts=portrait(args.photo,cols)
            canvas=Image.new('RGB',(cols*8+40,len(ls)*14+50),BG)
            draw=ImageDraw.Draw(canvas)
            for row,chars in enumerate(ls):
                for col,c in enumerate(chars): draw.text((20+col*8,20+row*14),c,font=font,fill=ts[row][col])
            canvas.save(folder/f'portrait-{cols}.png')
    print(f'Generated {len(lines[0])} × {len(lines)} ASCII portrait and two responsive SVGs.')

if __name__=='__main__': main()
