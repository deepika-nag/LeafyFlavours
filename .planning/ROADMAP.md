# Roadmap — Leafy Flavours Web Menu

## Phase 1 — Launch (NOW)

**Goal:** Get the link live so Deepika can send it to clients today.

Steps:
1. Create GitHub account (if needed) — github.com
2. Create new public repo: `leafyflavours` (or `leafy-flavours-menu`)
3. Upload files: `index.html`, `images/` folder, `LeafyFlavours_Menu.pdf`, `Leafy favlours brand .png`
4. Enable GitHub Pages: Settings → Pages → Source: main branch → /root
5. URL will be: `https://[username].github.io/leafyflavours/`
6. Share that link via WhatsApp

**Time estimate:** 15–20 minutes first time. After that, edits are instant.

---

## Phase 2 — Mobile Editing (NEXT)

**Goal:** Deepika can update menu items, photos, and copy from her phone.

Options (pick one):
- **GitHub mobile web editor** — edit `index.html` directly in github.com on iPhone. Free. No app needed.
- **GitHub app** — iOS app for GitHub. Good for small edits.
- **prose.io** — cleaner mobile editing UI layered on top of GitHub. Free.

Content-only approach:
- All editable text is in `index.html` — search for any item name and change it
- To add a photo: convert to JPG, upload to `images/` folder on GitHub, reference in `index.html`

---

## Phase 3 — Growth (LATER)

- Custom domain if Deepika wants leafyflavours.com.au
- Enquiry form via Formspree
- Instagram link in footer
- Analytics if she wants to see how many people view the menu

---

## Editing Cheat Sheet (for Deepika)

| What to change | Where in index.html |
|----------------|---------------------|
| Menu item names | Search for the item name, edit the `<li>` or `<span>` text |
| Section intro copy | Each `<p>` under the experience `<h2>` |
| Contact phone number | Search "0470 382 859" |
| Hero tagline | Search "Celebrate. Share. Savour." |
| Add/remove gallery photo | Find `.gallery-grid` section, add/remove `<img>` tags |
| Change hero photo | Find `images/hero.jpg`, replace file in `images/` folder |
