# Leafy Flavours — Claude Code Instructions

## Quick Context

This is a static HTML website for Leafy Flavours, a boutique Karnataka food experience service in Sydney.
Owner: Deepika Nagaraja | @leafyflavours | Kellyville

Full context: read `LEAFY_FLAVOURS_CONTEXT.md`
Project planning: read `.planning/PROJECT.md`

## Files

- `index.html` — the entire website (single file)
- `images/` — all photos used in the site
- `LeafyFlavours_Menu.pdf` — downloadable PDF (regenerate with `python3 build_menu.py`)
- `build_menu.py` — PDF rebuild script

## Rules

- NO prices on any client-facing content (PDF or website)
- NO frameworks, no npm, no build step — plain HTML/CSS only
- Brand: Teal `#1B6B6B` + Gold `#F5B800` + Cream `#FFFDF5`
- Fonts: Playfair Display (headings) + Lato (body) via Google Fonts
- Mobile-first — WhatsApp sharing is the primary distribution channel
- All copy should feel warm, cultural, personal — NOT corporate

## Pricing (internal only — never put on site or PDF)

Tindi Habbada $14pp | Namma Habba $24pp | Rajara Bendige $37pp | Elle Oota $37pp
Street Bites $6pp | Hearty Street Eats $7pp | Platters $50 flat

## When Editing

- Edit text: search for the exact phrase in `index.html` and update inline
- Add photo: copy JPG to `images/`, add `<img src="images/filename.jpg">` in right section
- Rebuild PDF: `python3 build_menu.py` → overwrites `LeafyFlavours_Menu.pdf`
- Deploy: `git add . && git commit -m "update" && git push` → GitHub Pages auto-deploys
