#!/usr/bin/env node
import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const PLAYER_PIXEL_BLOCK = `function getEquipDrawStyle(eq){if(!eq)return null;const color=resolvePixelColor((typeof RARITY_COLORS!=='undefined'&&RARITY_COLORS[eq.rarity])||'#fff');const main=hexToRgb(color);const mainRgba=[main.r,main.g,main.b,255];const hi=hexToRgb(shadeColor(color,0.32));const lo=hexToRgb(shadeColor(color,-0.38));const disp=typeof getEquipDisplayName==='function'?getEquipDisplayName(eq.name):eq.name;const themes=parseNameThemes(eq.name,disp);const kind=parseWeaponKind(eq.name,disp);const accent=themes.void?[130,50,170,255]:themes.fire?[255,110,50,255]:themes.ice?[120,200,255,255]:themes.energy?[70,220,255,255]:themes.shadow?[70,70,100,255]:[hi.r,hi.g,hi.b,255];return{mainRgba,hi,lo,themes,kind,rarity:eq.rarity,seed:hashStr((eq.name||'')+'|'+(eq.type||'')+'|'+eq.rarity),accent};}function drawPlayerBasePixels(grid){const bg=[8,8,16,255],skin=[255,214,190,255],skinLo=[235,180,155,255],hair=[248,248,255,255],hairHi=[255,255,255,255],hairLo=[205,205,220,255],eye=[0,220,255,255],lip=[255,150,170,255],suit=[30,32,44,255];fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,bg);fillGridRect(grid,3,0,10,3,hairHi);fillGridRect(grid,4,2,8,3,hair);fillGridRect(grid,2,3,2,9,hair);fillGridRect(grid,12,3,2,10,hair);setGridPx(grid,3,4,hairLo);setGridPx(grid,12,5,hairLo);fillGridRect(grid,3,11,2,3,hair);fillGridRect(grid,11,12,2,3,hair);fillGridRect(grid,6,4,4,4,skin);setGridPx(grid,6,5,skinLo);setGridPx(grid,9,5,skinLo);setGridPx(grid,6,6,eye);setGridPx(grid,9,6,eye);setGridPx(grid,7,7,lip);fillGridRect(grid,7,8,2,1,skin);fillGridRect(grid,5,9,6,4,suit);fillGridRect(grid,6,13,2,3,suit);setGridPx(grid,5,14,skinLo);setGridPx(grid,10,14,skinLo);}function overlayPlayerArmor(grid,st){const m=st.mainRgba,hi=[st.hi.r,st.hi.g,st.hi.b,255],lo=[st.lo.r,st.lo.g,st.lo.b,255];fillGridRect(grid,5,9,6,4,m);fillGridRect(grid,6,10,4,2,hi);if(st.themes.heavy){fillGridRect(grid,4,10,1,3,lo);fillGridRect(grid,11,10,1,3,lo);}setGridPx(grid,7,9,st.accent);}function overlayPlayerArmguard(grid,st){const m=st.mainRgba,hi=[st.hi.r,st.hi.g,st.hi.b,255],lo=[st.lo.r,st.lo.g,st.lo.b,255];fillGridRect(grid,3,10,2,3,m);fillGridRect(grid,11,10,2,3,m);setGridPx(grid,3,9,hi);setGridPx(grid,12,9,hi);setGridPx(grid,4,12,lo);setGridPx(grid,11,12,lo);}function overlayPlayerLegguard(grid,st){const m=st.mainRgba,hi=[st.hi.r,st.hi.g,st.hi.b,255],lo=[st.lo.r,st.lo.g,st.lo.b,255];fillGridRect(grid,5,13,2,3,m);fillGridRect(grid,9,13,2,3,m);setGridPx(grid,5,12,hi);setGridPx(grid,10,12,hi);setGridPx(grid,5,15,lo);setGridPx(grid,10,15,lo);}function overlayPlayerBoots(grid,st){const m=st.mainRgba,lo=[st.lo.r,st.lo.g,st.lo.b,255];fillGridRect(grid,4,14,3,2,m);fillGridRect(grid,9,14,3,2,m);setGridPx(grid,3,15,lo);setGridPx(grid,12,15,lo);if(st.themes.swift){setGridPx(grid,2,15,st.accent);setGridPx(grid,13,15,st.accent);}}function overlayPlayerMainhand(grid,st){const m=st.mainRgba,hi=[st.hi.r,st.hi.g,st.hi.b,255],lo=[st.lo.r,st.lo.g,st.lo.b,255],k=st.kind;if(k==='gun'){fillGridRect(grid,11,8,4,2,m);fillGridRect(grid,12,7,2,1,hi);setGridPx(grid,14,8,st.accent);}else if(k==='hammer'){fillGridRect(grid,11,6,3,3,m);fillGridRect(grid,12,9,2,5,lo);}else if(k==='scythe'){for(let i=0;i<5;i++){setGridPx(grid,13-i,4+i,m);setGridPx(grid,14-i,4+i,hi);}setGridPx(grid,12,10,lo);}else if(k==='dagger'){fillGridRect(grid,12,6,2,5,m);setGridPx(grid,13,5,hi);setGridPx(grid,12,11,lo);}else{for(let y=5;y<12;y++){setGridPx(grid,12,y,m);setGridPx(grid,13,y,hi);}fillGridRect(grid,12,12,2,3,lo);setGridPx(grid,12,4,hi);}}function overlayPlayerOffhand(grid,st){const m=st.mainRgba,hi=[st.hi.r,st.hi.g,st.hi.b,255],lo=[st.lo.r,st.lo.g,st.lo.b,255],k=st.kind;if(k==='shield'){fillGridRect(grid,1,7,4,5,m);fillGridRect(grid,2,8,2,3,hi);setGridPx(grid,2,12,lo);}else if(k==='gun'){fillGridRect(grid,0,9,4,2,m);setGridPx(grid,3,8,hi);}else if(k==='fist'){fillGridRect(grid,1,9,3,3,m);setGridPx(grid,1,12,lo);}else{fillGridRect(grid,2,7,2,5,m);fillGridRect(grid,2,12,2,2,lo);setGridPx(grid,2,6,hi);}}function overlayPlayerEquip(grid,eq){if(!eq)return;const st=getEquipDrawStyle(eq);const slot=eq.type||'armor';if(slot==='armor')overlayPlayerArmor(grid,st);else if(slot==='armguard')overlayPlayerArmguard(grid,st);else if(slot==='legguard')overlayPlayerLegguard(grid,st);else if(slot==='boots')overlayPlayerBoots(grid,st);else if(slot==='mainhand')overlayPlayerMainhand(grid,st);else if(slot==='offhand')overlayPlayerOffhand(grid,st);if(st.rarity==='legendary'||st.rarity==='hidden'){const spark=st.rarity==='legendary'?[255,180,220,255]:[230,80,80,255];setGridPx(grid,(st.seed%2)?1:14,(st.seed%4)+1,spark);}}function drawPlayerCombatPixels(grid){drawPlayerBasePixels(grid);if(typeof player==='undefined'||!player||!player.equipment)return;['armor','armguard','legguard','boots','mainhand','offhand'].forEach(s=>{const eq=player.equipment[s];if(eq)overlayPlayerEquip(grid,eq);});}function getPlayerCombatVisualKey(){if(typeof player==='undefined'||!player||!player.equipment)return'player|v1|empty';let k='player|v1|';['armor','armguard','legguard','boots','mainhand','offhand'].forEach(s=>{const eq=player.equipment[s];if(eq)k+=s+':'+(eq.name||'')+'|'+eq.rarity+'|'+(eq.upgradeLv||0)+';';});return k;}function getPlayerCombatPortraitUrl(){return getCachedPixelIcon(getPlayerCombatVisualKey(),drawPlayerCombatPixels);}function getPlayerPortraitSparkRarity(){if(typeof player==='undefined'||!player||!player.equipment)return'';const rank={hidden:5,legendary:4};let best='',bestR=0;['mainhand','offhand','armor','armguard','legguard','boots'].forEach(s=>{const eq=player.equipment[s];if(eq){const r=rank[eq.rarity]||0;if(r>bestR){bestR=r;best=eq.rarity;}}});return best==='legendary'||best==='hidden'?best:'';}function getPlayerCombatPortraitHtml(size){const px=size||getMonsterCombatPortraitSize(currentEnemy);const rarity=getPlayerPortraitSparkRarity();return pixelIconImgHtml(getPlayerCombatPortraitUrl(),px,' pixel-player',rarity||'');}function syncCombatPortraitStage(portraitId,px){const wrap=document.getElementById(portraitId);if(!wrap||!(px>0))return 0;wrap.style.width=px+'px';wrap.style.height=px+'px';wrap.style.minHeight=px+'px';wrap.style.maxWidth=px+'px';wrap.style.marginLeft='auto';wrap.style.marginRight='auto';return px;}`;

if (!html.includes('function drawPlayerCombatPixels')) {
  const anchor = 'function getMonsterVisualKey(enemy)';
  if (!html.includes(anchor)) throw new Error('getMonsterVisualKey anchor not found');
  html = html.replace(anchor, PLAYER_PIXEL_BLOCK + anchor);
}

html = html.replace(
  /function syncEnemyPortraitStage\(enemy,cardEl\)\{[^}]+\}[^}]+[^}]+[^}]+return px;\}/,
  'function syncEnemyPortraitStage(enemy,cardEl){const card=cardEl||document.getElementById(\'enemy-card\');const px=getMonsterCombatPortraitSize(enemy,card);return syncCombatPortraitStage(\'enemy-portrait\',px);}'
);

html = html.replace(
  'id="player-card"><div class="entity-name" id="player-name"',
  'id="player-card"><div class="entity-portrait" id="player-portrait"></div><div class="entity-name" id="player-name"'
);

const playerPortraitCss =
  '#player-portrait.entity-portrait{width:auto;min-width:0;min-height:0;margin:.1rem auto .32rem;padding:0;box-sizing:border-box;flex:0 0 auto;display:flex;align-items:center;justify-content:center;align-self:center;overflow:visible}#player-portrait .pixel-icon-wrap,#player-portrait .pixel-icon{width:auto!important;height:auto!important;max-width:none!important;max-height:none!important}';

if (!html.includes('#player-portrait.entity-portrait')) {
  html = html.replace(
    '#enemy-portrait .pixel-icon-wrap,#enemy-portrait .pixel-icon{width:auto!important;height:auto!important;max-width:none!important;max-height:none!important}',
    '#enemy-portrait .pixel-icon-wrap,#enemy-portrait .pixel-icon{width:auto!important;height:auto!important;max-width:none!important;max-height:none!important}' + playerPortraitCss
  );
  html = html.replace(
    '#enemy-portrait .pixel-icon-wrap,#enemy-portrait .pixel-icon{display:block;margin:0 auto}',
    '#enemy-portrait .pixel-icon-wrap,#enemy-portrait .pixel-icon{display:block;margin:0 auto}#player-portrait .pixel-icon-wrap,#player-portrait .pixel-icon{display:block;margin:0 auto}'
  );
}

const oldStatsKey =
  "const statsKey=[getMainAtk(),getOffAtk(),player.def,player.spd,player.critChance,player.critDmg,player.dodge,player.lifesteal,player.thorns,player.allDmg,player.allDmgReduction,player.maxShield,!!player.equipment.offhand,player.level,currentEnemy.atk,currentEnemy.def,currentEnemy.spd,currentEnemy.dodge,currentEnemy.resist,currentEnemy.isBoss,currentEnemy.elite,currentEnemy.poolIndex].join('|');";

const newStatsKey =
  "const equipPortraitKey=['armor','armguard','legguard','boots','mainhand','offhand'].map(s=>{const e=player.equipment[s];return e?(e.name+'+'+(e.upgradeLv||0)+'|'+e.rarity):'';}).join(';');const statsKey=[getMainAtk(),getOffAtk(),player.def,player.spd,player.critChance,player.critDmg,player.dodge,player.lifesteal,player.thorns,player.allDmg,player.allDmgReduction,player.maxShield,!!player.equipment.offhand,player.level,equipPortraitKey,currentEnemy.atk,currentEnemy.def,currentEnemy.spd,currentEnemy.dodge,currentEnemy.resist,currentEnemy.isBoss,currentEnemy.elite,currentEnemy.poolIndex].join('|');";

if (!html.includes('equipPortraitKey')) {
  if (!html.includes(oldStatsKey)) throw new Error('statsKey block not found');
  html = html.replace(oldStatsKey, newStatsKey);
}

const oldPortraitBlock =
  "const enemyCard=document.getElementById('enemy-card');enemyCard.className='battle-entity '+(currentEnemy.isBoss?'boss-side':currentEnemy.elite?'elite-side':'enemy-side');const enemyPortrait=document.getElementById('enemy-portrait');if(enemyPortrait)enemyPortrait.innerHTML=getMonsterPixelIconHtml(currentEnemy,getMonsterCombatPortraitSize(currentEnemy));";

const newPortraitBlock =
  "const enemyCard=document.getElementById('enemy-card');enemyCard.className='battle-entity '+(currentEnemy.isBoss?'boss-side':currentEnemy.elite?'elite-side':'enemy-side');const portraitPx=getMonsterCombatPortraitSize(currentEnemy,enemyCard);syncCombatPortraitStage('player-portrait',portraitPx);syncCombatPortraitStage('enemy-portrait',portraitPx);const playerPortrait=document.getElementById('player-portrait');if(playerPortrait)playerPortrait.innerHTML=getPlayerCombatPortraitHtml(portraitPx);const enemyPortrait=document.getElementById('enemy-portrait');if(enemyPortrait)enemyPortrait.innerHTML=getMonsterPixelIconHtml(currentEnemy,portraitPx);";

if (!html.includes("getPlayerCombatPortraitHtml(portraitPx)")) {
  if (!html.includes(oldPortraitBlock)) throw new Error('portrait block not found');
  html = html.replace(oldPortraitBlock, newPortraitBlock);
}

html = html.replace(/GAME_VERSION='2\.24\.59'/g, "GAME_VERSION='2.24.61'");
html = html.replace(/content="2\.24\.59"/g, 'content="2.24.61"');
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.60'",
  "GAME_VERSION_HISTORY=[{version:'2.24.61',date:'2026-06-09',summary:{zh:'v2.24.61 戰鬥新增玩家像素肖像（白長髮女角＋身上裝備）；螢光像素條與肖像最大尺寸貼合。',en:'v2.24.61 player combat pixel portrait with equipped gear; fluoro bars and max-fit portraits.'}},{version:'2.24.60'"
);
html = html.replace(
  "logBalanceV22460:'[功能 v2.24.60] 生命／經驗／護盾像素條改螢光紅、螢光藍、螢光白；怪物肖像依敵方卡片寬度貼合最大尺寸顯示。'",
  "logBalanceV22461:'[功能 v2.24.61] 戰鬥雙方皆顯示像素肖像；玩家為白長髮女角並依身上裝備生成像素外觀，尺寸與怪物相同。',logBalanceV22460:'[功能 v2.24.60] 生命／經驗／護盾像素條改螢光紅、螢光藍、螢光白；怪物肖像依敵方卡片寬度貼合最大尺寸顯示。'"
);

fs.writeFileSync(path, html);
fs.writeFileSync('/workspace/version.json', JSON.stringify({ version: '2.24.61', updated: '2026-06-09' }, null, 2) + '\n');
console.log('Patched index.html and version.json to v2.24.61');
