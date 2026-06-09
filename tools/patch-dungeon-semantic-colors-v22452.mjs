import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const keyOld =
  "function getDungeonTileKey(cell,r,c){if(!cell)return'floor';if(r===playerPos.r&&c===playerPos.c)return'floor';if(isDefeatedMonsterCell(cell))return'floor';if(!cell.explored)return cell.type==='treasure'?'fog-treasure':'fog';if(cell.enemy&&cell.enemy.hp>0&&cell.type==='boss')return'boss-floor';if(cell.enemy&&cell.enemy.hp>0&&cell.enemy.elite)return'elite-floor';switch(cell.type){case'start':return'start';case'exit':return'exit';case'treasure':return'treasure';case'shrine':return cell.explored?'shrine':'fog-event';case'trap':return cell.explored?'trap':'fog-event';case'cache':return cell.explored?'cache':'fog-event';case'monster':return'floor';default:return'floor';}}";

const keyNew =
  "function getDungeonTileKey(cell,r,c){if(!cell)return'visited';if(r===playerPos.r&&c===playerPos.c)return'visited';if(isDefeatedMonsterCell(cell))return'visited';const live=!!(cell.enemy&&cell.enemy.hp>0);if(live&&(cell.type==='monster'||cell.type==='boss'))return'monster';if(!cell.explored){if(cell.type==='treasure')return'fog-treasure';if(cell.type==='shrine')return'shrine';return'empty';}switch(cell.type){case'treasure':return'treasure';case'shrine':return'shrine';default:return'visited';}}";

const drawOld = fs.readFileSync('/workspace/index.html', 'utf8').match(
  /function drawDungeonTilePixels\(grid,key,tier\)\{[\s\S]*?\}(?=function getDungeonTileIconUrl)/,
)?.[0];
if (!drawOld) throw new Error('drawDungeonTilePixels block missing');

const drawNew = `function drawDungeonTilePixels(grid,key,tier){const edge=(c)=>{fillGridRect(grid,0,0,16,1,c);fillGridRect(grid,0,15,16,1,c);fillGridRect(grid,0,0,1,16,c);fillGridRect(grid,15,0,1,16,c);};const speckle=(base,hi,n)=>{for(let i=0;i<n;i++)setGridPx(grid,2+(i*3)%13,2+(i*5)%13,hi);setGridPx(grid,8,8,base);};if(key==='monster'){fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,[220,50,50,255]);edge([150,30,30,255]);speckle([255,90,90,255],[180,40,40,255],10);setGridPx(grid,6,7,[255,220,200,255]);setGridPx(grid,9,7,[255,220,200,255]);return;}if(key==='empty'){fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,[232,235,242,255]);edge([200,205,214,255]);speckle([248,250,255,255],[210,215,224,255],8);return;}if(key==='visited'){fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,[252,253,255,255]);edge([218,222,230,255]);speckle([255,255,255,255],[235,238,244,255],6);return;}if(key==='treasure'||key==='fog-treasure'){fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,[255,204,60,255]);edge([200,140,0,255]);speckle([255,230,120,255],[220,160,20,255],8);setGridPx(grid,7,6,[255,248,200,255]);setGridPx(grid,8,9,[255,248,200,255]);return;}if(key==='shrine'){fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,[186,104,255,255]);edge([120,40,190,255]);speckle([220,160,255,255],[150,60,210,255],8);setGridPx(grid,8,7,[255,240,255,255]);return;}fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,[252,253,255,255]);edge([218,222,230,255]);}`;

const renderOld =
  'function renderMapCell(r,c){if(!mapCellEls||!mapCellEls[r]||!mapCellEls[r][c]||!mapData[r])return;const cell=mapData[r][c];const div=mapCellEls[r][c];const tileKey=getDungeonTileKey(cell,r,c);let extra="";if(tileKey==="start")extra=" tile-start";else if(tileKey==="exit")extra=" tile-exit";else if(tileKey==="treasure"||tileKey==="fog-treasure")extra=" tile-treasure";else if(tileKey==="shrine"||tileKey==="trap"||tileKey==="cache"||tileKey==="fog-event")extra=" tile-event";else if(tileKey==="boss-floor")extra=" tile-boss";else if(tileKey==="elite-floor")extra=" tile-elite";div.className=`cell ${getCellClasses(cell,r,c)}${extra}`;const html=buildMapCellHtml(cell,r,c);if(div.innerHTML!==html)div.innerHTML=html;}';

const renderNew =
  'function renderMapCell(r,c){if(!mapCellEls||!mapCellEls[r]||!mapCellEls[r][c]||!mapData[r])return;const cell=mapData[r][c];const div=mapCellEls[r][c];const tileKey=getDungeonTileKey(cell,r,c);let extra="";if(tileKey==="monster")extra=" tile-monster";else if(tileKey==="empty")extra=" tile-empty";else if(tileKey==="visited")extra=" tile-visited";else if(tileKey==="treasure"||tileKey==="fog-treasure")extra=" tile-treasure";else if(tileKey==="shrine")extra=" tile-shrine";div.className=`cell ${getCellClasses(cell,r,c)}${extra}`;const html=buildMapCellHtml(cell,r,c);if(div.innerHTML!==html)div.innerHTML=html;}';

const cssOld =
  '.cell{position:relative;overflow:visible;background:linear-gradient(155deg,#172338 0%,#101a2c 55%,#0c1422 100%);border:1px solid #4a7098;box-shadow:0 0 0 1px rgba(0,229,255,.08),inset 0 1px 0 rgba(150,210,255,.14),inset 0 -2px 5px rgba(0,0,0,.35)}.cell.visited{border-color:#6a9cc8;box-shadow:0 0 0 1px rgba(0,229,255,.12),inset 0 1px 0 rgba(170,225,255,.18),inset 0 -2px 5px rgba(0,0,0,.28)}.cell.unexplored{background:linear-gradient(155deg,#0d131f 0%,#090e18 100%);border-color:#2f4560;box-shadow:inset 0 0 0 1px rgba(0,229,255,.04),inset 0 2px 6px rgba(0,0,0,.45)}.cell.player-pos{border-color:#fff;box-shadow:0 0 8px rgba(0,229,255,.45),inset 0 0 0 1px rgba(255,255,255,.2)}.cell.tile-start{border-color:rgba(90,255,120,.55)}.cell.tile-exit{border-color:rgba(0,229,255,.65)}.cell.tile-treasure{border-color:rgba(255,210,60,.55)}.cell.tile-event{border-color:rgba(150,185,255,.55)}.cell.tile-boss{border-color:rgba(210,240,255,.45)}.cell.tile-elite{border-color:rgba(210,140,255,.55)}';

const cssNew =
  '.cell{position:relative;overflow:visible;background:linear-gradient(155deg,#eef0f4 0%,#e4e7ee 100%);border:1px solid #cdd2dc;box-shadow:inset 0 1px 0 rgba(255,255,255,.55),inset 0 -1px 3px rgba(0,0,0,.08)}.cell.tile-empty,.cell.unexplored:not(.tile-monster):not(.tile-treasure):not(.tile-shrine){background:linear-gradient(155deg,#eceff4 0%,#dfe3eb 100%);border-color:#c5cad4}.cell.tile-visited,.cell.visited{background:linear-gradient(155deg,#fcfdff 0%,#f4f6fa 100%);border-color:#d5dae3;box-shadow:inset 0 1px 0 rgba(255,255,255,.8),inset 0 -1px 2px rgba(0,0,0,.06)}.cell.tile-monster,.cell.unexplored-monster{background:linear-gradient(155deg,#f05252 0%,#dc2626 100%);border-color:#b91c1c;box-shadow:inset 0 1px 0 rgba(255,180,180,.35),0 0 6px rgba(220,38,38,.25)}.cell.tile-treasure,.cell.unexplored-treasure{background:linear-gradient(155deg,#ffd54f 0%,#ffb300 100%);border-color:#c49000;box-shadow:inset 0 1px 0 rgba(255,240,180,.5),0 0 5px rgba(255,179,0,.2)}.cell.tile-shrine{background:linear-gradient(155deg,#d68cff 0%,#ab47bc 100%);border-color:#7b1fa2;box-shadow:inset 0 1px 0 rgba(240,200,255,.45),0 0 5px rgba(171,71,188,.25)}.cell.player-pos{border-color:#00e5ff;box-shadow:0 0 8px rgba(0,229,255,.55),inset 0 0 0 1px rgba(255,255,255,.35)}';

const glyphOld =
  '.cell .cell-glyph{position:relative;z-index:3;font-size:.62rem;line-height:1;text-shadow:0 0 5px rgba(0,229,255,.55)}.cell.unexplored .cell-pixel{opacity:.58;filter:saturate(.5) brightness(.88)}.cell.unexplored .cell-mob{opacity:0}.cell.unexplored-monster .cell-glyph,.cell.unexplored-boss .cell-glyph{color:#f46}';

const glyphNew =
  '.cell .cell-glyph{position:relative;z-index:3;font-size:.62rem;line-height:1}.cell.tile-empty .cell-glyph,.cell.tile-visited .cell-glyph,.cell.visited .cell-glyph{color:#334155;text-shadow:none}.cell.tile-monster .cell-glyph,.cell.unexplored-monster .cell-glyph,.cell.unexplored-boss .cell-glyph{color:#fff;text-shadow:0 0 4px rgba(0,0,0,.35)}.cell.tile-treasure .cell-glyph,.cell.unexplored-treasure .cell-glyph{color:#5c3d00;text-shadow:none}.cell.tile-shrine .cell-glyph{color:#fff;text-shadow:0 0 4px rgba(80,0,120,.4)}.cell .cell-glyph.cell-player{color:#00e5ff;text-shadow:0 0 5px rgba(0,229,255,.65)}.cell.unexplored.tile-empty .cell-pixel{opacity:.82;filter:none}.cell.unexplored:not(.tile-empty) .cell-pixel{opacity:1;filter:none}.cell.unexplored .cell-mob{opacity:0}';

if (!html.includes(keyOld)) throw new Error('getDungeonTileKey missing');
if (!html.includes(drawOld)) throw new Error('drawDungeonTilePixels missing');
if (!html.includes(renderOld)) throw new Error('renderMapCell missing');
if (!html.includes(cssOld)) throw new Error('cell css missing');
if (!html.includes(glyphOld)) throw new Error('glyph css missing');

html = html.replace(keyOld, keyNew);
html = html.replace(drawOld, drawNew);
html = html.replace(renderOld, renderNew);
html = html.replace(cssOld, cssNew);
html = html.replace(glyphOld, glyphNew);

html = html.replace(/GAME_VERSION='2\.24\.51'/g, "GAME_VERSION='2.24.52'");
html = html.replace(
  '<meta name="game-version" content="2.24.51">',
  '<meta name="game-version" content="2.24.52">',
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.51'",
  "GAME_VERSION_HISTORY=[{version:'2.24.52',date:'2026-06-09',summary:{zh:'v2.24.52 地城語意配色：怪物紅、空格/已走過白、寶箱金、聖壇紫。',en:'v2.24.52 semantic dungeon colors: monster red, empty/visited white, treasure gold, shrine purple.'}},{version:'2.24.51'",
);
html = html.replace(
  "logBalanceV22451:'[功能 v2.24.51]",
  "logBalanceV22452:'[功能 v2.24.52] 地城格子改為語意配色：怪物紅色、空格與已走過白色、寶箱金色、聖壇紫色。',logBalanceV22451:'[功能 v2.24.51]",
);
html = html.replace(
  "logBalanceV22451:'[Feature v2.24.51]",
  "logBalanceV22452:'[Feature v2.24.52] Semantic dungeon tiles: monsters red, empty/visited white, treasure gold, shrine purple.',logBalanceV22451:'[Feature v2.24.51]",
);

fs.writeFileSync(path, html);
fs.writeFileSync(
  '/workspace/version.json',
  JSON.stringify({ version: '2.24.52', publishedAt: Date.now() }, null, 2) + '\n',
);
console.log('Patched index.html -> v2.24.52 dungeon semantic colors');
