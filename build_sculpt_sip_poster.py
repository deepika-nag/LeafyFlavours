"""
Leafy Flavours — Sculpt & Sip, Diwali Edition
Mood board / poster for the Diwali clay workshop.

Run:  python3 build_sculpt_sip_poster.py
Out:  SculptAndSip_Diwali.jpg

EDIT THESE FIRST: DATE_LINE, TIME_LINE, SEATS_LINE below.
"""

from PIL import Image
from playwright.sync_api import sync_playwright
import base64, io, os, qrcode

HERE = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(HERE, 'images')

# ── EDIT ME ──────────────────────────────────────────────────────────────────
DATE_LINE  = 'Saturday 7 November'
TIME_LINE  = '2pm to 4pm'
SEATS_LINE = 'Eight seats only'
QR_URL     = 'https://www.instagram.com/leafyflavours'
# ─────────────────────────────────────────────────────────────────────────────

SETUP_PHOTO = os.path.expanduser('~/Downloads/IMG_2805.jpg')

def enc_png(path, size=320):
    im = Image.open(path).convert('RGBA')
    im.thumbnail((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return base64.b64encode(b.getvalue()).decode()

def enc_box(path, box, w, h, q=92):
    im = Image.open(path).convert('RGB').crop(box).resize((w, h), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q)
    return base64.b64encode(b.getvalue()).decode()

def enc_qr(url):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(url); qr.make(fit=True)
    im = qr.make_image(fill_color="#123028", back_color="white").convert('RGB')
    b = io.BytesIO(); im.save(b, 'PNG')
    return base64.b64encode(b.getvalue()).decode()

LOGO = enc_png(os.path.join(IMG, 'logo.png'))
QR   = enc_qr(QR_URL)

# hero: the low table, banana leaves, brass lamps, floor cushions
HERO = enc_box(SETUP_PHOTO, (0, 2980, 3213, 4560), 900, 443)
# detail: closer on the place setting
DET1 = enc_box(SETUP_PHOTO, (620, 3180, 2560, 4120), 420, 204)

STEPS = [
    ('Arrive &amp; settle',  'A welcome drink, low cushions, and a table dressed for the season.'),
    ('Shape your diyas',     'Two hours with the clay in your hands. No experience needed.'),
    ('Chai &amp; festive bites', 'Warm brewed chai and a spread of Karnataka festive bites.'),
]

MAKES = [
    'Two hand shaped clay diyas',
    'One keepsake piece to decorate',
    'All three wrapped and boxed to carry home',
]

KNOW = [
    'Air dry clay, pieces finish drying at home',
    'Wear something clay friendly',
    'Beginners welcome, ages 12 and up',
]

INCLUDED = [
    'All clay, tools and finishing colours',
    'Welcome drink on arrival',
    'Freshly brewed masala chai',
    'Karnataka festive bites, not a full dinner',
]

def li(items, cls='li'):
    return "\n".join(f'<div class="{cls}"><span class="dot"></span>{t}</div>' for t in items)

STEPS_HTML = "\n".join(f"""
      <div class="step">
        <div class="step-n">{i+1}</div>
        <div class="step-h">{h}</div>
        <div class="step-p">{p}</div>
      </div>""" for i, (h, p) in enumerate(STEPS))

SPRIG = """
<svg class="sprig" viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 6 C 60 30, 108 66, 142 112 C 166 146, 180 184, 186 224"
        fill="none" stroke="#B99B4A" stroke-width="1.4" opacity=".7"/>
  <g opacity=".78">
    <ellipse cx="44"  cy="24"  rx="18" ry="9"  fill="#8FB56A" transform="rotate(30 44 24)"/>
    <ellipse cx="76"  cy="50"  rx="20" ry="10" fill="#6E9E4E" transform="rotate(38 76 50)"/>
    <ellipse cx="106" cy="82"  rx="19" ry="9"  fill="#A3C47E" transform="rotate(48 106 82)"/>
    <ellipse cx="130" cy="120" rx="20" ry="10" fill="#6E9E4E" transform="rotate(60 130 120)"/>
    <ellipse cx="150" cy="164" rx="18" ry="9"  fill="#8FB56A" transform="rotate(70 150 164)"/>
  </g>
  <g fill="none" stroke="#C9A227" stroke-width="1.3" opacity=".62">
    <ellipse cx="34"  cy="52"  rx="15" ry="7" transform="rotate(74 34 52)"/>
    <ellipse cx="66"  cy="92"  rx="17" ry="8" transform="rotate(66 66 92)"/>
    <ellipse cx="104" cy="132" rx="16" ry="8" transform="rotate(50 104 132)"/>
    <ellipse cx="146" cy="94"  rx="15" ry="7" transform="rotate(22 146 94)"/>
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
  --marigold:#E08A1E; --terracotta:#B4552D;
  --ink:#1E2620; --muted:#6B6455;
}}
html {{ width:794px; height:1123px; overflow:hidden; }}
body {{
  width:794px; height:1123px; overflow:hidden; position:relative;
  background:var(--cream);
  font-family:'Cormorant Garamond',serif; color:var(--ink);
  display:flex; flex-direction:column;
}}
.sprig {{ position:absolute; width:132px; height:132px; z-index:9; opacity:.42; pointer-events:none; }}
.c-tl {{ top:-22px; left:-22px; }}
.c-tr {{ top:-22px; right:-22px; transform:scaleX(-1); }}

/* ═══ MASTHEAD ═══ */
.mast {{
  flex-shrink:0; text-align:center;
  padding:16px 40px 12px;
  border-bottom:1px solid var(--gold);
  position:relative; z-index:6;
}}
.logo {{
  width:56px; height:56px; border-radius:50%; margin:0 auto 6px;
  overflow:hidden; background:#fff; border:2px solid var(--gold);
}}
.logo img {{ width:100%; height:100%; object-fit:cover; }}
.mast-brand {{
  font-family:'Lato',sans-serif; font-size:11px; font-weight:900;
  letter-spacing:.34em; text-transform:uppercase; color:var(--teal-dk);
}}
.mast-sub {{
  font-size:12.5px; font-style:italic; color:var(--muted);
  letter-spacing:.05em; margin-top:2px;
}}

/* ═══ TITLE ═══ */
.title-wrap {{
  flex-shrink:0; text-align:center;
  padding:14px 40px 13px;
  background:var(--cream);
}}
.eyebrow {{
  display:inline-block;
  font-family:'Lato',sans-serif; font-size:9.5px; font-weight:900;
  letter-spacing:.3em; text-transform:uppercase;
  color:#fff; background:var(--terracotta);
  padding:4px 14px; border-radius:2px;
}}
.title {{
  font-size:62px; font-weight:600; letter-spacing:.02em;
  color:var(--teal-dk); line-height:1; margin-top:9px;
}}
.title em {{ font-style:italic; color:var(--marigold); }}
.subtitle {{
  font-size:19px; color:var(--muted); font-style:italic;
  margin-top:6px; letter-spacing:.02em;
}}

/* ═══ HERO ═══ */
.hero {{
  position:relative; flex-shrink:0;
  height:222px; overflow:hidden;
  border-top:3px solid var(--gold); border-bottom:3px solid var(--gold);
}}
.hero img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.hero-veil {{
  position:absolute; inset:0;
  background:linear-gradient(to top,
    rgba(18,48,40,.90) 0%, rgba(18,48,40,.45) 28%, rgba(18,48,40,0) 58%);
}}
.hero-cap {{
  position:absolute; left:0; right:0; bottom:0; padding:0 30px 14px;
  text-align:center;
}}
.hero-cap-l {{
  font-size:23px; color:#fff; font-style:italic;
  text-shadow:0 3px 12px rgba(0,0,0,.5); line-height:1.28;
}}
.hero-cap-s {{
  font-family:'Lato',sans-serif; font-size:9.5px; font-weight:700;
  letter-spacing:.22em; text-transform:uppercase;
  color:rgba(255,255,255,.82); margin-top:6px;
}}

/* ═══ STEPS ═══ */
.steps {{
  flex-shrink:0;
  display:grid; grid-template-columns:1fr 1fr 1fr;
  gap:16px; padding:12px 34px 10px;
  background:var(--cream2);
  border-bottom:1px solid var(--gold);
}}
.step {{ text-align:center; position:relative; }}
.step + .step::before {{
  content:''; position:absolute; left:-9px; top:4px; bottom:2px;
  width:1px; background:rgba(201,162,39,.45);
}}
.step-n {{
  width:22px; height:22px; margin:0 auto 4px;
  border-radius:50%; background:var(--marigold); color:#fff;
  font-family:'Lato',sans-serif; font-size:11px; font-weight:900;
  line-height:22px;
}}
.step-h {{
  font-family:'Lato',sans-serif; font-size:11px; font-weight:900;
  letter-spacing:.09em; text-transform:uppercase;
  color:var(--teal-dk); margin-bottom:2px;
}}
.step-p {{ font-size:14px; color:var(--muted); font-style:italic; line-height:1.34; }}

/* ═══ BODY: make + included ═══ */
.body {{
  flex:1; min-height:0;
  display:grid; grid-template-columns:1.02fr 0.98fr;
  gap:22px; padding:13px 34px 8px;
}}
.col {{ display:flex; flex-direction:column; min-height:0; }}
.col-h {{
  font-family:'Lato',sans-serif; font-size:11px; font-weight:900;
  letter-spacing:.16em; text-transform:uppercase; color:var(--teal);
  padding-bottom:4px; margin-bottom:7px;
  border-bottom:1px solid var(--gold);
}}
.li {{
  font-size:15.5px; color:var(--ink); line-height:1.5;
  display:flex; align-items:baseline; gap:7px; margin-bottom:4px;
}}
.dot {{
  width:5px; height:5px; border-radius:50%;
  background:var(--marigold); flex-shrink:0; margin-top:6px;
}}
.det-img {{
  margin-top:auto; border-radius:4px; overflow:hidden;
  border:1.5px solid var(--gold);
}}
.det-img img {{ width:100%; height:100px; object-fit:cover; display:block; }}
.note {{
  background:var(--gold-pale);
  border-left:3px solid var(--marigold);
  border-radius:3px; padding:7px 11px; margin-top:8px;
  font-size:13.5px; color:var(--ink); font-style:italic; line-height:1.36;
}}

/* ═══ DETAILS STRIP ═══ */
.details {{
  flex-shrink:0;
  display:grid; grid-template-columns:1fr 1fr 1fr;
  background:var(--teal); color:#fff;
  padding:11px 34px;
}}
.d {{ text-align:center; position:relative; }}
.d + .d::before {{
  content:''; position:absolute; left:0; top:3px; bottom:3px;
  width:1px; background:rgba(255,255,255,.24);
}}
.d-l {{
  font-family:'Lato',sans-serif; font-size:8.5px; font-weight:900;
  letter-spacing:.2em; text-transform:uppercase;
  color:var(--gold-lt); margin-bottom:2px;
}}
.d-v {{ font-size:17px; color:#fff; letter-spacing:.02em; }}

/* ═══ FOOTER ═══ */
.foot {{
  flex-shrink:0;
  background:var(--teal-dk);
  padding:20px 44px 34px;
  display:flex; align-items:center; gap:22px;
  border-top:3px solid var(--gold);
}}
.qr {{
  width:122px; flex-shrink:0;
  background:#fff; padding:8px 8px 5px; border-radius:5px;
  text-align:center; box-shadow:0 3px 14px rgba(0,0,0,.3);
}}
.qr img {{ width:100%; height:104px; display:block; }}
.qr-tag {{
  font-family:'Lato',sans-serif; font-size:7.5px; font-weight:900;
  letter-spacing:.15em; text-transform:uppercase;
  color:var(--teal-dk); margin-top:3px;
}}
.foot-mid {{ flex:1; }}
.foot-h {{
  font-size:27px; color:#fff; font-weight:600; letter-spacing:.02em; line-height:1.1;
}}
.foot-h em {{ color:var(--gold-lt); font-style:italic; }}
.foot-s {{
  font-family:'Lato',sans-serif; font-size:9.5px; font-weight:700;
  letter-spacing:.18em; text-transform:uppercase;
  color:rgba(235,209,119,.82); margin-top:6px;
}}
.foot-r {{ flex-shrink:0; text-align:right; }}
.handle {{ font-size:24px; color:var(--gold-lt); font-weight:600; letter-spacing:.02em; }}
.loc {{
  font-family:'Lato',sans-serif; font-size:9.5px; font-weight:700;
  letter-spacing:.16em; text-transform:uppercase;
  color:rgba(255,255,255,.6); margin-top:4px;
}}
</style>
</head>
<body>

{SPRIG.replace('class="sprig"','class="sprig c-tl"')}
{SPRIG.replace('class="sprig"','class="sprig c-tr"')}

<!-- MASTHEAD -->
<div class="mast">
  <div class="logo"><img src="data:image/png;base64,{LOGO}" alt="Leafy Flavours"></div>
  <div class="mast-brand">Leafy Flavours</div>
  <div class="mast-sub">Taste of Mysuru &nbsp;&middot;&nbsp; Kellyville, Sydney</div>
</div>

<!-- TITLE -->
<div class="title-wrap">
  <div class="eyebrow">Diwali Edition</div>
  <div class="title">Sculpt &amp; <em>Sip</em></div>
  <div class="subtitle">A mindful clay afternoon, with chai and festive bites</div>
</div>

<!-- HERO -->
<div class="hero">
  <img src="data:image/jpeg;base64,{HERO}" alt="Sculpt and Sip table setting">
  <div class="hero-veil"></div>
  <div class="hero-cap">
    <div class="hero-cap-l">Light your own diyas this Diwali.<br>The ones you shaped yourself.</div>
    <div class="hero-cap-s">Two hours &nbsp;&bull;&nbsp; Clay, chai and good company</div>
  </div>
</div>

<!-- STEPS -->
<div class="steps">{STEPS_HTML}
</div>

<!-- BODY -->
<div class="body">
  <div class="col">
    <div class="col-h">What you will make</div>
    {li(MAKES)}
    <div class="note" style="margin-top:auto;">
      No experience needed. If you have never touched clay, this session was built for you.
    </div>
  </div>
  <div class="col">
    <div class="col-h">What is included</div>
    {li(INCLUDED)}
    <div class="col-h" style="margin-top:13px;">Good to know</div>
    {li(KNOW)}
  </div>
</div>

<!-- DETAILS -->
<div class="details">
  <div class="d">
    <div class="d-l">When</div>
    <div class="d-v">{DATE_LINE}</div>
  </div>
  <div class="d">
    <div class="d-l">Time</div>
    <div class="d-v">{TIME_LINE}</div>
  </div>
  <div class="d">
    <div class="d-l">Seats</div>
    <div class="d-v">{SEATS_LINE}</div>
  </div>
</div>

<!-- FOOTER -->
<div class="foot">
  <div class="qr">
    <img src="data:image/png;base64,{QR}" alt="QR">
    <div class="qr-tag">Scan Me</div>
  </div>
  <div class="foot-mid">
    <div class="foot-h">Save your <em>seat</em></div>
    <div class="foot-s">Scan or DM to book</div>
  </div>
  <div class="foot-r">
    <div class="handle">@leafyflavours</div>
    <div class="loc">Kellyville, Sydney</div>
  </div>
</div>

</body>
</html>"""

def render(html, dest):
    tmp = '/private/tmp/sculpt_sip.html'
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
    render(HTML, os.path.join(HERE, 'SculptAndSip_Diwali.jpg'))
