"""
Leafy Flavours — Pop-up Signboard
Designed to read from 2-3 metres. Detail lives behind the QR.
Run:  python3 build_brand_flyer.py
Output: BrandFlyer_LeafyFlavours.jpg
"""

from PIL import Image
from playwright.sync_api import sync_playwright
import base64, io, os, qrcode

HERE = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(HERE, 'images')

QR_URL = 'https://deepika-nag.github.io/LeafyFlavours/'

# ── encoders ─────────────────────────────────────────────────────────────────

def enc_png(path, size=340):
    im = Image.open(path).convert('RGBA')
    im.thumbnail((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return base64.b64encode(b.getvalue()).decode()

def enc_crop(name, w, h, focus=0.4, q=90):
    """Center-crop to w:h aspect. focus = vertical bias (0 top, 1 bottom)."""
    im = Image.open(os.path.join(IMG, name)).convert('RGB')
    tw, th = im.size
    target, cur = w / h, tw / th
    if cur > target:
        nw = int(th * target)
        im = im.crop(((tw - nw) // 2, 0, (tw + nw) // 2, th))
    else:
        nh = int(tw / target)
        top = int((th - nh) * focus)
        im = im.crop((0, top, tw, top + nh))
    im = im.resize((w, h), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q)
    return base64.b64encode(b.getvalue()).decode()

def enc_qr(url):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(url); qr.make(fit=True)
    im = qr.make_image(fill_color="#123028", back_color="white").convert('RGB')
    b = io.BytesIO(); im.save(b, 'PNG')
    return base64.b64encode(b.getvalue()).decode()

LOGO  = enc_png(os.path.join(IMG, 'logo.png'))
HERO  = enc_crop('main-banner.jpg', 900, 470, focus=0.45)
QR    = enc_qr(QR_URL)

# three buckets, not six
TILES = [
    ('Grazing Tables',  'Karnataka spreads &amp; street food, styled on your table.',   'namma5.jpg'),
    ('Sit-Down Feasts', 'Elle Oota &amp; supper clubs, served course by course.',        'sitdown-hero.jpg'),
    ('The Opening Act', 'You bring the mains. We bring the starters &amp; the styling.', 'openingact.jpg'),
]

# the answer to "why are you three times the stall next door"
WHY = [
    ('We come to you',      'We arrive and style your table to your theme, down to the details. Then we leave you to your evening.'),
    ('Cooked for your date','Made fresh on the day. Never bulk. Never reheated.'),
    ('One table at a time', 'Only 1&ndash;2 events a month, so yours gets everything.'),
]

def enc_box(name, box, w, h, q=92):
    """Crop an explicit (l,t,r,b) box then resize."""
    im = Image.open(os.path.join(IMG, name)).convert('RGB').crop(box)
    im = im.resize((w, h), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q)
    return base64.b64encode(b.getvalue()).decode()

# tight frame on Deepika plating at a supper club
PORTRAIT = enc_box('deepika.jpg', (430, 500, 2400, 2760), 330, 380)

WHY_HTML = "\n".join(f"""
      <div class="why-col">
        <div class="why-n">{i+1}</div>
        <div class="why-h">{h}</div>
        <div class="why-p">{p}</div>
      </div>""" for i, (h, p) in enumerate(WHY))

TILE_HTML = "\n".join(f"""
      <div class="tile">
        <div class="tile-img"><img src="data:image/jpeg;base64,{enc_crop(img, 320, 260, 0.4)}" alt=""></div>
        <div class="tile-name">{name}</div>
        <div class="tile-desc">{desc}</div>
      </div>""" for name, desc, img in TILES)

SPRIG = """
<svg class="sprig" viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 6 C 60 30, 108 66, 142 112 C 166 146, 180 184, 186 224"
        fill="none" stroke="#B99B4A" stroke-width="1.4" opacity=".7"/>
  <g opacity=".8">
    <ellipse cx="44"  cy="24"  rx="18" ry="9"  fill="#8FB56A" transform="rotate(30 44 24)"/>
    <ellipse cx="76"  cy="50"  rx="20" ry="10" fill="#6E9E4E" transform="rotate(38 76 50)"/>
    <ellipse cx="106" cy="82"  rx="19" ry="9"  fill="#A3C47E" transform="rotate(48 106 82)"/>
    <ellipse cx="130" cy="120" rx="20" ry="10" fill="#6E9E4E" transform="rotate(60 130 120)"/>
    <ellipse cx="150" cy="164" rx="18" ry="9"  fill="#8FB56A" transform="rotate(70 150 164)"/>
  </g>
  <g fill="none" stroke="#C9A227" stroke-width="1.3" opacity=".65">
    <ellipse cx="34"  cy="52"  rx="15" ry="7" transform="rotate(74 34 52)"/>
    <ellipse cx="66"  cy="92"  rx="17" ry="8" transform="rotate(66 66 92)"/>
    <ellipse cx="104" cy="132" rx="16" ry="8" transform="rotate(50 104 132)"/>
    <ellipse cx="146" cy="94"  rx="15" ry="7" transform="rotate(22 146 94)"/>
    <ellipse cx="142" cy="204" rx="14" ry="7" transform="rotate(80 142 204)"/>
  </g>
</svg>
"""

HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Lato:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
:root {{
  --cream:#FFFCF3; --cream2:#FBF4E2;
  --gold:#C9A227; --gold-lt:#EBD177; --gold-pale:#F4E9C4;
  --teal:#1B6B6B; --teal-dk:#123028;
  --leaf:#6E9E4E;
  --ink:#1E2620; --muted:#6B6455;
}}
html {{ width:794px; height:1123px; overflow:hidden; }}
body {{
  width:794px; height:1123px; overflow:hidden; position:relative;
  background:var(--cream);
  font-family:'Cormorant Garamond',serif; color:var(--ink);
  display:flex; flex-direction:column;
}}
.sprig {{ position:absolute; width:158px; height:158px; z-index:9; opacity:.5; pointer-events:none; }}
.c-tl {{ top:-26px; left:-26px; }}
.c-tr {{ top:-26px; right:-26px; transform:scaleX(-1); }}

/* ═══ MASTHEAD ═══ */
.mast {{
  background:var(--cream);
  padding:20px 40px 14px;
  text-align:center; flex-shrink:0;
  position:relative; z-index:6;
  border-bottom:2px solid var(--gold);
}}
.logo {{
  width:94px; height:94px; border-radius:50%; margin:0 auto 8px;
  overflow:hidden; background:#fff; border:2px solid var(--gold);
  box-shadow:0 3px 12px rgba(0,0,0,.10);
}}
.logo img {{ width:100%; height:100%; object-fit:cover; }}
.brand {{
  font-size:47px; font-weight:600; letter-spacing:.085em;
  color:var(--teal-dk); line-height:.98;
}}
.mysuru {{
  display:inline-block; margin-top:9px;
  font-family:'Lato',sans-serif; font-size:13px; font-weight:900;
  letter-spacing:.42em; text-transform:uppercase;
  color:var(--teal);
  border-top:1px solid var(--gold); border-bottom:1px solid var(--gold);
  padding:5px 20px 5px 24px;
}}
.by {{
  font-size:16px; color:var(--muted); letter-spacing:.06em; margin-top:7px;
  font-style:italic;
}}

/* ═══ HERO ═══ */
.hero {{
  position:relative; flex-shrink:0;
  height:196px; overflow:hidden;
  border-bottom:4px solid var(--gold);
}}
.hero img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.hero-veil {{
  position:absolute; inset:0;
  background:linear-gradient(to top,
    rgba(18,48,40,.93) 0%, rgba(18,48,40,.62) 34%,
    rgba(18,48,40,.12) 66%, rgba(18,48,40,0) 100%);
}}
.hero-txt {{
  position:absolute; left:0; right:0; bottom:0; padding:0 36px 18px;
  text-align:center;
}}
.hero-line {{
  font-size:33px; font-weight:600; color:#fff;
  letter-spacing:.02em; line-height:1.16;
  text-shadow:0 3px 14px rgba(0,0,0,.55);
}}
.hero-line em {{ color:var(--gold-lt); font-style:italic; }}
.hero-sub {{
  font-family:'Lato',sans-serif; font-size:11px; font-weight:700;
  letter-spacing:.24em; text-transform:uppercase;
  color:rgba(255,255,255,.82); margin-top:7px;
}}

/* ═══ TILES ═══ */
.tiles {{
  flex:1; display:grid; grid-template-columns:1fr 1fr 1fr;
  gap:14px; padding:16px 34px 12px;
  background:var(--cream); min-height:0;
}}
.tile {{ display:flex; flex-direction:column; min-height:0; }}
.tile-img {{
  flex:1; min-height:0; overflow:hidden;
  border-radius:4px; border:1.5px solid var(--gold);
  box-shadow:0 3px 10px rgba(0,0,0,.10);
}}
.tile-img img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.tile-name {{
  font-family:'Lato',sans-serif; font-size:14px; font-weight:900;
  letter-spacing:.11em; text-transform:uppercase;
  color:var(--teal-dk); margin-top:9px; text-align:center;
}}
.tile-desc {{
  font-size:14.5px; color:var(--muted); font-style:italic;
  text-align:center; margin-top:2px; line-height:1.32;
}}

/* ═══ WHY WE'RE NOT A CATERER ═══ */
.why {{
  flex-shrink:0;
  background:var(--cream2);
  border-top:1px solid var(--gold); border-bottom:1px solid var(--gold);
  padding:10px 30px 11px;
}}
.why-title {{
  text-align:center;
  font-family:'Lato',sans-serif; font-size:11px; font-weight:900;
  letter-spacing:.26em; text-transform:uppercase;
  color:var(--teal); margin-bottom:9px;
}}
.why-cols {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px; }}
.why-col {{ text-align:center; position:relative; }}
.why-col + .why-col::before {{
  content:''; position:absolute; left:-10px; top:6px; bottom:2px;
  width:1px; background:rgba(201,162,39,.45);
}}
.why-n {{
  font-size:15px; font-weight:700; color:var(--gold);
  line-height:1; margin-bottom:2px;
}}
.why-h {{
  font-family:'Lato',sans-serif; font-size:11.5px; font-weight:900;
  letter-spacing:.1em; text-transform:uppercase;
  color:var(--teal-dk); margin-bottom:2px;
}}
.why-p {{
  font-size:14px; color:var(--muted); font-style:italic; line-height:1.32;
}}

/* ═══ SIGNATURE + PROOF ═══ */
.sig {{
  flex-shrink:0; text-align:center;
  padding:14px 56px 14px;
  background:var(--cream);
  border-bottom:1px solid var(--gold);
}}
.sig-stars {{
  color:var(--gold); font-size:12px; letter-spacing:.34em; margin-bottom:6px;
}}
.sig-quote {{
  font-size:20px; color:var(--ink); font-style:italic;
  line-height:1.34; letter-spacing:.01em;
}}
.sig-quote b {{ font-style:normal; font-weight:700; color:var(--teal-dk); }}
.sig-cite {{
  font-family:'Lato',sans-serif; font-size:9.5px; font-weight:700;
  letter-spacing:.18em; text-transform:uppercase;
  color:var(--muted); margin-top:6px;
}}
.sig-rule {{
  height:1px; width:190px; margin:9px auto 8px;
  background:linear-gradient(to right,transparent,var(--gold),transparent);
}}
.sig-name {{
  font-family:'Lato',sans-serif; font-size:11.5px; font-weight:900;
  letter-spacing:.14em; text-transform:uppercase; color:var(--teal-dk);
}}
.sig-line {{
  font-size:22px; color:var(--teal-dk); letter-spacing:.02em;
}}
.sig-line b {{ font-weight:700; }}
.sig-note {{
  font-family:'Lato',sans-serif; font-size:10.5px; font-weight:700;
  letter-spacing:.2em; text-transform:uppercase;
  color:var(--teal); margin-top:5px;
}}

/* ═══ FOOTER ═══ */
.foot {{
  flex-shrink:0;
  background:var(--teal-dk);
  padding:26px 48px 42px;
  display:flex; align-items:center; gap:26px;
}}
.qr {{
  width:142px; flex-shrink:0;
  background:#fff; padding:9px 9px 6px; border-radius:5px;
  box-shadow:0 3px 14px rgba(0,0,0,.28);
  text-align:center;
}}
.qr img {{ width:100%; height:122px; display:block; }}
.qr-tag {{
  font-family:'Lato',sans-serif; font-size:8px; font-weight:900;
  letter-spacing:.16em; text-transform:uppercase;
  color:var(--teal-dk); margin-top:4px;
}}
.foot-mid {{ flex:1; }}
.foot-h {{
  font-size:29px; font-weight:600; color:#fff;
  letter-spacing:.03em; line-height:1.08;
}}
.foot-h em {{ color:var(--gold-lt); font-style:italic; }}
.foot-sub {{
  font-family:'Lato',sans-serif; font-size:10.5px; font-weight:700;
  letter-spacing:.2em; text-transform:uppercase;
  color:rgba(235,209,119,.8); margin-top:6px;
}}
.foot-right {{ flex-shrink:0; text-align:right; }}
.handle {{
  font-size:27px; color:var(--gold-lt); font-weight:600; letter-spacing:.03em;
}}
.loc {{
  font-family:'Lato',sans-serif; font-size:10.5px; font-weight:700;
  letter-spacing:.18em; text-transform:uppercase;
  color:rgba(255,255,255,.62); margin-top:5px;
}}
</style>
</head>
<body>

{SPRIG.replace('class="sprig"','class="sprig c-tl"')}
{SPRIG.replace('class="sprig"','class="sprig c-tr"')}

<!-- MASTHEAD -->
<div class="mast">
  <div class="logo"><img src="data:image/png;base64,{LOGO}" alt="Leafy Flavours"></div>
  <div class="brand">LEAFY FLAVOURS</div>
  <div class="mysuru">Taste of Mysuru</div>
  <div class="by">by KitchenChimes &nbsp;&middot;&nbsp; Kellyville, Sydney</div>
</div>

<!-- HERO -->
<div class="hero">
  <img src="data:image/jpeg;base64,{HERO}" alt="">
  <div class="hero-veil"></div>
  <div class="hero-txt">
    <div class="hero-line">Most caterers hand you a tray.<br><em>We hand you an experience.</em></div>
    <div class="hero-sub">Karnataka cuisine &nbsp;&bull;&nbsp; styled &amp; served at your venue</div>
  </div>
</div>

<!-- TILES -->
<div class="tiles">{TILE_HTML}
</div>

<!-- WHY -->
<div class="why">
  <div class="why-title">Why we&rsquo;re not a caterer</div>
  <div class="why-cols">{WHY_HTML}
  </div>
</div>

<!-- PROOF + SIGNATURE -->
<div class="sig">
  <div class="sig-stars">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
  <div class="sig-quote">&ldquo;You didn&rsquo;t just cater an event. You poured love, creativity and thought into <b>every single detail</b>.&rdquo;</div>
  <div class="sig-cite">From a recent client review</div>
  <div class="sig-rule"></div>
  <div class="sig-name">Cooked, styled &amp; served by Deepika Nagaraja</div>
</div>

<!-- FOOTER -->
<div class="foot">
  <div class="qr">
    <img src="data:image/png;base64,{QR}" alt="QR">
    <div class="qr-tag">Scan Me</div>
  </div>
  <div class="foot-mid">
    <div class="foot-h">Curate your <em>next celebration</em></div>
    <div class="foot-sub">Scan for menus &amp; bookings</div>
  </div>
  <div class="foot-right">
    <div class="handle">@leafyflavours</div>
    <div class="loc">0470 382 859</div>
  </div>
</div>

</body>
</html>"""

def render(html, dest):
    tmp = '/private/tmp/brand_flyer.html'
    with open(tmp, 'w') as f:
        f.write(html)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=1.56)
        pg.goto(f'file://{tmp}')
        pg.wait_for_load_state('networkidle')
        pg.wait_for_timeout(2500)
        png = pg.screenshot(clip={'x': 0, 'y': 0, 'width': 794, 'height': 1123})
        b.close()
    im = Image.open(io.BytesIO(png)).convert('RGB')
    im.save(dest, 'JPEG', quality=95)
    print(f'Saved {im.size} -> {dest}')

if __name__ == '__main__':
    render(HTML, os.path.join(HERE, 'BrandFlyer_LeafyFlavours.jpg'))
