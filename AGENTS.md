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

### Bug Pipeline Worker

- Config in `index.html`: `BUG_PIPELINE_CONFIG.endpoint` (empty until worker is deployed)
- Worker source: `workers/bug-pipeline/` (`/health`, `/status`, `/report`, `/probe`)
- **One-time setup** (Account ID is auto-resolved from token):
  1. [Create API token](https://dash.cloudflare.com/profile/api-tokens) — template **Edit Cloudflare Workers**
  2. On Cursor Cloud / local VM (paste token once):
     ```bash
     CLOUDFLARE_API_TOKEN=your_token bash tools/setup-cloudflare-auto.sh
     ```
     This verifies the token, resolves Account ID, deploys the worker, patches `index.html`, sets GitHub Secrets (if `gh` has admin), and triggers CI.
  3. Or add only `CLOUDFLARE_API_TOKEN` to GitHub Actions secrets and run workflow *Deploy Bug Pipeline Worker*
- Optional: `cd workers/bug-pipeline && npx wrangler secret put OPENAI_API_KEY` for AI triage
- Without token the workflow **skips** deploy (warning only); game shows Bug 監測「未連線」 and works offline

### Stripe live payments

- Config in `index.html`: `PAYMENT_CONFIG` (`mode`, `pkLive`, `pkTest`, `verifyEndpoint`, `allowLiveTrustRedirect`)
- Localhost auto-uses **test** keys/links; production uses **live**
- Create live Payment Links: `STRIPE_SECRET_KEY=sk_live_... node tools/setup-stripe-payment-links.mjs --mode live --write-index`
- **Deploy verify worker** (pick one):
  1. **GitHub Actions** — repo Settings → Secrets → add `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `STRIPE_SECRET_KEY` (`rk_live_` or `sk_live_`), then run workflow *Deploy Stripe Verify Worker*
  2. **Local Wrangler** — `CLOUDFLARE_API_TOKEN=... STRIPE_SECRET_KEY=rk_live_... bash tools/deploy-stripe-verify.sh`
  3. **Vercel** — connect repo, set `STRIPE_SECRET_KEY`, use `https://<project>.vercel.app/api/stripe-verify` as `verifyEndpoint`
- After deploy: set `verifyEndpoint` to worker/API URL and `allowLiveTrustRedirect: false`
- Never commit `sk_live_` / `rk_live_` to the repo (`pk_live_` is public)
