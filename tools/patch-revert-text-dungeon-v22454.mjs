import fs from 'fs';
import { execSync } from 'child_process';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');
const old248 = execSync('git show a20ddec:index.html', { encoding: 'utf8' });

function extractFn(src, name) {
  const i = src.indexOf(`function ${name}`);
  if (i < 0) return null;
  let depth = 0;
  for (let j = src.indexOf('{', i); j < src.length; j++) {
    if (src[j] === '{') depth++;
    else if (src[j] === '}') {
      depth--;
      if (!depth) return src.slice(i, j + 1);
    }
  }
  return null;
}

const pixelCssStart = html.indexOf('#map-container{background:linear-gradient(180deg,#010308');
const pixelCssEnd = html.indexOf(
  '.pixel-icon-wrap.rarity-boss{animation:bossAura 2.4s ease-in-out infinite}',
  pixelCssStart,
);
if (pixelCssStart < 0 || pixelCssEnd < 0) throw new Error('pixel dungeon css block missing');
html =
  html.slice(0, pixelCssStart) +
  html.slice(pixelCssEnd + '.pixel-icon-wrap.rarity-boss{animation:bossAura 2.4s ease-in-out infinite}'.length);

const dungeonJsStart = html.indexOf('function getDungeonTileKey(');
const dungeonJsEnd = html.indexOf('function getEquipPixelIconHtml(');
if (dungeonJsStart < 0 || dungeonJsEnd < 0) throw new Error('dungeon js block missing');
html = html.slice(0, dungeonJsStart) + html.slice(dungeonJsEnd);

const replacements = [
  [
    "function pixelIconImgHtml(url,size,cls,rarity){if(!url)return'';const px=size||22;const extra=cls?' '+cls:'';const img='<img class=\"pixel-icon'+extra+'\" src=\"'+url+'\" width=\"'+px+'\" height=\"'+px+'\" alt=\"\" draggable=\"false\">';if(rarity==='legendary'||rarity==='hidden'||rarity==='elite'||rarity==='boss'){const n=rarity==='boss'?5:4;let sparks='';for(let i=1;i<=n;i++)sparks+='<span class=\"pixel-spark p'+i+'\"></span>';return'<span class=\"pixel-icon-wrap rarity-'+rarity+'\" style=\"width:'+px+'px;height:'+px+'px\">'+img+sparks+'</span>';}return img;}",
    extractFn(old248, 'pixelIconImgHtml'),
  ],
  [
    extractFn(html, 'renderMapCell'),
    extractFn(old248, 'renderMapCell'),
  ],
  [
    extractFn(html, 'getCellClasses'),
    extractFn(old248, 'getCellClasses'),
  ],
  [
    'id="enemy-card"><div class="entity-portrait" id="enemy-portrait"></div><div class="entity-name" id="battle-enemy-name">',
    'id="enemy-card"><div class="entity-name" id="battle-enemy-name">',
  ],
  [
    "const statsKey=[getMainAtk(),getOffAtk(),player.def,player.spd,currentEnemy.atk,currentEnemy.def,currentEnemy.spd,currentEnemy.isBoss,currentEnemy.elite,currentEnemy.poolIndex].join('|');const portraitKey=getMonsterVisualKey(currentEnemy);if(full||statsKey!==battleUiCache.statsKey||portraitKey!==battleUiCache.portraitKey){battleUiCache.statsKey=statsKey;battleUiCache.portraitKey=portraitKey;document.getElementById('player-name').textContent='> '+(playerCustomName||'你');const enemyCard=document.getElementById('enemy-card');enemyCard.className='battle-entity '+(currentEnemy.isBoss?'boss-side':currentEnemy.elite?'elite-side':'enemy-side');const enemyPortrait=document.getElementById('enemy-portrait');if(enemyPortrait)enemyPortrait.innerHTML=getMonsterPixelIconHtml(currentEnemy,40);",
    "const statsKey=[getMainAtk(),getOffAtk(),player.def,player.spd,currentEnemy.atk,currentEnemy.def,currentEnemy.spd,currentEnemy.isBoss].join('|');if(full||statsKey!==battleUiCache.statsKey){battleUiCache.statsKey=statsKey;document.getElementById('player-name').textContent='> '+(playerCustomName||'你');const enemyCard=document.getElementById('enemy-card');enemyCard.className='battle-entity '+(currentEnemy.isBoss?'boss-side':'enemy-side');",
  ],
  ['isBoss:false,poolIndex:idx,', 'isBoss:false,'],
  ['isBoss:true,poolIndex:idx,', 'isBoss:true,'],
];

for (const [from, to] of replacements) {
  if (!from || !to) throw new Error('replacement pair missing');
  if (!html.includes(from)) throw new Error(`missing: ${from.slice(0, 80)}...`);
  html = html.replace(from, to);
}

html = html.replace(/GAME_VERSION='2\.24\.53'/g, "GAME_VERSION='2.24.54'");
html = html.replace(
  '<meta name="game-version" content="2.24.53">',
  '<meta name="game-version" content="2.24.54">',
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.53'",
  "GAME_VERSION_HISTORY=[{version:'2.24.54',date:'2026-06-09',summary:{zh:'v2.24.54 地城改回純文字顯示，移除像素化地圖。',en:'v2.24.54 revert dungeon to classic text map, remove pixel tiles.'}},{version:'2.24.53'",
);
html = html.replace(
  "logBalanceV22453:'[功能 v2.24.53]",
  "logBalanceV22454:'[功能 v2.24.54] 地城地圖改回純文字符號顯示（@、#、$ 等），移除像素圖塊與戰鬥怪物肖像。',logBalanceV22453:'[功能 v2.24.53]",
);
html = html.replace(
  "logBalanceV22453:'[Feature v2.24.53]",
  "logBalanceV22454:'[Feature v2.24.54] Dungeon map restored to classic text glyphs; pixel tiles and combat portraits removed.',logBalanceV22453:'[Feature v2.24.53]",
);

fs.writeFileSync(path, html);
fs.writeFileSync(
  '/workspace/version.json',
  JSON.stringify({ version: '2.24.54', publishedAt: Date.now() }, null, 2) + '\n',
);
console.log('Patched index.html -> v2.24.54 text dungeon');
