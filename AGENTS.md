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

Push to `main` triggers `.github/workflows/deploy-pages.yml` (GitHub Pages). **One-time:** repo owner must enable **Settings → Pages → Build and deployment → Source: GitHub Actions**. The workflow uses `enablement: true` but the token may lack permission to create the Pages site automatically.

### Gotchas

- Gun.js chat requires network; game core works offline after first load
- Desktop layout activates at width ≥ 900px
- Account saves: `td_accounts_v1` (local), `td_session` (active login)
- Cloud accounts: Gun.js `muxtext-cloud-v1/accounts/{key}` (AES-GCM encrypted, E2E)
- Cloud sync requires login each browser session (password held in memory only)
- Legacy keys (pre-account): `td_full_save`, `td_player_name`, `td_avatar`
- Global: `td_settings`, `td_lang`
