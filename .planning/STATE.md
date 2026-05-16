# Project State

Last updated: 2026-05-16

## Current Phase: 1 — Launch

## Done

- [x] Business restructured into 4 named experiences (no prices on menu)
- [x] `index.html` built — full single-page website with brand colours, photos, elevated pitches
- [x] `images/` folder set up with 13 photos (HEIC → JPG converted)
- [x] `LeafyFlavours_Menu.pdf` generated (6-page PDF via reportlab)
- [x] `build_menu.py` — reusable PDF rebuild script
- [x] `LEAFY_FLAVOURS_CONTEXT.md` — reusable session context file
- [x] GSD project initialised (.planning/ created)

## In Progress

- [ ] GitHub repo creation + Pages deployment

## Blocked / Waiting

- GitHub account needed to push and deploy
- Deepika to confirm GitHub username so Pages URL can be confirmed

## Next Actions

1. Deepika creates GitHub repo (or shares existing username)
2. Push files to repo
3. Enable GitHub Pages
4. Test link on mobile
5. Share with first client

## Notes

- HEIC → JPG conversion: use `sips -s format jpeg` + `sips -Z 800` to resize
- PDF download link in `index.html` references `LeafyFlavours_Menu.pdf` — must be in repo root
- Logo file has a space in name: `Leafy favlours brand .png` — already renamed to `images/logo.png`
