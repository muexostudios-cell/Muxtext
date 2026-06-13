#!/usr/bin/env node
/**
 * patch-combat-fix-v22476.mjs
 *
 * Fixes two bugs in v2.24.75:
 *   1. Pixel combat portraits appear blurry / invisible
 *      - cachePixelIcon() used gridToDataUrl (16×16 canvas) for all pixel icons.
 *        At 86px display size that is a 5.4× upscale with no pixelated rendering,
 *        resulting in a blurry blob on a dark background.
 *      - Fix A: add image-rendering:pixelated;image-rendering:crisp-edges to
 *               the .pixel-icon CSS rule so ALL pixel art is crisp.
 *      - Fix B: switch cachePixelIcon() from gridToDataUrl (16×16) to
 *               gridToCombatDataUrl (32×32) so every icon starts sharper.
 *
 *   2. Attack buttons (#btn-atk-main / #btn-atk-off) appear invisible / missing
 *      - updateWeaponAttackButtons() rewrites button.className to
 *        'combat-atk-btn' + rarity, which silently removes the 'ready' class
 *        that setAtkBtnStyle(true) had just added.
 *      - Without 'ready': buttons render as color:#aaa on #050505 background —
 *        nearly invisible against the black UI.  When disabled (cooldown /
 *        processing), opacity drops to 0.25, making them essentially transparent.
 *      - Fix: append a setAtkBtnStyle() call at the end of updateWeaponAttackButtons()
 *             so the correct ready state is restored after each className overwrite,
 *             regardless of which code path invoked the function.
 *
 * Version bump: 2.24.75 → 2.24.76
 *
 * Usage (from Muxtext repo root):
 *   node tools/patch-combat-fix-v22476.mjs
 */

import fs from 'fs';

const path = './index.html';
let html = fs.readFileSync(path, 'utf8');

const OLD_VER = '2.24.75';
const NEW_VER = '2.24.76';
const TODAY   = '2026-06-13';

const patches = [];

function apply(description, oldStr, newStr) {
  if (!html.includes(oldStr)) {
    throw new Error(`Patch "${description}" failed — anchor not found in index.html`);
  }
  html = html.replace(oldStr, newStr);
  patches.push(description);
}

// ─── Fix A: image-rendering:pixelated on .pixel-icon ─────────────────────────
apply(
  'add image-rendering:pixelated to .pixel-icon CSS',
  '.pixel-icon{width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain}',
  '.pixel-icon{width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain;image-rendering:pixelated;image-rendering:crisp-edges}'
);

// ─── Fix B: cachePixelIcon — use 32×32 canvas for sharper base images ────────
apply(
  'cachePixelIcon: gridToDataUrl → gridToCombatDataUrl (16→32px canvas)',
  'function cachePixelIcon(key,grid){if(_pixelIconCache.size>=_PIXEL_ICON_CACHE_MAX)_pixelIconCache.clear();const url=gridToDataUrl(grid);_pixelIconCache.set(key,url);return url;}',
  'function cachePixelIcon(key,grid){if(_pixelIconCache.size>=_PIXEL_ICON_CACHE_MAX)_pixelIconCache.clear();const url=gridToCombatDataUrl(grid);_pixelIconCache.set(key,url);return url;}'
);

// ─── Fix 2: updateWeaponAttackButtons — restore ready state after className overwrite ──
//
// The function rewrites btn.className which strips the 'ready' class set by
// setAtkBtnStyle().  Appending a setAtkBtnStyle() call at the end ensures the
// accent-colour highlight is re-applied every time weapon labels are refreshed,
// whether called from updateButtons() or updateCombatItemBarVisibility().
apply(
  'updateWeaponAttackButtons: restore ready class after className overwrite',
  "main.className='combat-atk-btn'+(m?' rarity-'+m.rarity:'');off.className='combat-atk-btn'+(o?' rarity-'+o.rarity:'');}",
  "main.className='combat-atk-btn'+(m?' rarity-'+m.rarity:'');off.className='combat-atk-btn'+(o?' rarity-'+o.rarity:'');const _rdy=!!(typeof inCombat!=='undefined'&&inCombat&&typeof currentEnemy!=='undefined'&&currentEnemy&&!gameOver&&!isProcessingQueue&&Date.now()>=(typeof playerAttackCooldownUntil!=='undefined'?playerAttackCooldownUntil:0));setAtkBtnStyle(_rdy);}"
);

// ─── Version bump ─────────────────────────────────────────────────────────────
apply('GAME_VERSION constant',      `GAME_VERSION='${OLD_VER}'`,  `GAME_VERSION='${NEW_VER}'`);
apply('content meta version tag',   `content="${OLD_VER}"`,       `content="${NEW_VER}"`);

apply(
  'prepend version history entry',
  `GAME_VERSION_HISTORY=[{version:'${OLD_VER}'`,
  `GAME_VERSION_HISTORY=[{version:'${NEW_VER}',date:'${TODAY}',summary:{` +
    `zh:'v${NEW_VER} 修復戰鬥像素肖像模糊消失（image-rendering:pixelated + 32px 畫布）；修復攻擊按鈕 ready 高亮因 className 覆蓋而遺失。',` +
    `en:'v${NEW_VER} fix blurry/invisible combat pixel portraits (image-rendering:pixelated + 32px canvas); fix attack-button ready accent lost after className overwrite.'` +
  `}},{version:'${OLD_VER}'`
);

apply(
  'prepend balance-log entry',
  `logBalanceV22475:`,
  `logBalanceV22476:'[修復 v${NEW_VER}] ` +
    `像素肖像新增 image-rendering:pixelated 及升級至 32px 畫布，消除放大模糊；` +
    `updateWeaponAttackButtons 末端補呼叫 setAtkBtnStyle，修復攻擊按鈕 ready 高亮顏色遺失。',` +
  `logBalanceV22475:`
);

// ─── Write output ─────────────────────────────────────────────────────────────
fs.writeFileSync(path, html);

try {
  const vj = JSON.parse(fs.readFileSync('./version.json', 'utf8'));
  vj.version = NEW_VER;
  vj.updated = TODAY;
  fs.writeFileSync('./version.json', JSON.stringify(vj, null, 2) + '\n');
  patches.push('version.json updated');
} catch {
  // version.json is optional
}

console.log(`\n✓ Applied ${patches.length} patches (${OLD_VER} → ${NEW_VER}):\n`);
patches.forEach((p, i) => console.log(`  ${i + 1}. ${p}`));
console.log('');
