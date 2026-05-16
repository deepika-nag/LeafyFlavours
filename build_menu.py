#!/usr/bin/env python3
"""Leafy Flavours — Menu PDF Builder"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether, PageBreak,
    NextPageTemplate,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import os

# ── Brand colours ──────────────────────────────────────────────────────────────
TEAL       = HexColor('#1B6B6B')
TEAL_MID   = HexColor('#2A8A8A')
TEAL_LIGHT = HexColor('#DFF0F0')
GOLD       = HexColor('#F5B800')
GOLD_DARK  = HexColor('#B38600')
GOLD_LIGHT = HexColor('#FFF5CC')
CREAM      = HexColor('#FFFDF5')
DARK       = HexColor('#1A2A2A')
GREY       = HexColor('#666666')
WHITE      = white

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
CW = PAGE_W - 2 * MARGIN   # usable content width


# ── Style factory ──────────────────────────────────────────────────────────────
def S(name, font='Helvetica', size=10, color=DARK, align=TA_LEFT,
      leading=None, before=0, after=4, left=0, bold=False, italic=False):
    if bold and italic:
        font = 'Helvetica-BoldOblique'
    elif bold:
        font = 'Helvetica-Bold'
    elif italic:
        font = 'Helvetica-Oblique'
    return ParagraphStyle(
        name, fontName=font, fontSize=size,
        textColor=color, alignment=align,
        leading=leading or size * 1.4,
        spaceBefore=before, spaceAfter=after,
        leftIndent=left,
    )


# Pre-build the styles we use throughout
cover_title    = S('ct',   size=34, color=GOLD,      align=TA_CENTER, bold=True,   leading=40, after=4)
cover_by       = S('cby',  size=11, color=WHITE,     align=TA_CENTER, after=4)
cover_boutique = S('cbq',  size=12, color=WHITE,     align=TA_CENTER, italic=True, after=4)
cover_small    = S('csm',  size=8,  color=HexColor('#AADDDD'), align=TA_CENTER, after=3)
cover_tag      = S('ctag', size=10, color=GOLD,      align=TA_CENTER, bold=True,   after=4)
cover_contact  = S('cco',  size=9,  color=HexColor('#CCEEEE'), align=TA_CENTER, after=3)

page_h1        = S('ph1',  size=20, color=TEAL,      align=TA_CENTER, bold=True,   leading=24, before=4, after=6)
page_h2        = S('ph2',  size=14, color=TEAL,      align=TA_CENTER, bold=True,   leading=18, before=4, after=4)
body           = S('bod',  size=10, color=DARK,      align=TA_JUSTIFY,leading=16,  after=8)
body_c         = S('bodc', size=10, color=DARK,      align=TA_CENTER, leading=16,  after=6)
italic_c       = S('ic',   size=10, color=DARK,      align=TA_CENTER, italic=True, leading=16, after=8)
italic_sm      = S('ism',  size=9,  color=GREY,      align=TA_CENTER, italic=True, leading=14, after=4)
bold_teal      = S('bt',   size=10, color=TEAL,      bold=True,       leading=14,  after=2)
grey_sm        = S('gsm',  size=9,  color=GREY,      leading=13,      after=4,     left=14)

exp_num_style  = S('ens',  size=9,  color=GOLD_DARK, align=TA_CENTER, bold=True,   italic=True, after=2)
exp_title_s    = S('ets',  size=22, color=TEAL,      align=TA_CENTER, bold=True,   leading=26,  after=2)
exp_sub_s      = S('ess',  size=10, color=GOLD_DARK, align=TA_CENTER, bold=True,   italic=True, after=6)
exp_best_s     = S('ebs',  size=9,  color=GREY,      align=TA_CENTER, italic=True, leading=14,  after=4)
exp_pitch_s    = S('eps',  size=10, color=DARK,      align=TA_CENTER, italic=True, leading=17,  after=8)

cat_title_s    = S('cts',  size=9,  color=WHITE,     align=TA_CENTER, bold=True,   leading=13)
cat_instr_s    = S('cis',  size=8,  color=HexColor('#CCEEEE'), align=TA_CENTER, italic=True, leading=12)
cat_items_s    = S('cit',  size=10, color=DARK,      align=TA_CENTER, leading=17,  after=2)

tier_name_s    = S('tns',  size=12, color=TEAL,      bold=True,       leading=15,  after=1)
tier_sub_s     = S('tss',  size=9,  color=GOLD_DARK, italic=True,     leading=13,  after=2)
tier_desc_s    = S('tds',  size=9,  color=GREY,      italic=True,     leading=13,  after=4)
tier_pick_s    = S('tps',  size=9,  color=TEAL,      bold=True,       leading=14,  after=2)

choice_l_s     = S('cls',  size=9,  color=WHITE,     align=TA_CENTER, bold=True,   leading=14)
choice_r_s     = S('crs',  size=9,  color=DARK,      leading=14,      after=0)

step_num_s     = S('sns',  size=13, color=WHITE,     align=TA_CENTER, bold=True,   leading=17)
step_txt_s     = S('sts2', size=10, color=DARK,      leading=14,      after=0)

contact_head_s = S('chs',  size=16, color=TEAL,      align=TA_CENTER, bold=True,   leading=20,  after=4)
contact_line_s = S('cls2', size=11, color=DARK,      align=TA_CENTER, leading=18,  after=4)


# ── Page canvas callbacks ──────────────────────────────────────────────────────
def draw_cover_bg(c, doc):
    c.saveState()
    c.setFillColor(TEAL)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.rect(0.9 * cm, 0.9 * cm, PAGE_W - 1.8 * cm, PAGE_H - 1.8 * cm, fill=0, stroke=1)
    c.setLineWidth(0.4)
    c.rect(1.2 * cm, 1.2 * cm, PAGE_W - 2.4 * cm, PAGE_H - 2.4 * cm, fill=0, stroke=1)
    c.restoreState()


def draw_content_bg(c, doc):
    c.saveState()
    # teal top bar
    c.setFillColor(TEAL)
    c.rect(0, PAGE_H - 1.1 * cm, PAGE_W, 1.1 * cm, fill=1, stroke=0)
    # gold accent under top bar
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 1.25 * cm, PAGE_W, 0.14 * cm, fill=1, stroke=0)
    # header text
    c.setFillColor(GOLD)
    c.setFont('Helvetica', 7)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.7 * cm,
                        '@leafyflavours   ·   0470 382 859   ·   Kellyville, Sydney')
    # teal bottom bar
    c.setFillColor(TEAL)
    c.rect(0, 0, PAGE_W, 0.7 * cm, fill=1, stroke=0)
    c.restoreState()


# ── Helper flowables ───────────────────────────────────────────────────────────
def gold_rule(pct=70):
    return HRFlowable(width=f'{pct}%', thickness=1.2, color=GOLD,
                      spaceBefore=4, spaceAfter=6, hAlign='CENTER')


def teal_rule():
    return HRFlowable(width='100%', thickness=0.5, color=TEAL_LIGHT,
                      spaceBefore=4, spaceAfter=4)


def full_width_table(rows_data, style_cmds, row_heights=None):
    t = Table(rows_data, colWidths=[CW], rowHeights=row_heights)
    t.setStyle(TableStyle(style_cmds))
    return t


def exp_header(num, title, subtitle, best_for):
    """Coloured header block for each experience."""
    rows = [
        [Paragraph(f'— EXPERIENCE {num} —', exp_num_style)],
        [Paragraph(title, exp_title_s)],
        [Paragraph(subtitle, exp_sub_s)],
        [Paragraph(f'Best for: {best_for}', exp_best_s)],
    ]
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), GOLD_LIGHT),
        ('LINEABOVE',     (0, 0), (-1, 0),  3, TEAL),
        ('BOX',           (0, 0), (-1, -1), 0.75, GOLD),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return t


def cat_box(title, instruction, items_html):
    """Teal-header category selector box."""
    header = Table(
        [[Paragraph(title, cat_title_s)],
         [Paragraph(instruction, cat_instr_s)]],
        colWidths=[CW],
    )
    header.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), TEAL),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    body_cell = Table(
        [[Paragraph(items_html, cat_items_s)]],
        colWidths=[CW],
    )
    body_cell.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), TEAL_LIGHT),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
        ('BOX',           (0, 0), (-1, -1), 0.5, TEAL),
    ]))
    outer = Table([[header], [body_cell]], colWidths=[CW])
    outer.setStyle(TableStyle([
        ('BOX',           (0, 0), (-1, -1), 0.75, TEAL),
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))
    return outer


def choice_row(label, items_html):
    """Side-by-side teal label + item list row."""
    lw = CW * 0.30
    rw = CW * 0.70
    t = Table(
        [[Paragraph(label, choice_l_s),
          Paragraph(items_html, choice_r_s)]],
        colWidths=[lw, rw],
    )
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, 0), TEAL),
        ('BACKGROUND',    (1, 0), (1, 0), TEAL_LIGHT),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (0, 0),  6),
        ('RIGHTPADDING',  (0, 0), (0, 0),  6),
        ('LEFTPADDING',   (1, 0), (1, 0), 10),
        ('RIGHTPADDING',  (1, 0), (1, 0),  8),
        ('BOX',           (0, 0), (-1, -1), 0.4, TEAL),
    ]))
    return t


def tier_block(name, kannada_sub, desc, picks):
    """One tier card for the Karnataka Table."""
    lw = CW * 0.52
    rw = CW * 0.48
    top_row = Table(
        [[Paragraph(name, tier_name_s),
          Paragraph(kannada_sub, tier_sub_s)]],
        colWidths=[lw, rw],
    )
    top_row.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), GOLD_LIGHT),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW',     (0, 0), (-1, -1), 0.5, GOLD),
    ]))
    body_rows = Table(
        [[Paragraph(desc, tier_desc_s)],
         [Paragraph(picks, tier_pick_s)]],
        colWidths=[CW],
    )
    body_rows.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), CREAM),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    outer = Table([[top_row], [body_rows]], colWidths=[CW])
    outer.setStyle(TableStyle([
        ('BOX',           (0, 0), (-1, -1), 0.75, GOLD),
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))
    return outer


def course_row(name, sub, items_html):
    """One course row for Elle Oota."""
    lw = CW * 0.30
    rw = CW * 0.70
    left_cell = Table(
        [[Paragraph(name, S('crn', size=8, color=WHITE, align=TA_CENTER,
                            bold=True, leading=12, after=0))],
         [Paragraph(sub,  S('crs2', size=7, color=HexColor('#CCEEEE'),
                             align=TA_CENTER, italic=True, leading=11, after=0))]],
        colWidths=[lw],
    )
    left_cell.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), TEAL),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    right_cell = Paragraph(items_html, S('cri', size=9, color=DARK,
                                         leading=15, after=0))
    t = Table([[left_cell, right_cell]], colWidths=[lw, rw])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (1, 0), (1, 0), TEAL_LIGHT),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',   (1, 0), (1, 0), 10),
        ('RIGHTPADDING',  (1, 0), (1, 0), 8),
        ('TOPPADDING',    (1, 0), (1, 0), 0),
        ('BOTTOMPADDING', (1, 0), (1, 0), 0),
        ('BOX',           (0, 0), (-1, -1), 0.5, TEAL),
        ('LINEBELOW',     (0, 0), (-1, -1), 0.3, WHITE),
        ('TOPPADDING',    (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0),
        ('LEFTPADDING',   (0, 0), (0, 0), 0),
        ('RIGHTPADDING',  (0, 0), (0, 0), 0),
    ]))
    return t


# ── Page builders ──────────────────────────────────────────────────────────────

def cover_page(logo_path):
    e = []
    e.append(Spacer(1, 2.5 * cm))
    if os.path.exists(logo_path):
        img = Image(logo_path, width=5.2 * cm, height=5.2 * cm)
        img.hAlign = 'CENTER'
        e.append(img)
    e.append(Spacer(1, 0.6 * cm))
    e.append(Paragraph('LEAFY FLAVOURS', cover_title))
    e.append(Paragraph('by KitchenChimes', cover_by))
    e.append(Spacer(1, 0.5 * cm))
    e.append(HRFlowable(width='55%', thickness=1.5, color=GOLD,
                        spaceBefore=2, spaceAfter=6, hAlign='CENTER'))
    e.append(Paragraph('A Boutique Karnataka Food Experience', cover_boutique))
    e.append(Spacer(1, 0.3 * cm))
    e.append(Paragraph(
        'Taste of Mysuru  ·  Indian Street Bites  ·  Elle Oota Heritage Style',
        cover_small))
    e.append(Spacer(1, 1.8 * cm))
    e.append(HRFlowable(width='50%', thickness=1, color=GOLD,
                        spaceBefore=2, spaceAfter=6, hAlign='CENTER'))
    e.append(Paragraph('CELEBRATE  ·  SHARE  ·  SAVOUR', cover_tag))
    e.append(Spacer(1, 1.8 * cm))
    e.append(Paragraph('0470 382 859  |  Kellyville, Sydney', cover_contact))
    e.append(Paragraph('@leafyflavours', cover_contact))
    return e


def about_page():
    e = []
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph('Not Your Usual Caterer.', page_h1))
    e.append(gold_rule())

    e.append(Paragraph(
        'Leafy Flavours is a boutique food experience service based in Kellyville, Sydney. '
        'We specialise in authentic Karnataka cuisine — rooted in the flavours of Mysuru — '
        'and Indian street food that takes you straight back to the lanes of Bangalore or Delhi.',
        body))

    e.append(Paragraph(
        'We are not a bulk caterer. We do not do pickup trays or dabba deliveries. '
        'Every Leafy Flavours experience is curated, styled, and served at your venue. '
        'We bring the food, the setup, the table dressing, the branded signage, and a '
        'personalised experience — you just show up and celebrate.',
        body))

    e.append(Spacer(1, 0.2 * cm))

    why = [
        ('Authentic Karnataka & Chaat Cuisine',
         'Mysuru recipes made with care — kosumbri, puliyogare, masala puri, '
         'pani puri — the real thing, not a generic "South Indian" menu.'),
        ('Styled Setup Included',
         'Your table looks beautiful every time. Tiered stands, branded menu cards, '
         'table dressing, decorative props — all part of every experience.'),
        ('We Come to You',
         'We arrive, set up, serve, and pack down. You do not lift a finger.'),
        ('Personalised to Your Event & Theme',
         'Birthday, baby shower, haldi, housewarming, naming ceremony — we match '
         'your theme, your colour palette, your occasion.'),
        ('Boutique, Not Bulk',
         'Small batches, individual portions, real quality. '
         'Not a tray of food — an experience on a table.'),
    ]
    for title, desc in why:
        e.append(Paragraph(f'&#10022;  {title}', bold_teal))
        e.append(Paragraph(desc, grey_sm))

    e.append(Spacer(1, 0.2 * cm))
    e.append(teal_rule())

    e.append(Paragraph('How It Works', page_h2))

    steps = [
        ('1', 'Choose your experience — Street Table, Karnataka Table, or Elle Oota'),
        ('2', 'Tell us your guest count, date, and event theme'),
        ('3', 'We send your personalised quote — clear and complete'),
        ('4', 'We arrive, style the table, and take care of everything'),
        ('5', 'You celebrate. We pack down when the party is done.'),
    ]
    lw, rw = 0.9 * cm, CW - 1.1 * cm
    rows = [[Paragraph(n, step_num_s), Paragraph(t, step_txt_s)] for n, t in steps]
    st = Table(rows, colWidths=[lw, rw])
    st.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, -1), TEAL),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING',   (1, 0), (1, -1), 10),
        ('LINEBELOW',     (0, 0), (-1, -2), 0.4, TEAL_LIGHT),
    ]))
    e.append(st)
    return e


def street_table_page():
    e = []
    e.append(exp_header(
        '1',
        'THE STREET TABLE',
        'Galli Ka Andaaz, Aapke Ghar Mein',
        'Birthday parties  ·  Baby showers  ·  Haldi nights  ·  Kitty parties',
    ))
    e.append(Spacer(1, 0.3 * cm))
    e.append(Paragraph(
        '"You know that moment when guests walk into a party and their eyes go straight '
        'to the food table — and they just <i>know</i> this is going to be a good night? '
        'That is the Street Table. Indian street bites, styled and served at your venue. '
        'Your guests crowd around, share bites, argue about the chutneys. '
        'That galli energy — in your living room in Sydney."',
        exp_pitch_s))
    e.append(gold_rule())

    e.append(cat_box(
        'CHATPATA BITES',
        'choose any 3 to 5',
        'Maddur Vada Bites  ·  Dhokla Sticks  ·  Matar Kulche Boats  ·  Onion Bajji Sticks'
        '<br/>Churmuri Slices  ·  Pinwheel Samosas  ·  Nippat  ·  Masala Corn Salsa  ·  Guac Dips',
    ))
    e.append(Spacer(1, 0.3 * cm))

    e.append(cat_box(
        'THE HUNGRY CENTRE',
        'choose 1 or 2 — the crowd-puller of the table',
        'Masala Puri Cups  ·  Samosa Chaat Cups  ·  Vada Pav Sliders  ·  Naan Bhaji Boats',
    ))
    e.append(Spacer(1, 0.3 * cm))

    e.append(cat_box(
        'LEVEL UP YOUR TABLE',
        'optional stations — worth every single time',
        'DIY Pani Puri Station  ·  Papdi Chaat Platter  ·  Pakoda Platter',
    ))
    e.append(Spacer(1, 0.3 * cm))

    note = full_width_table(
        [[Paragraph(
            'All items are individually portioned and styled on a dressed table. '
            'Minimum 10 guests. Contact us for your personalised quote.',
            italic_sm)]],
        [('BACKGROUND', (0, 0), (-1, -1), GOLD_LIGHT),
         ('BOX',        (0, 0), (-1, -1), 0.5, GOLD),
         ('TOPPADDING', (0, 0), (-1, -1), 8),
         ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
         ('LEFTPADDING', (0, 0), (-1, -1), 12),
         ('RIGHTPADDING', (0, 0), (-1, -1), 12)],
    )
    e.append(note)
    return e


def karnataka_table_page():
    e = []
    e.append(exp_header(
        '2',
        'THE KARNATAKA TABLE',
        'Namma Oota, Namma Habba — Our Food, Our Festival',
        'Karnataka birthdays  ·  Housewarmings  ·  Naming ceremonies  ·  Ugadi  ·  Diwali',
    ))
    e.append(Spacer(1, 0.3 * cm))
    e.append(Paragraph(
        '"You know that smell before you even see the table — kosumbri, puliyogare, bonda soup. '
        'That is not just food. That is your paati\'s kitchen. That is Dasara morning. '
        'That is Ugadi lunch. The Karnataka Table brings those flavours back — '
        'styled, served, and set up at your celebration. '
        'For every Kannadiga at your party, this is homecoming."',
        exp_pitch_s))
    e.append(gold_rule())

    tiers = [
        (
            'TINDI HABBADA',
            'Small Celebration Bites',
            'Light and lovely — perfect as a starter spread, or pair with your own mains.',
            'Pick 2 Welcome Bites  +  1 Hot Off the Pan  +  1 Sweet Farewell',
        ),
        (
            'NAMMA HABBA  (Most Popular)',
            'Our Full Festival Table',
            'The complete Karnataka festive experience. The one every guest remembers.',
            'Pick 2 Welcome Bites  +  1 Hot Off the Pan  +  1 Heart of Karnataka  +  1 Sweet Farewell',
        ),
        (
            'RAJARA BENDIGE',
            'The Royal Evening Spread',
            'A full, abundant Karnataka table — for when you want to do it properly.',
            'Pick 3 Welcome Bites  +  1 Hot Off the Pan  +  2 Heart of Karnataka  +  1 Sweet Farewell',
        ),
    ]
    for nm, sub, desc, picks in tiers:
        e.append(tier_block(nm, sub, desc, picks))
        e.append(Spacer(1, 0.22 * cm))

    e.append(Spacer(1, 0.15 * cm))
    e.append(teal_rule())
    e.append(Paragraph('YOUR CHOICES', S('yc', size=9, color=TEAL, align=TA_CENTER,
                                         bold=True, leading=13, after=6)))

    choices = [
        ('WELCOME BITES',
         'Kosumbri Cups  ·  Rasayana Cups  ·  Usli Cups  ·  Bonda Soup Dips'),
        ('HOT OFF THE PAN',
         'Dill Masala Vada  ·  Aloo Bonda  ·  Maida Pakoda'),
        ('HEART OF KARNATAKA',
         'Gojjavalaki Boats  ·  Mavinkayi Chitranna Donne  ·  Puliyogare Batlu'
         '<br/>Rawa Idli Bites with Peanut Chutney  ·  Veg Pulao'),
        ('SWEET FAREWELL',
         'Gasa Gase Payasa Shots  ·  Paan Shots  ·  Custard Gulab Jamoon'),
    ]
    for lbl, items in choices:
        e.append(choice_row(lbl, items))
        e.append(Spacer(1, 0.12 * cm))

    e.append(Spacer(1, 0.2 * cm))
    note = full_width_table(
        [[Paragraph(
            'Minimum 10 guests. Styled setup, branded menu card, and table dressing always included. '
            'Contact us for your personalised quote.',
            italic_sm)]],
        [('BACKGROUND',    (0, 0), (-1, -1), GOLD_LIGHT),
         ('BOX',           (0, 0), (-1, -1), 0.5, GOLD),
         ('TOPPADDING',    (0, 0), (-1, -1), 8),
         ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
         ('LEFTPADDING',   (0, 0), (-1, -1), 12),
         ('RIGHTPADDING',  (0, 0), (-1, -1), 12)],
    )
    e.append(note)
    return e


def elle_oota_page():
    e = []
    e.append(exp_header(
        '3',
        'ELLE OOTA HERITAGE STYLE',
        'Traditional Karnataka Sit-Down Experience',
        'Intimate milestone celebrations  ·  Parents\' birthdays  ·  Family visits  ·  Small gatherings (8-20 guests)',
    ))
    e.append(Spacer(1, 0.3 * cm))
    e.append(Paragraph(
        '"In Karnataka, when food is served on a banana leaf, it is not just a meal — '
        'it is respect. It is love. It is <i>banni, oota maadi</i> — come, let us eat. '
        'Elle Oota Heritage Style brings a full traditional Karnataka sit-down meal '
        'to your dining table. Small group, full flavours, properly served. '
        'Not a buffet queue. Your guests sit. We serve. '
        'The way it was always meant to be."',
        exp_pitch_s))
    e.append(gold_rule())

    courses = [
        ('SWAGATA',
         'The Welcome Cup',
         'Kosumbri Cups  ·  Rasayana Cups  ·  Usli Cups  — choose one'),
        ('USIRU SOUP',
         'The Warming Course',
         'Bonda Soup Dips — hot bonda in thin Karnataka-style soup'),
        ('KARIGIDA',
         'Hot Off the Pan',
         'Dill Masala Vada  ·  Aloo Bonda  ·  Maida Pakoda  — choose one'),
        ('ANNA PALYA',
         'Main Dish One',
         'Gojjavalaki Boats  ·  Mavinkayi Chitranna Donne  ·  Puliyogare Batlu'
         '<br/>Rawa Idli Bites with Peanut Chutney  ·  Veg Pulao  — choose one'),
        ('INNORU ANNA',
         'Main Dish Two',
         'A second choice from the main dishes above'),
        ('SEETE MUKHA',
         'The Sweet Farewell',
         'Gasa Gase Payasa Shots  ·  Paan Shots  ·  Custard Gulab Jamoon  — choose one'),
    ]
    for nm, sub, items in courses:
        e.append(course_row(nm, sub, items))
        e.append(Spacer(1, 0.18 * cm))

    e.append(Spacer(1, 0.2 * cm))
    note = full_width_table(
        [[Paragraph(
            'Full table styling  ·  Printed menu card per guest  ·  Course service included\n'
            'Minimum 8 guests  ·  Maximum 20 guests  ·  Contact us to personalise your meal',
            italic_sm)]],
        [('BACKGROUND',    (0, 0), (-1, -1), GOLD_LIGHT),
         ('BOX',           (0, 0), (-1, -1), 0.5, GOLD),
         ('TOPPADDING',    (0, 0), (-1, -1), 8),
         ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
         ('LEFTPADDING',   (0, 0), (-1, -1), 12),
         ('RIGHTPADDING',  (0, 0), (-1, -1), 12)],
    )
    e.append(note)
    return e


def opening_act_contact_page():
    e = []

    # Opening Act header
    oa_header = full_width_table(
        [[Paragraph('THE OPENING ACT',
                    S('oah', size=18, color=GOLD, align=TA_CENTER,
                      bold=True, leading=22, after=0))]],
        [('BACKGROUND',    (0, 0), (-1, -1), TEAL),
         ('TOPPADDING',    (0, 0), (-1, -1), 12),
         ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
         ('LEFTPADDING',   (0, 0), (-1, -1), 10)],
    )
    e.append(oa_header)
    e.append(Spacer(1, 0.1 * cm))
    e.append(Paragraph(
        'Starters + Style — You Handle the Mains',
        S('oasub', size=10, color=GOLD_DARK, align=TA_CENTER,
          bold=True, italic=True, leading=14, after=6)))

    e.append(Paragraph(
        '"Getting biryani from your favourite place? Family cooking the mains? No problem. '
        'Book Leafy Flavours for just the starters and the styled setup. '
        'We bring the street bites or the Karnataka spread — dressed and ready '
        'before your first guest arrives. By the time the mains come out, '
        'everyone is already in party mode. <b>We do the wow factor. You do the rest.</b>"',
        italic_c))

    oa_box = full_width_table(
        [[Paragraph(
            'Choose any selection from Experience 1 (The Street Table) '
            'or Experience 2 (The Karnataka Table).\n'
            'Minimum 10 guests. Styled setup and table dressing always included — '
            'even for the starters-only edition.',
            S('oan', size=9, color=DARK, align=TA_CENTER, leading=15, after=0))]],
        [('BACKGROUND',    (0, 0), (-1, -1), GOLD_LIGHT),
         ('BOX',           (0, 0), (-1, -1), 0.75, GOLD),
         ('TOPPADDING',    (0, 0), (-1, -1), 10),
         ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
         ('LEFTPADDING',   (0, 0), (-1, -1), 14),
         ('RIGHTPADDING',  (0, 0), (-1, -1), 14)],
    )
    e.append(oa_box)

    e.append(Spacer(1, 0.4 * cm))
    e.append(teal_rule())
    e.append(Spacer(1, 0.2 * cm))

    # Theme matching
    e.append(Paragraph('We Match Your Theme', page_h2))
    e.append(Paragraph(
        'Every Leafy Flavours table is dressed to match your occasion. '
        'Tell us your theme — same food, completely different magic every time.',
        body_c))

    themes = [
        'Pastel Baby Shower', 'Bollywood Night', 'Royal Mysuru',
        "Kids' Unicorn Party", 'Pool Party Vibes', 'Rustic Outdoor',
        'Elegant Marble', 'Retro Vintage', 'Floral Garden',
    ]
    e.append(Paragraph(
        '  ·  '.join(themes),
        S('thm', size=9, color=TEAL, align=TA_CENTER,
          italic=True, leading=16, after=10)))

    e.append(teal_rule())
    e.append(Spacer(1, 0.3 * cm))

    # Contact
    e.append(Paragraph('Book Your Experience', contact_head_s))
    e.append(gold_rule(50))

    contact_info = [
        ['Phone', '0470 382 859'],
        ['Instagram', '@leafyflavours'],
        ['Location', 'Kellyville, Sydney  —  We travel to your venue'],
    ]
    for label, value in contact_info:
        lw = CW * 0.22
        rw = CW * 0.78
        row = Table(
            [[Paragraph(label, S('cl', size=9, color=WHITE, align=TA_CENTER,
                                 bold=True, leading=13, after=0)),
              Paragraph(value, S('cv', size=10, color=DARK, leading=14, after=0))]],
            colWidths=[lw, rw],
        )
        row.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (0, 0), TEAL),
            ('BACKGROUND',    (1, 0), (1, 0), CREAM),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING',    (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING',   (0, 0), (0, 0),  6),
            ('LEFTPADDING',   (1, 0), (1, 0), 12),
            ('BOX',           (0, 0), (-1, -1), 0.4, TEAL),
            ('LINEBELOW',     (0, 0), (-1, -1), 0.3, TEAL_LIGHT),
        ]))
        e.append(row)
        e.append(Spacer(1, 0.1 * cm))

    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph(
        'Contact us to receive your personalised quote.\n'
        'We work with your guest count, your budget, and your vision.',
        italic_sm))

    return e


# ── Assemble document ──────────────────────────────────────────────────────────
def build(output_path, logo_path):
    doc = BaseDocTemplate(
        output_path, pagesize=A4,
        title='Leafy Flavours — Menu 2025',
        author='Leafy Flavours by KitchenChimes',
    )

    cover_frame = Frame(
        0, 0, PAGE_W, PAGE_H,
        leftPadding=MARGIN + 0.5 * cm, rightPadding=MARGIN + 0.5 * cm,
        topPadding=1.5 * cm, bottomPadding=1.5 * cm,
        id='cover_frame',
    )
    content_frame = Frame(
        MARGIN, 0.9 * cm,
        CW, PAGE_H - 2.4 * cm,
        leftPadding=0, rightPadding=0,
        topPadding=0.3 * cm, bottomPadding=0.3 * cm,
        id='content_frame',
    )

    doc.addPageTemplates([
        PageTemplate(id='Cover',   frames=[cover_frame],   onPage=draw_cover_bg),
        PageTemplate(id='Content', frames=[content_frame], onPage=draw_content_bg),
    ])

    story = []
    story += cover_page(logo_path)
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())
    story += about_page()
    story.append(PageBreak())
    story += street_table_page()
    story.append(PageBreak())
    story += karnataka_table_page()
    story.append(PageBreak())
    story += elle_oota_page()
    story.append(PageBreak())
    story += opening_act_contact_page()

    doc.build(story)
    print(f'Done: {output_path}')


if __name__ == '__main__':
    BASE = '/Users/deepika.nagaraja/Documents/QE_AI_LAB/LeafyFlavours'
    build(
        output_path=os.path.join(BASE, 'LeafyFlavours_Menu.pdf'),
        logo_path=os.path.join(BASE, 'Leafy favlours brand .png'),
    )
