# AGENTS.md

## Cursor Cloud specific instructions

### Product

**MUX text-rpg · 文字地城** — browser text RPG. Canonical game source is `index.html` (not README.md).

### Play URL

- Production: https://muexostudios-cell.github.io/Muxtext/
- Local: `python3 -m http.server 8000` → http://localhost:8000/

### Development

- Edit **`index.html`** for game changes
- `README.md` is project documentation only
- No package manager, build step, or test suite

### Deploy

Push to `main` triggers `.github/workflows/deploy-pages.yml` (GitHub Pages). Ensure repo **Settings → Pages → Source: GitHub Actions**.

### Gotchas

- Gun.js chat requires network; game core works offline after first load
- Desktop layout activates at width ≥ 900px
- `localStorage` keys: `td_full_save`, `td_settings`, `td_lang`, etc.
