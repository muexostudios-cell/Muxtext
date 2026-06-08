#!/usr/bin/env python3
"""v2.14.3: fix level rollback, reconcile XP on load/save, smarter cloud merge."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:240]}")
    s = s.replace(old, new, 1)


# version
rep("GAME_VERSION='2.14.2'", "GAME_VERSION='2.14.3'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.14.2'",
    "GAME_VERSION_HISTORY=[{version:'2.14.3',date:'2026-06-08',summary:{zh:'v2.14.3 修復等級異常回調；強化經驗進度保存與雲端合併。',en:'v2.14.3 fix level rollback; improve XP progress save and cloud merge.'}},{version:'2.14.2'",
    "hist",
)
rep("SAVE_VERSION=42", "SAVE_VERSION=43", "save")

# i18n
rep(
    'logBalanceV213:"[平衡 v2.13] 經驗值優化：貼合純手動硬核戰鬥，適等級地城約 1 趟升 1 級；通關額外獎勵；重複刷圖經驗懲罰放寬。",',
    'logBalanceV214:"[修復 v2.14.3] 等級與經驗進度已校準並強化存檔；雲端同步會保留較高的等級進度，避免異常回調。",logBalanceV213:"[平衡 v2.13] 經驗值優化：貼合純手動硬核戰鬥，適等級地城約 1 趟升 1 級；通關額外獎勵；重複刷圖經驗懲罰放寬。",',
    "i18n zh",
)
rep(
    'logBalanceV213:"[Balance v2.13] XP tuned for manual hardcore combat; clear bonus; softer repeat-run XP penalty.",',
    'logBalanceV214:"[Fix v2.14.3] Level/XP progress reconciled on save; cloud sync keeps higher level progress.",logBalanceV213:"[Balance v2.13] XP tuned for manual hardcore combat; clear bonus; softer repeat-run XP penalty.",',
    "i18n en",
)

# XP reconcile helpers
rep(
    "function getDungeonClearXpBonus(tier){const rate=tier==='hell'?XP_CLEAR_BONUS_HELL:tier==='hard'?XP_CLEAR_BONUS_HARD:XP_CLEAR_BONUS_NORMAL;return Math.max(0,Math.floor((player.xpToNext||1)*rate));}",
    "function getDungeonClearXpBonus(tier){const rate=tier==='hell'?XP_CLEAR_BONUS_HELL:tier==='hard'?XP_CLEAR_BONUS_HARD:XP_CLEAR_BONUS_NORMAL;return Math.max(0,Math.floor((player.xpToNext||1)*rate));}function getPlayerProgressScore(p){if(!p)return 0;const lv=Math.max(1,Math.floor(Number(p.level)||1)),peak=Math.max(lv,Math.floor(Number(p.stats&&p.stats.peakLevel)||0)),xp=Math.max(0,Math.floor(Number(p.xp)||0));return peak*1e12+xp;}function getSaveProgressScore(saveRaw){try{const data=JSON.parse(saveRaw);return getPlayerProgressScore(data&&data.player);}catch(e){return 0;}}function processPlayerLevelUps(opts={}){const showPopup=opts.showPopup!==false;let leveled=false;player.xp=Math.max(0,Math.floor(Number(player.xp)||0));player.level=Math.max(1,Math.floor(Number(player.level)||1));player.xpToNext=getXpToNext(player.level);while(player.xp>=player.xpToNext){player.xp-=player.xpToNext;player.level++;player.xpToNext=getXpToNext(player.level);addTalentPoints(1);leveled=true;if(showPopup)notifyLevelUp(player.level,true);}if(!player.stats)player.stats=getDefaultPlayer().stats;player.stats.peakLevel=Math.max(player.level,Math.floor(Number(player.stats.peakLevel)||0));if(leveled&&!opts.skipRecalc){recalcPlayerStats();player.hp=player.maxHp;player.shield=player.maxShield||0;}return leveled;}function reconcilePlayerXpProgress(opts={}){player.level=Math.max(1,Math.floor(Number(player.level)||1));player.xp=Math.max(0,Math.floor(Number(player.xp)||0));if(!player.stats)player.stats=getDefaultPlayer().stats;const peak=Math.floor(Number(player.stats.peakLevel)||0);if(peak>player.level)player.level=peak;player.xpToNext=getXpToNext(player.level);return processPlayerLevelUps({showPopup:false,skipRecalc:opts.skipRecalc});}",
    "xp helpers",
)

# default player peakLevel
rep(
    "stats:{createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0,",
    "stats:{createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0,peakLevel:0,",
    "default peak",
)

# save / load
rep(
    "function saveGame(){if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};initTalentPoints();",
    "function saveGame(){if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};reconcilePlayerXpProgress({skipRecalc:true});initTalentPoints();",
    "save reconcile",
)
rep(
    "player=data.player;player=applyPlayerDefaults(player);if(!player.stats)",
    "player=data.player;player=applyPlayerDefaults(player);reconcilePlayerXpProgress({skipRecalc:true});if(!player.stats)",
    "load reconcile",
)

# migrate
rep(
    "function migrateSave(data){if(data.version<42){data._balanceV213Notice=true;data.version=42;}",
    "function migrateSave(data){if(data.version<43){if(data.player){const lv=Math.max(1,Math.floor(Number(data.player.level)||1));if(!data.player.stats)data.player.stats={};data.player.stats.peakLevel=Math.max(lv,Math.floor(Number(data.player.stats.peakLevel)||0));}data._balanceV214Notice=true;data.version=43;}if(data.version<42){data._balanceV213Notice=true;data.version=42;}",
    "migrate",
)
rep(
    "const _balanceV213Notice=!!data._balanceV213Notice;delete data._balanceV213Notice;if(data.autoHerbSettings)",
    "const _balanceV213Notice=!!data._balanceV213Notice;delete data._balanceV213Notice;const _balanceV214Notice=!!data._balanceV214Notice;delete data._balanceV214Notice;if(data.autoHerbSettings)",
    "load notice var",
)
rep(
    "if(_balanceV213Notice)logInfo(t('logBalanceV213'));leaderboardTrackedLevel=-1;",
    "if(_balanceV213Notice)logInfo(t('logBalanceV213'));if(_balanceV214Notice)logInfo(t('logBalanceV214'));leaderboardTrackedLevel=-1;",
    "load notice log",
)

# cloud merge by progress score
rep(
    "function mergeSaveData(localRaw,cloudRaw){const lt=localRaw?getSaveUpdatedAt(localRaw):0;const ct=cloudRaw?getSaveUpdatedAt(cloudRaw):0;if(!cloudRaw||ct>lt)return{save:cloudRaw,pulled:!!cloudRaw&&ct>lt};return{save:localRaw,pulled:false};}",
    "function mergeSaveData(localRaw,cloudRaw){if(!cloudRaw)return{save:localRaw,pulled:false};if(!localRaw)return{save:cloudRaw,pulled:true};const lp=getSaveProgressScore(localRaw),cp=getSaveProgressScore(cloudRaw),lt=getSaveUpdatedAt(localRaw),ct=getSaveUpdatedAt(cloudRaw);if(cp>lp)return{save:cloudRaw,pulled:true};if(lp>cp)return{save:localRaw,pulled:false};if(ct>lt)return{save:cloudRaw,pulled:true};return{save:localRaw,pulled:false};}",
    "merge save",
)

# kill enemy: use shared level-up + immediate save
rep(
    "let lvlUp=false;while(player.xp>=player.xpToNext){player.xp-=player.xpToNext;player.level++;player.xpToNext=getXpToNext(player.level);addTalentPoints(1);recalcPlayerStats();player.hp=player.maxHp;player.shield=player.maxShield;lvlUp=true;notifyLevelUp(player.level,true);}if(lvlUp)flashEntity('player-card');",
    "const lvlUp=processPlayerLevelUps({showPopup:true});if(lvlUp){flashEntity('player-card');saveGame();}",
    "kill level up",
)

# flush save when tab hidden
rep(
    "if(document.hidden){if(playtimeInterval){clearInterval(playtimeInterval);playtimeInterval=null;}}else if(!playtimeInterval)startPlaytimeCounter();});}",
    "if(document.hidden){if(playtimeInterval){clearInterval(playtimeInterval);playtimeInterval=null;}try{if(player&&!player.isPermanentlyDead)saveGame();}catch(e){}}else if(!playtimeInterval)startPlaytimeCounter();});}",
    "visibility save",
)

path.write_text(s)
print("v2.14.3 XP save fix OK")
