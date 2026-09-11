"""
Leafy Flavours — Festive Brochure Builder
Run:  python3 build_festive_brochure.py
Outputs:
  FestiveBrochure_LeafyFlavours.jpg  (with prices)
  FestiveBrochure_Enquire.jpg        (enquire version)
"""

from PIL import Image
from playwright.sync_api import sync_playwright
import base64, io, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Image helpers ─────────────────────────────────────────────────────────────

def enc_crop(path, y0, y1, max_w=700, max_h=700, q=88):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    img = img.crop((0, int(h * y0), w, int(h * y1)))
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=q)
    return base64.b64encode(buf.getvalue()).decode()

def enc_png(path, size=220):
    img = Image.open(path).convert('RGBA')
    img.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

# ── Encode assets ─────────────────────────────────────────────────────────────

LOGO = enc_png(os.path.join(HERE, 'images/logo.png'))
TAMB = enc_crop(os.path.expanduser('~/Downloads/IMG_2294.jpg'), 0.28, 0.82)
BAAG = enc_crop(os.path.expanduser('~/Downloads/IMG_8883.jpg'), 0.12, 0.72)

# ── HTML generator ────────────────────────────────────────────────────────────

def make_html(show_prices: bool) -> str:
    price_tamb  = '$18'    if show_prices else 'Enquire'
    price_baag  = '$50'    if show_prices else 'Enquire'
    price_note  = 'AUD per box' if show_prices else 'DM @leafyflavours'
    addon_tamb  = ('Artisanal Mithai <span class="ap">+$3</span>'
                   '&nbsp;&nbsp; Traditional Khara <span class="ap">+$3</span>'
                   if show_prices else
                   'Artisanal Mithai &nbsp;&nbsp; Traditional Khara')
    addon_baag  = ('Artisanal Mithai <span class="ap">+$3</span>'
                   '&nbsp;&nbsp; Traditional Khara <span class="ap">+$3</span>'
                   if show_prices else
                   'Artisanal Mithai &nbsp;&nbsp; Traditional Khara')

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
:root{{
  --green:#1E3A2B;--green-dk:#0F2018;--green-mid:#1a3324;
  --gold:#C9A84C;--gold-lt:#EDD98A;--gold-pale:#FAF4DC;
  --cream:#FAF7F0;--crimson:#9B1C1C;
  --text:#1A1208;--muted:#7A5C35;--border:rgba(180,145,60,.28);
}}
html{{width:794px;height:1123px;overflow:hidden;background:var(--cream);}}
body{{
  font-family:'Lato',sans-serif;color:var(--text);
  width:794px;height:1123px;
  display:flex;flex-direction:column;
  overflow:hidden;
}}

/* ── HEADER ── */
.hdr{{
  background:var(--green-dk);
  padding:13px 22px 11px;
  display:flex;align-items:center;gap:16px;
  border-bottom:2px solid var(--gold);
  flex-shrink:0;
}}
.logo-ring{{
  width:70px;height:70px;border-radius:50%;
  border:2px solid var(--gold);overflow:hidden;flex-shrink:0;background:#fff;
}}
.logo-ring img{{width:100%;height:100%;object-fit:cover;}}
.hdr-mid{{flex:1;}}
.brand-name{{
  font-family:'Playfair Display',serif;
  font-size:28px;color:#fff;letter-spacing:.12em;font-weight:700;
  line-height:1;
}}
.brand-tag{{
  font-size:8px;color:rgba(237,217,138,.7);letter-spacing:.18em;
  text-transform:uppercase;margin-top:4px;
}}
.hdr-right{{text-align:right;}}
.badge{{
  display:inline-block;
  background:var(--crimson);color:#fff;
  font-size:7.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  padding:4px 10px;border-radius:2px;
}}
.badge::before{{content:'✦ ';}}
.badge::after{{content:' ✦';}}
.hdr-occ{{
  font-family:'Cormorant Garamond',serif;font-style:italic;
  font-size:11px;color:rgba(237,217,138,.75);
  margin-top:6px;line-height:1.9;
}}

/* ── WELCOME ── */
.welcome{{
  background:var(--cream);
  padding:10px 24px 9px;text-align:center;
  border-bottom:1px solid var(--border);
  flex-shrink:0;
}}
.welcome h2{{
  font-family:'Playfair Display',serif;
  font-size:18px;color:var(--green-dk);letter-spacing:.02em;font-weight:600;
}}
.welcome p{{
  font-size:10.5px;color:var(--muted);
  font-style:italic;font-family:'Cormorant Garamond',serif;
  margin-top:3px;letter-spacing:.03em;
}}

/* ── DIVIDER ── */
.orn{{
  display:flex;align-items:center;gap:8px;padding:5px 22px;
  background:var(--cream);flex-shrink:0;
}}
.orn-line{{flex:1;height:1px;background:linear-gradient(to right,transparent,var(--gold),transparent);}}
.orn-sym{{color:var(--gold);font-size:11px;letter-spacing:5px;}}

/* ── CAT BAND ── */
.cat-band{{
  background:var(--green);padding:7px 22px;
  display:flex;align-items:center;justify-content:space-between;
  border-top:1px solid rgba(201,168,76,.3);
  flex-shrink:0;
}}
.cat-lhs .cat-num{{
  font-size:7.5px;color:rgba(237,217,138,.55);letter-spacing:.2em;
  text-transform:uppercase;font-weight:700;margin-bottom:1px;
}}
.cat-lhs .cat-title{{
  font-family:'Playfair Display',serif;
  font-size:16px;color:var(--gold-lt);letter-spacing:.03em;font-weight:600;
}}
.cat-occ{{
  font-family:'Cormorant Garamond',serif;font-style:italic;
  font-size:10px;color:rgba(237,217,138,.65);text-align:right;line-height:1.9;
}}

/* ── CAT ROW ── */
.cat-row{{display:flex;flex:1;min-height:0;}}
.photo-panel{{width:240px;flex-shrink:0;overflow:hidden;}}
.photo-panel img{{width:100%;height:100%;object-fit:cover;object-position:center center;}}
.content-panel{{
  flex:1;padding:11px 18px 9px;
  display:flex;flex-direction:column;
  border-left:1px solid var(--border);
  background:#fff;
  overflow:hidden;
}}

/* ── PRODUCT TOP ── */
.prod-eyebrow{{
  font-size:7px;font-weight:700;color:var(--gold);
  letter-spacing:.14em;text-transform:uppercase;margin-bottom:3px;
}}
.prod-eyebrow::before{{content:'✦ ';}}
.prod-row{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:2px;}}
.prod-name{{
  font-family:'Playfair Display',serif;
  font-size:14px;color:var(--green-dk);font-weight:600;
}}
.prod-price-wrap{{text-align:right;line-height:1;}}
.prod-price{{
  font-family:'Playfair Display',serif;
  font-size:26px;color:var(--crimson);font-weight:700;
}}
.prod-price-note{{
  display:block;font-size:8px;color:var(--muted);margin-top:2px;
}}
.prod-sub{{
  font-size:9px;color:var(--muted);font-style:italic;
  font-family:'Cormorant Garamond',serif;letter-spacing:.02em;margin-bottom:7px;
}}
.divider-thin{{height:1px;background:var(--border);margin-bottom:8px;}}

/* ── ITEMS ── */
.items-cols{{display:grid;grid-template-columns:1fr 1fr;gap:0 16px;flex:1;overflow:hidden;}}
.grp{{margin-bottom:6px;}}
.grp-label{{
  font-size:7px;font-weight:900;color:var(--green);
  text-transform:uppercase;letter-spacing:.12em;
  border-bottom:1px solid var(--border);
  padding-bottom:2px;margin-bottom:4px;
}}
.itm{{
  font-size:9.5px;color:var(--text);line-height:1.6;
  display:flex;align-items:baseline;gap:5px;
}}
.dot{{
  width:4px;height:4px;border-radius:50%;
  background:var(--gold);flex-shrink:0;margin-top:4px;
}}

/* ── ADD-ONS ── */
.addons-wrap{{margin-top:auto;padding-top:6px;}}
.addons-box{{
  border:1px solid var(--border);border-radius:3px;
  background:var(--gold-pale);
  padding:6px 12px;
  display:flex;align-items:center;gap:10px;
}}
.addon-label{{
  font-size:7px;font-weight:700;color:var(--green);
  text-transform:uppercase;letter-spacing:.1em;flex-shrink:0;
  border-right:1px solid var(--border);padding-right:10px;
}}
.addon-items{{font-size:9px;color:var(--text);}}
.ap{{color:var(--green);font-weight:700;font-size:8.5px;}}
.box-note{{
  font-size:7px;color:var(--muted);font-style:italic;
  text-align:right;margin-top:3px;letter-spacing:.03em;
}}

/* ── FOOTER ── */
.order{{
  background:var(--green-dk);
  padding:10px 24px 11px;
  border-top:2px solid var(--gold);
  flex-shrink:0;
}}
.order-head{{
  font-family:'Playfair Display',serif;
  font-size:15px;color:#fff;text-align:center;letter-spacing:.04em;font-weight:600;
}}
.order-sub{{
  font-size:8.5px;color:rgba(237,217,138,.65);text-align:center;
  font-style:italic;font-family:'Cormorant Garamond',serif;
  margin-top:2px;margin-bottom:8px;letter-spacing:.04em;
}}
.order-cols{{display:flex;justify-content:center;gap:0;}}
.order-col{{
  flex:1;text-align:center;
  border-right:1px solid rgba(201,168,76,.25);padding:0 16px;
}}
.order-col:last-child{{border-right:none;}}
.o-lbl{{
  font-size:6.5px;font-weight:700;color:var(--gold);
  text-transform:uppercase;letter-spacing:.14em;display:block;margin-bottom:3px;
}}
.o-val{{font-size:8.5px;color:rgba(237,217,138,.85);line-height:1.6;}}
.order-cta{{
  text-align:center;margin-top:7px;
  font-family:'Playfair Display',serif;
  font-size:11px;color:var(--gold-lt);letter-spacing:.06em;
}}
.order-cta span{{color:var(--gold);font-weight:700;}}
</style>
</head>
<body>

<!-- HEADER -->
<div class="hdr">
  <div class="logo-ring">
    <img src="data:image/png;base64,{LOGO}" alt="Leafy Flavours">
  </div>
  <div class="hdr-mid">
    <div class="brand-name">LEAFY FLAVOURS</div>
    <div class="brand-tag">Bespoke Festive &amp; Ceremonial Curations &nbsp;|&nbsp; Sydney</div>
  </div>
  <div class="hdr-right">
    <div class="badge">Limited Period Collection</div>
    <div class="hdr-occ">
      Varamahalakshmi &middot; Gauri Habba<br>
      Navaratri &middot; Housewarming
    </div>
  </div>
</div>

<!-- WELCOME -->
<div class="welcome">
  <h2>Celebrate the Sacred. Gift with Intention.</h2>
  <p>Handcrafted with devotion for Sydney families who honour tradition and refuse to compromise on beauty.</p>
</div>

<!-- DIVIDER -->
<div class="orn">
  <div class="orn-line"></div>
  <span class="orn-sym">✦ &nbsp; ✦ &nbsp; ✦</span>
  <div class="orn-line"></div>
</div>

<!-- COLLECTION 01 — TAMBULA -->
<div class="cat-band">
  <div class="cat-lhs">
    <div class="cat-num">Collection One</div>
    <div class="cat-title">Royal Tambula Gifting Box</div>
  </div>
  <div class="cat-occ">
    Varamahalakshmi &middot; Gauri Habba &middot; Navaratri<br>
    Housewarming Return Gifts &middot; Gruhapravesh
  </div>
</div>

<div class="cat-row">
  <div class="photo-panel">
    <img src="data:image/jpeg;base64,{TAMB}" alt="Tambula">
  </div>
  <div class="content-panel">
    <div class="prod-eyebrow">Royal Boutique Curation</div>
    <div class="prod-row">
      <div class="prod-name">Royal Tambula Gifting Box</div>
      <div class="prod-price-wrap">
        <span class="prod-price">{price_tamb}</span>
        <span class="prod-price-note">{price_note}</span>
      </div>
    </div>
    <div class="prod-sub">Handcrafted and styled to gift beautifully</div>
    <div class="divider-thin"></div>
    <div class="items-cols">
      <div class="grp">
        <div class="grp-label">Auspicious Essentials</div>
        <div class="itm"><span class="dot"></span>Arishina &amp; Kumkuma</div>
        <div class="itm"><span class="dot"></span>Fresh Betel Leaves &amp; Supari</div>
        <div class="itm"><span class="dot"></span>Dakshina</div>
      </div>
      <div class="grp">
        <div class="grp-label">Festive Gifting</div>
        <div class="itm"><span class="dot"></span>Traditional glass bangles set</div>
        <div class="itm"><span class="dot"></span>Premium aesthetic tea towel</div>
        <div class="itm"><span class="dot"></span>Mini golden organza keepsake box</div>
      </div>
    </div>
    <div class="addons-wrap">
      <div class="addons-box">
        <span class="addon-label">Luxury Add-ons</span>
        <span class="addon-items">{addon_tamb}</span>
      </div>
      <div class="box-note">Mini golden keepsake gift box</div>
    </div>
  </div>
</div>

<!-- DIVIDER -->
<div class="orn">
  <div class="orn-line"></div>
  <span class="orn-sym">✦ &nbsp; ✦ &nbsp; ✦</span>
  <div class="orn-line"></div>
</div>

<!-- COLLECTION 02 — BAAGINA -->
<div class="cat-band">
  <div class="cat-lhs">
    <div class="cat-num">Collection Two</div>
    <div class="cat-title">Royal Heritage Baagina Box</div>
  </div>
  <div class="cat-occ">
    Complete 16 Element Set &middot; Gauri Habba Ceremony
  </div>
</div>

<div class="cat-row">
  <div class="photo-panel">
    <img src="data:image/jpeg;base64,{BAAG}" alt="Baagina">
  </div>
  <div class="content-panel">
    <div class="prod-eyebrow">Complete 16 Element Ceremonial Set</div>
    <div class="prod-row">
      <div class="prod-name">Royal Heritage Baagina Box</div>
      <div class="prod-price-wrap">
        <span class="prod-price">{price_baag}</span>
        <span class="prod-price-note">{price_note}</span>
      </div>
    </div>
    <div class="prod-sub">Nothing left out. Everything curated with intention.</div>
    <div class="divider-thin"></div>
    <div class="items-cols">
      <div>
        <div class="grp">
          <div class="grp-label">Pancha Dhanya &amp; Staples</div>
          <div class="itm"><span class="dot"></span>Toor, Chana, Moong &amp; Urad Dal</div>
          <div class="itm"><span class="dot"></span>Rice, Wheat &amp; Rava</div>
          <div class="itm"><span class="dot"></span>6 reusable glass jars</div>
        </div>
        <div class="grp">
          <div class="grp-label">Sacred Samagri</div>
          <div class="itm"><span class="dot"></span>Acchu Bella (Jaggery block)</div>
          <div class="itm"><span class="dot"></span>Arishina &amp; Kumkuma</div>
          <div class="itm"><span class="dot"></span>Kannu Kappu</div>
          <div class="itm"><span class="dot"></span>Betel Leaves, Supari &amp; Dakshina</div>
        </div>
      </div>
      <div>
        <div class="grp">
          <div class="grp-label">Soubhagya Ornaments</div>
          <div class="itm"><span class="dot"></span>Traditional glass bangles</div>
          <div class="itm"><span class="dot"></span>Bichole &amp; Karimani</div>
          <div class="itm"><span class="dot"></span>Comb &amp; pocket mirror</div>
          <div class="itm"><span class="dot"></span>Traditional Jhumkas</div>
          <div class="itm"><span class="dot"></span>Premium tea towel</div>
        </div>
        <div class="grp">
          <div class="grp-label">Fresh Offerings</div>
          <div class="itm"><span class="dot"></span>Fresh coconut &amp; bananas</div>
        </div>
      </div>
    </div>
    <div class="addons-wrap">
      <div class="addons-box">
        <span class="addon-label">Luxury Add-ons</span>
        <span class="addon-items">{addon_baag}</span>
      </div>
      <div class="box-note">Large rigid golden keepsake box</div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<div class="order">
  <div class="order-head">Reserve Your Collection</div>
  <div class="order-sub">Strictly limited. Handcrafted to order. Sydney families only.</div>
  <div class="order-cols">
    <div class="order-col">
      <span class="o-lbl">Collection</span>
      <div class="o-val">Sydney pickup &amp;<br>local collection points</div>
    </div>
    <div class="order-col">
      <span class="o-lbl">Pre Order Required</span>
      <div class="o-val">Minimum 2 weeks<br>before Gauri Habba</div>
    </div>
    <div class="order-col">
      <span class="o-lbl">Availability</span>
      <div class="o-val">Limited batches only<br>First come, first served</div>
    </div>
  </div>
  <div class="order-cta">DM on Instagram &nbsp;<span>@leafyflavours</span></div>
</div>

</body>
</html>"""

# ── Render ────────────────────────────────────────────────────────────────────

def render(html: str, dest: str):
    tmp = '/private/tmp/brochure_render.html'
    with open(tmp, 'w') as f:
        f.write(html)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=1.56)
        page.goto(f'file://{tmp}')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2500)
        png = page.screenshot(clip={'x': 0, 'y': 0, 'width': 794, 'height': 1123})
        browser.close()
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(png)).convert('RGB')
    img.save(dest, format='JPEG', quality=95)
    print(f'Saved {img.size} → {dest}')

if __name__ == '__main__':
    priced_dest  = os.path.join(HERE, 'FestiveBrochure_LeafyFlavours.jpg')
    enquire_dest = os.path.join(HERE, 'FestiveBrochure_Enquire.jpg')

    render(make_html(show_prices=True),  priced_dest)
    render(make_html(show_prices=False), enquire_dest)
    print('Done.')
