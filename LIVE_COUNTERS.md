# Live Counters — Notes & Poster Source

Working notes for the live-counter offering and the standalone **Unlimited Dosa Feast** collab poster.
This is a **separate venture / collaboration** — posters here intentionally carry **no "Leafy Flavours" branding**.

---

## Contact (to add to poster later)

- **Phone / WhatsApp:** 0470382859
- _Not printed on the poster yet — add when ready._

## General terms

- **Minimum 25 guests**
- Pricing/duration is **hourly basis** — discussed with the customer at enquiry (do not state duration on the poster).
- Made fresh, live, in front of guests.

---

## The Live Counters (3)

On the main Leafy Flavours site these appear as **Experience 4 — Live Counters**:

1. **Dosa Counter** — *Mysuru Dosa Mela*. Benne masala dosa, set dosa, uttapam and more, crisped to order on a live tava.
2. **Churmuri Chaat Counter** — *Karnataka Style*. Puffed rice tossed fresh with raw mango, carrot, onion and Karnataka spice.
3. **Hot Chaat Counter** — *Built to Order*. Live chaat station layering crunch, chutneys and masala.

---

## Unlimited Dosa Feast — Poster Spec

**Price:** Starting from **$30 per person**

**Tagline:** Crisp · Golden · Made to Order

**Intro:** Wow your guests with a live dosa counter — crisp, golden and sizzling straight off the
pan. Every dosa is included and served unlimited, made fresh to order in front of them.

### The Dosa Menu — all included at $30 (guests don't choose, everything is offered)
- Mysuru Masala Dosa
- Benne Masala Dosa
- Plain Dosa
- Onion Chilli Uttapam
- Onion Capsicum Uttapam

### Toppings — choose any 3, included
Cheese · Onion · Capsicum · Chilli · Corn · Tomato · Beetroot · (& more on request)

### Every plate includes (no extra charge)
- Fresh Coconut Chutney
- Hot Sambar
- Choice of Rice Item _(options discussed at enquiry)_

### Add-ons (elevate the spread)
| Add-on | Description | Price |
|---|---|---|
| Live Akki Rotti | Made fresh at the counter | + $3 |
| Kesari Bath | Warm saffron semolina sweet | + $2 |
| Shavige Bath | Spiced South-Indian vermicelli | + $2 |
| Veg Saagu | Karnataka-style coconut veg curry | + $2 |
| Extra Toppings | Beyond your 3 included | + 50¢ each |

---

## Files

- **`dosa-feast-poster.html`** — single editable poster source (green/yellow, ~3:4 portrait, two-column).
  Renders **two versions** from the same file via a URL flag:
  - **Branded** (`?branded`) — adds *"Leafy Flavours presents"* at the top + phone number in the
    footer; photo crop shows the full Mysuru Dosa Mela board (brand on the board is fine here).
  - **Collab** (no flag, default) — no brand line, no contact; photo crop shifted down so the
    board's *"Leafy flavours"* script is cropped out.
- **`Dosa-Feast-Poster-LeafyFlavours.jpg`** — branded export (~2184×3045).
- **`Dosa-Feast-Poster-Collab.jpg`** — unbranded collab export (~2184×2904).

### How to re-export both JPEGs after editing the HTML
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Branded
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1092,1700 --default-background-color=0C3E26FF \
  --screenshot="$PWD/branded.png" "file://$PWD/dosa-feast-poster.html?branded"
# Collab
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1092,1620 --default-background-color=0C3E26FF \
  --screenshot="$PWD/collab.png" "file://$PWD/dosa-feast-poster.html"
sips -s format jpeg -s formatOptions 88 branded.png --out "Dosa-Feast-Poster-LeafyFlavours.jpg"
sips -s format jpeg -s formatOptions 88 collab.png  --out "Dosa-Feast-Poster-Collab.jpg"
rm branded.png collab.png
# (trim the extra bottom green margin to a clean even frame — see git history for the PIL snippet)
```

## Done / decisions
- ✓ Two versions produced (branded + collab).
- ✓ Branded footer carries the phone number: **0470 382 859**.
- ✓ "Leafy flavours" on the board: shown on branded, cropped out on collab (photo `object-position`).
