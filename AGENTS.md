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
- No build step or bundler — static `index.html` served as-is
- **Dev server:** `python3 -m http.server 8000` → http://localhost:8000/
- **Tests:** `npm install` then `npx playwright install chromium` (first time only), then `npm test`
- **Lint:** none configured (no ESLint/Prettier in repo)

### Cloud agent startup

1. `python3 -m http.server 8000` (tmux or background) for browser testing at http://localhost:8000/
2. Outbound network required for Gun.js CDN + `https://gun.o8.is/gun` (account register/login blocks until relay is ready)
3. Playwright smoke test uses fixed username `smoke_test`; if that account already exists on Gun cloud, registration fails — use a unique username for manual hello-world demos

### Hello-world smoke test

1. Log in or register on the account overlay.
2. Click **> 地城** (`#btn-dungeon`).
3. Pick an available level (e.g. Lv.1–3), choose **普通** (normal), then **手動戰鬥** (manual) if the drone prompt appears.
4. Click an adjacent map cell to move or start combat.

### Deploy

Push to `main` triggers `.github/workflows/deploy-pages.yml` (GitHub Pages). **One-time:** repo owner must enable **Settings → Pages → Build and deployment → Source: GitHub Actions**. The workflow uses `enablement: true` but the token may lack permission to create the Pages site automatically.

### Gotchas

- Gun.js chat requires network; game core works offline after first load
- Desktop layout activates at width ≥ 900px
- Mobile chat: **> 聊天室** tab between 裝備 and 背包 opens `#chat-overlay`
- Account saves: `td_accounts_v1` (local), `td_session` (active login)
- Cloud accounts: Gun.js `muxtext-cloud-v1/accounts/{key}` (AES-GCM encrypted, E2E)
- Cloud sync requires login each browser session (password held in memory only)
- Legacy keys (pre-account): `td_full_save`, `td_player_name`, `td_avatar`
- Global: `td_settings`, `td_lang`
- **Debug hook**: `window.repairDrone` is exposed globally for drone repair during development
