import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const mapOld =
  '#map{gap:.14rem;max-width:336px;padding:.18rem;background-color:#04070f;background-image:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,229,255,.07) 3px,rgba(0,229,255,.07) 4px),repeating-linear-gradient(90deg,transparent,transparent 3px,rgba(0,229,255,.05) 3px,rgba(0,229,255,.05) 4px);border:1px solid #223a58;border-radius:2px;box-shadow:inset 0 2px 10px rgba(0,0,0,.5)}';
const mapNew =
  '#map{gap:.14rem;max-width:336px;padding:.18rem;background-color:#04070f;background-image:none;border:1px solid #223a58;border-radius:2px;box-shadow:inset 0 2px 10px rgba(0,0,0,.5)}';

const cellOld = '.cell{position:relative;overflow:visible;background:linear-gradient(155deg,#eef0f4 0%,#e4e7ee 100%)';
const cellNew = '.cell{position:relative;overflow:hidden;background:linear-gradient(155deg,#eef0f4 0%,#e4e7ee 100%)';

const monsterShadowOld =
  '.cell.tile-monster,.cell.unexplored-monster{background:linear-gradient(155deg,#f05252 0%,#dc2626 100%);border-color:#b91c1c;box-shadow:inset 0 1px 0 rgba(255,180,180,.35),0 0 6px rgba(220,38,38,.25)}';
const monsterShadowNew =
  '.cell.tile-monster,.cell.unexplored-monster{background:linear-gradient(155deg,#f05252 0%,#dc2626 100%);border-color:#b91c1c;box-shadow:inset 0 1px 0 rgba(255,180,180,.35),inset 0 -1px 3px rgba(0,0,0,.2)}';

const treasureShadowOld =
  '.cell.tile-treasure,.cell.unexplored-treasure{background:linear-gradient(155deg,#ffd54f 0%,#ffb300 100%);border-color:#c49000;box-shadow:inset 0 1px 0 rgba(255,240,180,.5),0 0 5px rgba(255,179,0,.2)}';
const treasureShadowNew =
  '.cell.tile-treasure,.cell.unexplored-treasure{background:linear-gradient(155deg,#ffd54f 0%,#ffb300 100%);border-color:#c49000;box-shadow:inset 0 1px 0 rgba(255,240,180,.5),inset 0 -1px 3px rgba(0,0,0,.12)}';

const shrineShadowOld =
  '.cell.tile-shrine{background:linear-gradient(155deg,#d68cff 0%,#ab47bc 100%);border-color:#7b1fa2;box-shadow:inset 0 1px 0 rgba(240,200,255,.45),0 0 5px rgba(171,71,188,.25)}';
const shrineShadowNew =
  '.cell.tile-shrine{background:linear-gradient(155deg,#d68cff 0%,#ab47bc 100%);border-color:#7b1fa2;box-shadow:inset 0 1px 0 rgba(240,200,255,.45),inset 0 -1px 3px rgba(0,0,0,.15)}';

const playerShadowOld =
  '.cell.player-pos{border-color:#00e5ff;box-shadow:0 0 8px rgba(0,229,255,.55),inset 0 0 0 1px rgba(255,255,255,.35)}';
const playerShadowNew =
  '.cell.player-pos{border-color:#00e5ff;box-shadow:inset 0 0 0 1px rgba(0,229,255,.55),inset 0 0 10px rgba(0,229,255,.25)}';

const innerOld =
  '.cell-inner{position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center}';
const innerNew =
  '.cell-inner{position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center;overflow:hidden}';

const pixelIconOld =
  '.cell .cell-pixel .pixel-icon{width:100%!important;height:100%!important;max-width:100%;max-height:100%;border:none;background:transparent;filter:drop-shadow(0 0 1px rgba(0,229,255,.25))}';
const pixelIconNew =
  '.cell .cell-pixel .pixel-icon{width:100%!important;height:100%!important;max-width:100%;max-height:100%;border:none;background:transparent;image-rendering:pixelated;image-rendering:crisp-edges;filter:none}';

const mobOld =
  '.cell .cell-mob{position:relative;z-index:2;display:flex;align-items:center;justify-content:center}';
const mobNew =
  '.cell .cell-mob{position:relative;z-index:2;display:flex;align-items:center;justify-content:center;overflow:hidden;max-width:92%;max-height:92%}.cell .cell-mob .pixel-icon,.cell .cell-mob .pixel-icon-wrap{max-width:100%;max-height:100%;overflow:hidden}';

const buildOld =
  "if(showMob&&cell.explored)parts.push('<span class=\"cell-mob\">',getMonsterPixelIconHtml(cell.enemy,20),'</span>');";
const buildNew =
  "if(showMob&&cell.explored)parts.push('<span class=\"cell-mob\">',pixelIconImgHtml(getMonsterPixelIconUrl(cell.enemy),20,' pixel-mob'),'</span>');";

for (const [label, old, neu] of [
  ['map', mapOld, mapNew],
  ['cell overflow', cellOld, cellNew],
  ['monster shadow', monsterShadowOld, monsterShadowNew],
  ['treasure shadow', treasureShadowOld, treasureShadowNew],
  ['shrine shadow', shrineShadowOld, shrineShadowNew],
  ['player shadow', playerShadowOld, playerShadowNew],
  ['cell-inner', innerOld, innerNew],
  ['pixel icon', pixelIconOld, pixelIconNew],
  ['cell-mob', mobOld, mobNew],
  ['buildMapCellHtml', buildOld, buildNew],
]) {
  if (!html.includes(old)) throw new Error(`missing anchor: ${label}`);
  html = html.replace(old, neu);
}

html = html.replace(/GAME_VERSION='2\.24\.52'/g, "GAME_VERSION='2.24.53'");
html = html.replace(
  '<meta name="game-version" content="2.24.52">',
  '<meta name="game-version" content="2.24.53">',
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.52'",
  "GAME_VERSION_HISTORY=[{version:'2.24.53',date:'2026-06-09',summary:{zh:'v2.24.53 地城語意配色；像素圖僅在格子內顯示不外溢。',en:'v2.24.53 semantic dungeon colors; pixel art clipped inside cells only.'}},{version:'2.24.52'",
);
html = html.replace(
  "logBalanceV22452:'[功能 v2.24.52]",
  "logBalanceV22453:'[功能 v2.24.53] 地城語意配色（怪物紅/空格與已走過白/寶箱金/聖壇紫）；像素圖僅在格子內渲染，格間不再顯示像素網格。',logBalanceV22452:'[功能 v2.24.52]",
);
html = html.replace(
  "logBalanceV22452:'[Feature v2.24.52]",
  "logBalanceV22453:'[Feature v2.24.53] Semantic dungeon colors; pixel tiles clipped inside cells, no pixel grid in gaps.',logBalanceV22452:'[Feature v2.24.52]",
);

fs.writeFileSync(path, html);
fs.writeFileSync(
  '/workspace/version.json',
  JSON.stringify({ version: '2.24.53', publishedAt: Date.now() }, null, 2) + '\n',
);
console.log('Patched index.html -> v2.24.53 dungeon cell clip + semantic colors');
