# MUX text-rpg · 文字地城

A single-page browser text RPG built with plain HTML, CSS, and JavaScript.

## Run locally

Open `index.html` directly in a browser, or serve the repository with a static file server:

```bash
python3 -m http.server 8080
```

Then visit <http://localhost:8080/>.

## Test

Browser smoke tests use Playwright:

```bash
npm install
npm test
```

The smoke test loads `index.html`, starts a manual dungeon run, and verifies the map renders.

## Project structure

- `index.html` - the game UI, styles, and game logic
- `tests/smoke.spec.js` - Playwright browser smoke test
- `package.json` - test scripts and development dependencies
