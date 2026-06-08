#!/usr/bin/env python3
"""v2.17.7: Dungeon performance — incremental map, combat UI cache, defer sync."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")


def rep(old, new, label, count=1):
    global text
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:240]}")
    text = text.replace(old, new, 1)


# version
rep("GAME_VERSION='2.17.6'", "GAME_VERSION='2.17.7'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.6',date:'2026-06-08',summary:{zh:'v2.17.6 修復等級歸零與跨裝置登入：防雲端覆寫、啟動拉取進度、強化合併與上傳保護。',en:'v2.17.6 fix level rollback and cross-device login: anti-wipe upload, boot cloud pull, merge guards.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.7',date:'2026-06-08',summary:{zh:'v2.17.7 地下城效能優化：地圖增量渲染、戰鬥 UI 快取、地城內延後雲端同步與存檔。',en:'v2.17.7 dungeon perf: incremental map, battle UI cache, deferred cloud sync/save in dungeon.'}},{version:'2.17.6',date:'2026-06-08',summary:{zh:'v2.17.6 修復等級歸零與跨裝置登入：防雲端覆寫、啟動拉取進度、強化合併與上傳保護。',en:'v2.17.6 fix level rollback and cross-device login: anti-wipe upload, boot cloud pull, merge guards.'}},",
    "hist",
)
rep("SAVE_VERSION=52", "SAVE_VERSION=53", "save")

rep(
    'logBalanceV2176:"[修復 v2.17.6] 修復等級異常歸 1 與跨裝置無法讀取進度；雲端同步不再覆寫較高進度。",logBalanceV2175:',
    'logBalanceV2177:"[優化 v2.17.7] 地下城卡頓優化：地圖增量更新、戰鬥介面快取、地城內延後雲端同步。",logBalanceV2176:"[修復 v2.17.6] 修復等級異常歸 1 與跨裝置無法讀取進度；雲端同步不再覆寫較高進度。",logBalanceV2175:',
    "i18n zh log",
)

rep(
    'logBalanceV2176:"[Fix v2.17.6] Level rollback and cross-device progress restore; cloud sync no longer overwrites higher saves.",logBalanceV2175:',
    'logBalanceV2177:"[Optimize v2.17.7] Dungeon lag fixes: incremental map, battle UI cache, deferred cloud sync in dungeon.",logBalanceV2176:"[Fix v2.17.6] Level rollback and cross-device progress restore; cloud sync no longer overwrites higher saves.",logBalanceV2175:',
    "i18n en log",
)

rep(
    "if(_balanceV2176Notice)logInfo(t('logBalanceV2176'));logInfo(t('logBalanceV2175'));logInfo(t('logBalanceV2174'));logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'));leaderboardTrackedLevel=-1;",
    "if(_balanceV2176Notice)logInfo(t('logBalanceV2176'));if(_balanceV2177Notice)logInfo(t('logBalanceV2177'));logInfo(t('logBalanceV2175'));logInfo(t('logBalanceV2174'));logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'));leaderboardTrackedLevel=-1;",
    "load log",
)

rep(
    "function migrateSave(data){if(data.version<52){",
    "function migrateSave(data){if(data.version<53){data._balanceV2177Notice=true;data.version=53;}if(data.version<52){",
    "migrate",
)
rep(
    "const _balanceV2176Notice=!!data._balanceV2176Notice;delete data._balanceV2176Notice;if(data.autoHerbSettings)",
    "const _balanceV2176Notice=!!data._balanceV2176Notice;delete data._balanceV2176Notice;const _balanceV2177Notice=!!data._balanceV2177Notice;delete data._balanceV2177Notice;if(data.autoHerbSettings)",
    "load notice var",
)

# throttle save: slower in dungeon/combat
rep(
    "function throttleSave(){if(saveTimeout)clearTimeout(saveTimeout);saveTimeout=setTimeout(()=>{saveGame();saveTimeout=null;},1000);}",
    "function throttleSave(){if(saveTimeout)clearTimeout(saveTimeout);const delay=inCombat?2500:(inDungeon?1800:1000);saveTimeout=setTimeout(()=>{saveGame();saveTimeout=null;},delay);}",
    "throttle save",
)

# log scroll batch
rep(
    "function log(msg,cls=''){const div=document.createElement('div');div.className='log-line'+(cls?' '+cls:'');div.innerHTML=msg;logEl.appendChild(div);while(logEl.children.length>MAX_LOG_LINES){logEl.removeChild(logEl.firstChild);}logEl.scrollTop=logEl.scrollHeight;}",
    "let logScrollRaf=0;function log(msg,cls=''){const div=document.createElement('div');div.className='log-line'+(cls?' '+cls:'');div.innerHTML=msg;logEl.appendChild(div);while(logEl.children.length>MAX_LOG_LINES){logEl.removeChild(logEl.firstChild);}if(!logScrollRaf){logScrollRaf=requestAnimationFrame(()=>{logScrollRaf=0;logEl.scrollTop=logEl.scrollHeight;});}}",
    "log raf",
)

# leaderboard: skip during dungeon/combat
rep(
    "function syncLeaderboardLevelIfChanged(){if(!getSessionKey()||!player||player.isPermanentlyDead)return;const lv=Math.max(1,Math.floor(Number(player.level)||1));if(lv===leaderboardTrackedLevel)return;leaderboardTrackedLevel=lv;publishLeaderboardEntry(true);}",
    "function syncLeaderboardLevelIfChanged(){if(inCombat||inDungeon)return;if(!getSessionKey()||!player||player.isPermanentlyDead)return;const lv=Math.max(1,Math.floor(Number(player.level)||1));if(lv===leaderboardTrackedLevel)return;leaderboardTrackedLevel=lv;publishLeaderboardEntry(true);}",
    "leaderboard skip",
)

rep(
    "}else{btnAtkMain.style.color='#666';btnAtkMain.style.borderColor='#333';btnAtkOff.style.color='#666';btnAtkOff.style.borderColor='#333';}syncLeaderboardLevelIfChanged();}function updateButtons()",
    "}else{btnAtkMain.style.color='#666';btnAtkMain.style.borderColor='#333';btnAtkOff.style.color='#666';btnAtkOff.style.borderColor='#333';}}function updateButtons()",
    "atk btn leaderboard",
)

# cloud sync: defer during dungeon/combat
rep(
    "function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession()){stopCloudAutoSync();return;}",
    "function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy||inCombat||inDungeon)return;if(!hasActiveCloudSession()){stopCloudAutoSync();return;}",
    "cloud sync skip",
)

# useHerb: skip full panel rebuild in combat
rep(
    "if(inCombat)updateBattleUI();updateStatusBar();renderAllPanels();throttleSave();return true;}function getH",
    "if(inCombat){updateBattleUI();updateStatusBar();renderInventoryPanel();}else{updateBattleUI();updateStatusBar();renderAllPanels();}throttleSave();return true;}function getH",
    "herb panels",
)

# dungeon banner cache
rep(
    "let mapCellEls=null;function invalidateMapCells(){mapCellEls=null;if(mapEl)mapEl.innerHTML='';}function renderMap(){if(!currentDungeon)return;if(!mapCellEls){mapEl.innerHTML='';mapCellEls=[];for(let r=0;r<7;r++){mapCellEls[r]=[];for(let c=0;c<7;c++){const div=document.createElement('div');div.dataset.r=r;div.dataset.c=c;mapEl.appendChild(div);mapCellEls[r][c]=div;}}}for(let r=0;r<7;r++){for(let c=0;c<7;c++){const cell=mapData[r][c];const div=mapCellEls[r][c];div.className=`cell ${getCellClasses(cell,r,c)}`;div.textContent=getCellChar(cell,r,c);}}updateDungeonRunBanner();}",
    "let mapCellEls=null,dungeonBannerSig='';function invalidateMapCells(){mapCellEls=null;if(mapEl)mapEl.innerHTML='';}function renderMapCell(r,c){if(!mapCellEls||!mapCellEls[r]||!mapCellEls[r][c]||!mapData[r])return;const cell=mapData[r][c];const div=mapCellEls[r][c];div.className=`cell ${getCellClasses(cell,r,c)}`;div.textContent=getCellChar(cell,r,c);}function renderMap(opts){if(!currentDungeon)return;if(!mapCellEls){mapEl.innerHTML='';mapCellEls=[];for(let r=0;r<7;r++){mapCellEls[r]=[];for(let c=0;c<7;c++){const div=document.createElement('div');div.dataset.r=r;div.dataset.c=c;mapEl.appendChild(div);mapCellEls[r][c]=div;}}}const cells=opts&&opts.cells;if(cells&&cells.length){for(const p of cells)renderMapCell(p.r,p.c);return;}for(let r=0;r<7;r++){for(let c=0;c<7;c++)renderMapCell(r,c);}updateDungeonRunBanner();}",
    "map incremental",
)

rep(
    "function updateDungeonRunBanner(){const header=document.getElementById('dungeon-run-header');const el=document.getElementById('dungeon-run-banner');if(!header||!el)return;if(!inDungeon||!currentDungeon){header.innerHTML='<div id=\"dungeon-run-banner\"></div>';return;}",
    "function updateDungeonRunBanner(){const header=document.getElementById('dungeon-run-header');if(!header)return;if(!inDungeon||!currentDungeon){dungeonBannerSig='';header.innerHTML='<div id=\"dungeon-run-banner\"></div>';return;}const sig=(currentDungeon.tierLevel||0)+'|'+(currentDungeon.tier||'')+'|'+(currentDungeon.layout||'')+'|'+((currentDungeon.modifiers||[]).map(m=>m.labelKey).join(','));if(sig===dungeonBannerSig&&header.querySelector('#dungeon-run-banner'))return;dungeonBannerSig=sig;",
    "banner cache",
)

# moveTo: incremental map cells
rep(
    "}playerPos={r,c};cell.explored=true;if((cell.type==='monster'||cell.type==='boss')&&cell.enemy){",
    "}const prevPos={r:playerPos.r,c:playerPos.c};playerPos={r,c};cell.explored=true;const mapDirty=[{r:prevPos.r,c:prevPos.c},{r,c}];if((cell.type==='monster'||cell.type==='boss')&&cell.enemy){",
    "move prev pos",
)
rep(
    "}else if(cell.type==='shrine'){handleShrineCell();mapData[r][c].type='empty';}else if(cell.type==='trap'){handleTrapCell();mapData[r][c].type='empty';}else if(cell.type==='cache'){handleCacheCell();mapData[r][c].type='empty';}else if(cell.type==='treasure'){const eq=generateEquipment(getDungeonEquipmentLevel(currentDungeon.floorLevel+TIERS_PER_LEVEL-1));tryAddEquipToInventory(eq);logInfo(`寶箱: ${equipToString(eq,false)}`);mapData[r][c].type='empty';}updateButtons();renderMap();updateStatusBar();throttleSave();}",
    "}else if(cell.type==='shrine'){handleShrineCell();mapData[r][c].type='empty';}else if(cell.type==='trap'){handleTrapCell();mapData[r][c].type='empty';}else if(cell.type==='cache'){handleCacheCell();mapData[r][c].type='empty';}else if(cell.type==='treasure'){const eq=generateEquipment(getDungeonEquipmentLevel(currentDungeon.floorLevel+TIERS_PER_LEVEL-1));tryAddEquipToInventory(eq);logInfo(`寶箱: ${equipToString(eq,false)}`);mapData[r][c].type='empty';}updateButtons();renderMap({cells:mapDirty});updateStatusBar();throttleSave();}",
    "move render partial",
)

# battle UI cache
rep(
    "function updateBattleUI(){if(!inCombat||!currentEnemy||gameOver)return;document.getElementById('player-name').textContent='> '+(playerCustomName||'你');const enemyCard=document.getElementById('enemy-card');enemyCard.className='battle-entity '+(currentEnemy.isBoss?'boss-side':'enemy-side');document.getElementById('battle-player-hp').textContent=`${player.hp}/${player.maxHp}`;document.getElementById('battle-player-shield').textContent=`${player.shield}/${player.maxShield}`;document.getElementById('battle-player-atk-main').textContent=formatCombatNum(getMainAtk());document.getElementById('battle-player-atk-off').textContent=formatCombatNum(getOffAtk());document.getElementById('battle-player-def').textContent=formatCombatNum(player.def);document.getElementById('battle-player-spd').textContent=formatCombatNum(player.spd);document.getElementById('battle-player-crit').textContent=Math.floor(player.critChance*100)+'%';document.getElementById('battle-player-dodge').textContent=Math.floor(player.dodge*100)+'%';document.getElementById('player-hp-bar').innerHTML=renderHPBar(player.hp,player.maxHp);document.getElementById('player-shield-bar').innerHTML=player.maxShield>0?renderShieldBar(player.shield,player.maxShield):'';document.getElementById('battle-player-xp').textContent=`${player.xp}/${player.xpToNext}`;document.getElementById('player-xp-bar').innerHTML=renderXPBar(player.xp,player.xpToNext);document.getElementById('battle-enemy-name').textContent='> '+(currentEnemy.isBoss?'BOSS: ':'')+currentEnemy.name;document.getElementById('battle-enemy-hp').textContent=`${Math.max(0,currentEnemy.hp)}/${currentEnemy.maxHp}`;document.getElementById('battle-enemy-atk').textContent=formatCombatNum(currentEnemy.atk);document.getElementById('battle-enemy-def').textContent=formatCombatNum(currentEnemy.def);document.getElementById('battle-enemy-spd').textContent=formatCombatNum(currentEnemy.spd);document.getElementById('battle-enemy-dodge').textContent=Math.floor((currentEnemy.dodge||0)*100)+'%';document.getElementById('enemy-hp-bar').innerHTML=renderHPBar(Math.max(0,currentEnemy.hp),currentEnemy.maxHp);}",
    "let battleUiCache={playerHp:'',playerShield:'',enemyHp:'',statsKey:''};function updateBattleUI(opts){if(!inCombat||!currentEnemy||gameOver)return;const full=!!(opts&&opts.full);const playerHpKey=player.hp+'/'+player.maxHp;const playerShieldKey=player.shield+'/'+player.maxShield;const enemyHpKey=Math.max(0,currentEnemy.hp)+'/'+currentEnemy.maxHp;const statsKey=[getMainAtk(),getOffAtk(),player.def,player.spd,currentEnemy.atk,currentEnemy.def,currentEnemy.spd,currentEnemy.isBoss].join('|');if(full||statsKey!==battleUiCache.statsKey){battleUiCache.statsKey=statsKey;document.getElementById('player-name').textContent='> '+(playerCustomName||'你');const enemyCard=document.getElementById('enemy-card');enemyCard.className='battle-entity '+(currentEnemy.isBoss?'boss-side':'enemy-side');document.getElementById('battle-player-atk-main').textContent=formatCombatNum(getMainAtk());document.getElementById('battle-player-atk-off').textContent=formatCombatNum(getOffAtk());document.getElementById('battle-player-def').textContent=formatCombatNum(player.def);document.getElementById('battle-player-spd').textContent=formatCombatNum(player.spd);document.getElementById('battle-player-crit').textContent=Math.floor(player.critChance*100)+'%';document.getElementById('battle-player-dodge').textContent=Math.floor(player.dodge*100)+'%';document.getElementById('battle-enemy-name').textContent='> '+(currentEnemy.isBoss?'BOSS: ':'')+currentEnemy.name;document.getElementById('battle-enemy-atk').textContent=formatCombatNum(currentEnemy.atk);document.getElementById('battle-enemy-def').textContent=formatCombatNum(currentEnemy.def);document.getElementById('battle-enemy-spd').textContent=formatCombatNum(currentEnemy.spd);document.getElementById('battle-enemy-dodge').textContent=Math.floor((currentEnemy.dodge||0)*100)+'%';document.getElementById('battle-player-xp').textContent=`${player.xp}/${player.xpToNext}`;document.getElementById('player-xp-bar').innerHTML=renderXPBar(player.xp,player.xpToNext);}if(full||playerHpKey!==battleUiCache.playerHp){battleUiCache.playerHp=playerHpKey;document.getElementById('battle-player-hp').textContent=playerHpKey;document.getElementById('player-hp-bar').innerHTML=renderHPBar(player.hp,player.maxHp);}if(full||playerShieldKey!==battleUiCache.playerShield){battleUiCache.playerShield=playerShieldKey;document.getElementById('battle-player-shield').textContent=playerShieldKey;document.getElementById('player-shield-bar').innerHTML=player.maxShield>0?renderShieldBar(player.shield,player.maxShield):'';}if(full||enemyHpKey!==battleUiCache.enemyHp){battleUiCache.enemyHp=enemyHpKey;document.getElementById('battle-enemy-hp').textContent=enemyHpKey;document.getElementById('enemy-hp-bar').innerHTML=renderHPBar(Math.max(0,currentEnemy.hp),currentEnemy.maxHp);}}",
    "battle ui cache",
)

rep(
    "enterCombat(enemy){if(gameOver||player.isPermanentlyDead)return;currentEnemy={...enemy};inCombat=true;attackQueue=[];isProcessingQueue=false;showBattleScreen(true);updateBattleUI();",
    "enterCombat(enemy){if(gameOver||player.isPermanentlyDead)return;currentEnemy={...enemy};inCombat=true;attackQueue=[];isProcessingQueue=false;battleUiCache={playerHp:'',playerShield:'',enemyHp:'',statsKey:''};showBattleScreen(true);updateBattleUI({full:true});",
    "enter combat full ui",
)

rep(
    "function leaveDungeon(cleared=false){const clearedTier=currentDungeon?currentDungeon.tier:null;const hadCurse=hasActiveDailyCurse();bossDefeatOverlay.style.display='none';clearAllTimers();clearDroneTimers();inCombat=false;",
    "function leaveDungeon(cleared=false){const clearedTier=currentDungeon?currentDungeon.tier:null;const hadCurse=hasActiveDailyCurse();bossDefeatOverlay.style.display='none';clearAllTimers();clearDroneTimers();dungeonBannerSig='';if(hasActiveCloudSession())void uploadCurrentAccountToCloud({silent:true}).catch(()=>{});inCombat=false;",
    "leave dungeon sync",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (v2.17.7 dungeon perf)")
