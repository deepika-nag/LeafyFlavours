# Leafy Flavours — Project Context

Drop this file into any Claude Code session and say: "Read LEAFY_FLAVOURS_CONTEXT.md and pick up from there."

---

## The Business

**Leafy Flavours** by KitchenChimes
Owner: Deepika Nagaraja | 0470 382 859 | Kellyville, Sydney | @leafyflavours

A **boutique Karnataka food experience service** — not a bulk caterer, not pickup.
Deepika arrives at client's venue, styles the table, serves the food, packs down.
Speciality: Mysuru/Karnataka cuisine + Indian street food/chaats.
Target market: Indian community in Sydney for birthdays, baby showers, housewarmings.

**The core problem solved:** Old menus looked like a takeaway order form → clients compared to bulk caterers → price shock at end → lost orders. New approach: sell experiences not items, no prices on menu, contact for quote.

---

## Brand

- Teal `#1B6B6B` + Gold `#F5B800`
- Logo: `Leafy favlours brand .png` (round yellow badge, Mysore Palace)
- Tagline: Celebrate. Share. Savour.

---

## The Three Experiences + Opening Act

### Experience 1 — THE STREET TABLE
*Galli Ka Andaaz, Aapke Ghar Mein*

**CHATPATA BITES** (choose 3–5): Maddur Vada Bites · Dhokla Sticks · Matar Kulche Boats · Onion Bajji Sticks · Churmuri Slices · Pinwheel Samosas · Nippat · Masala Corn Salsa · Guac Dips

**THE HUNGRY CENTRE** (choose 1–2): Masala Puri Cups · Samosa Chaat Cups · Vada Pav Sliders · Naan Bhaji Boats

**LEVEL UP** (optional): DIY Pani Puri Station · Papdi Chaat Platter · Pakoda Platter

---

### Experience 2 — THE KARNATAKA TABLE
*Namma Oota, Namma Habba*

| Tier | Kannada Name | What's Included |
|------|-------------|-----------------|
| Light | TINDI HABBADA | 2 Welcome Bites + 1 Fried + 1 Sweet |
| Popular ⭐ | NAMMA HABBA | 2 Welcome Bites + 1 Fried + 1 Hearty + 1 Sweet |
| Full | RAJARA BENDIGE | 3 Welcome Bites + 1 Fried + 2 Hearty + 1 Sweet |

**WELCOME BITES:** Kosumbri Cups · Rasayana Cups · Usli Cups · Bonda Soup Dips
**HOT OFF THE PAN:** Dill Masala Vada · Aloo Bonda · Maida Pakoda
**HEART OF KARNATAKA:** Gojjavalaki Boats · Chitranna Donne · Puliyogare Batlu · Rawa Idli Bites · Veg Pulao
**SWEET FAREWELL:** Gasa Gase Payasa Shots · Paan Shots · Custard Gulab Jamoon

---

### Experience 3 — ELLE OOTA HERITAGE STYLE
*Traditional Karnataka Sit-Down Experience* | 8–20 guests

6-course Karnataka meal served at client's dining table:
SWAGATA (welcome) → USIRU SOUP (bonda soup) → KARIGIDA (fried) → ANNA PALYA (main 1) → INNORU ANNA (main 2) → SEETE MUKHA (sweet)

---

### The Opening Act
Starters only — client brings their own mains. Same styled setup, same Leafy Flavours experience.
"We do the wow factor. You do the rest."

---

## Pricing (Internal Reference — NOT on client menu)

| Item Type | Price |
|-----------|-------|
| Street Bites & Dips | $6 per portion |
| Hearty Street Eats | $7 per portion |
| Grazing Platters | $50 flat |
| Karnataka Welcome Bites | $3pp (Bonda Soup $6pp) |
| Karnataka Fried | $5pp (2 pcs) |
| Karnataka Hearty Fillers | $10pp |
| Karnataka Sweets | $3pp |

Tindi Habbada = $14pp | Namma Habba = $24pp | Rajara Bendige = $37pp | Elle Oota = $37pp

---

## Files

| File | Purpose |
|------|---------|
| `LeafyFlavours_Menu.pdf` | 6-page client-facing menu (no prices) |
| `build_menu.py` | Python/reportlab script — run to regenerate PDF |
| `Leafy favlours brand .png` | Brand logo |
| `LeafyLFavours chaats grazing menu.pdf` | Old chaats menu (reference only) |
| `Leafy Flavours Karnataka Menu.jpg` | Old Karnataka menu (reference only) |

---

## Rebuild the PDF

```bash
cd /Users/deepika.nagaraja/Documents/QE_AI_LAB/LeafyFlavours
python3 build_menu.py
```

Output: `LeafyFlavours_Menu.pdf` — ready to send to clients.

---

## Elevated Pitches (Use These Everywhere)

### About Leafy Flavours
"Most Indian catering in Sydney hands you a tray. We hand you an experience.

Leafy Flavours is a boutique food experience service based in Kellyville, Sydney. We specialise in authentic Mysuru and Karnataka cuisine — and Indian street food done properly — styled and served at your venue. Not a bulk caterer. Not a pickup service. We arrive, dress your table, serve your guests, and leave it spotless. What stays behind is the memory of a spread that felt like it actually meant something.

Because Karnataka food deserves more than a disposable container."

### Experience 1 — The Street Table
"You know the moment. Before anyone has sat down, someone has spotted the table and is already in the group chat. Masala puri cups that crack when you press the spoon in. Pani puri you fill yourself. Bites that taste like Bangalore's best lanes — except it's your living room in Sydney and we've already done all the work.

Indian street food as a centrepiece. Not an afterthought."

### Experience 2 — The Karnataka Table
"Your paati never catered a party. She cooked one. There's a difference.

The Karnataka Table is the closest your Sydney celebration can get to a home-cooked Karnataka spread — without anyone spending three days in the kitchen. Kosumbri made fresh. Puliyogare that smells like a Sunday in Mysuru. Bonda soup that your oldest aunty will quietly approve of.

Styled for your occasion. Specific to one region — because Karnataka food isn't just 'South Indian.' It has a voice of its own."

### Experience 3 — Elle Oota Heritage Style
"Some meals you eat. Some meals you remember.

Elle Oota is a full Karnataka sit-down meal served course by course at your own dining table. Welcome cup, bonda soup, something fried, two mains, a sweet farewell — the rhythm of a proper oota, in your home, for your people.

Your guests are seated. We serve. No buffet queue, no compromise on the meal."

### The Opening Act
"You've got the biryani sorted. Your family is bringing the dal. But the table still looks like a table.

Let us handle the opening. We bring the starters and the setup — dressed and ready before your first guest arrives. By the time the mains land, everyone's already in party mode. You take all the credit. That's the deal."

## What's Next (Web Menu)

Goal: A shareable link Deepika can send via WhatsApp to clients instead of a PDF.
Built as: static HTML site on GitHub Pages (free, permanent URL, mobile-friendly).
GSD project: initialised at `/Users/deepika.nagaraja/Documents/QE_AI_LAB/LeafyFlavours`
