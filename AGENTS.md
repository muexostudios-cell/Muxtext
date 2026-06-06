# AGENTS.md

## Cursor Cloud specific instructions

### Product overview

**MUX text-rpg · 文字地城** is a single-file, client-side browser game. The entire application lives in `README.md` (valid HTML). There is no backend, build step, package manager, test suite, or linter.

### Running the game locally

1. Copy the game file for HTTP serving (browsers handle `localStorage` more reliably over HTTP than `file://`):
   ```bash
   cp README.md index.html
   python3 -m http.server 8000
   ```
2. Open `http://localhost:8000/index.html` in a modern browser (Chrome/Firefox).

Alternatively, open `README.md` directly in a browser via `xdg-open README.md` (offline, no server).

### Hello-world smoke test

1. Enter a player name on the welcome overlay and confirm.
2. Click **> 地城** (`#btn-dungeon`).
3. Pick an available level (e.g. Lv.1–3), choose **普通** (normal), then **手動戰鬥** (manual) if the drone prompt appears.
4. Click an adjacent map cell to move or start combat.

### Services

| Service | Required? | Notes |
|---------|-----------|-------|
| Static HTTP server | Optional but recommended | `python3 -m http.server 8000` after copying to `index.html` |
| Web browser | Required | Game runs entirely in the browser |
| Database / Docker / Node | No | Not used |

### Lint / test / build

None configured. No `npm`, `make`, or CI targets exist in this repository.

### Gotchas

- **`index.html` is a dev convenience copy** of `README.md`; it is not tracked in git. Regenerate with `cp README.md index.html` after pulling changes to `README.md`.
- **New players** must use the top quick button `> 地城` (`#btn-dungeon`), not unrelated sidebar UI if testing in a generic browser layout.
- **Drone overlay**: when the player has a living drone, entering a normal dungeon shows a choice between drone auto-battle and manual combat; pick **手動戰鬥** for interactive testing.
- **Persistence**: saves use `localStorage` keys (`td_full_save`, `td_settings`, `td_lang`, etc.). Clear site data in DevTools for a clean run.
- **Debug hook**: `window.repairDrone` is exposed globally for drone repair during development.
