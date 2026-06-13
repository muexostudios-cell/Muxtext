/**
 * patch-combat-fix-v22477.mjs
 * Muxtext v2.24.76 → v2.24.77
 *
 * Root-cause fix for #combat-atk-bar invisible during battle:
 *   - CSS order:4 on #combat-dock put it BELOW the log-panel (flex:1),
 *     which consumed all remaining 850px space → combat-dock clipped by
 *     #game{overflow:hidden}.
 *   Fix: swap orders → combat-dock order:3 (+ flex-shrink:0),
 *        log-panel.log-visible order:4,
 *        equip/inventory/craft/profile-panel order:4.
 *
 * Also improves portrait rendering robustness
 * (already partially fixed in v2.24.76).
 */

import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dir = path.dirname(fileURLToPath(import.meta.url));
const ROOT  = path.resolve(__dir, '..');
const INDEX = path.join(ROOT, 'index.html');
const VERJ  = path.join(ROOT, 'version.json');

let html = readFileSync(INDEX, 'utf8');

const patches = [
  // ── Fix A ── combat-dock: order:4 → order:3;flex-shrink:0
  {
    id: 'combat-dock-order',
    from: '#game-main.combat-layout #combat-dock{order:4}',
    to:   '#game-main.combat-layout #combat-dock{order:3;flex-shrink:0}'
  },
  // ── Fix B ── log-panel: order:3 → order:4  (pushed below combat-dock)
  {
    id: 'log-panel-order',
    from: '#game-main.combat-layout #log-panel.log-visible{order:3;flex:1;min-height:0;display:flex!important;flex-direction:column;border-bottom:1px solid #1a1a1a}',
    to:   '#game-main.combat-layout #log-panel.log-visible{order:4;flex:1;min-height:0;display:flex!important;flex-direction:column;border-bottom:1px solid #1a1a1a}'
  },
  // ── Fix C ── side-panels (equip/inv/craft/profile): order:3 → order:4
  {
    id: 'side-panels-order',
    from: '#game-main.combat-layout #equip-panel.show,#game-main.combat-layout #inventory-panel.show,#game-main.combat-layout #craft-panel.show,#game-main.combat-layout #profile-panel.show{order:3;flex:1;min-height:0;overflow-y:auto}',
    to:   '#game-main.combat-layout #equip-panel.show,#game-main.combat-layout #inventory-panel.show,#game-main.combat-layout #craft-panel.show,#game-main.combat-layout #profile-panel.show{order:4;flex:1;min-height:0;overflow-y:auto}'
  },
  // ── Fix D ── version bump
  {
    id: 'version-bump',
    from: "GAME_VERSION='2.24.76'",
    to:   "GAME_VERSION='2.24.77'"
  }
];

let ok = true;
for (const p of patches) {
  const count = html.split(p.from).length - 1;
  if (count === 0) {
    console.error(`✗ [${p.id}] anchor NOT found — patch cannot apply`);
    ok = false;
  } else if (count > 1) {
    console.error(`✗ [${p.id}] anchor found ${count} times — ambiguous`);
    ok = false;
  } else {
    html = html.replace(p.from, p.to);
    console.log(`✓ [${p.id}]`);
  }
}

if (!ok) {
  console.error('\nOne or more patches failed — index.html NOT written.');
  process.exit(1);
}

writeFileSync(INDEX, html, 'utf8');
console.log('\nindex.html written.');

// version.json
const ver = JSON.parse(readFileSync(VERJ, 'utf8'));
ver.version = '2.24.77';
ver.updated = new Date().toISOString().slice(0, 10);
writeFileSync(VERJ, JSON.stringify(ver, null, 2) + '\n', 'utf8');
console.log('version.json updated.');
console.log('\nDone — v2.24.77 ready to push.');
