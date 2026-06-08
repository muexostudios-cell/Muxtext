#!/usr/bin/env python3
"""v2.17.6: Fix level rollback to 1 and cross-device login/progress restore."""
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
rep("GAME_VERSION='2.17.5'", "GAME_VERSION='2.17.6'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.5',date:'2026-06-08',summary:{zh:'v2.17.5 伺服器強化與加載優化：非阻塞啟動、預連線、延遲載入 Stripe/Gun、背景伺服器預熱。',en:'v2.17.5 server strengthen + load optimize: non-blocking boot, preconnect, lazy Stripe/Gun, background warmup.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.6',date:'2026-06-08',summary:{zh:'v2.17.6 修復等級歸零與跨裝置登入：防雲端覆寫、啟動拉取進度、強化合併與上傳保護。',en:'v2.17.6 fix level rollback and cross-device login: anti-wipe upload, boot cloud pull, merge guards.'}},{version:'2.17.5',date:'2026-06-08',summary:{zh:'v2.17.5 伺服器強化與加載優化：非阻塞啟動、預連線、延遲載入 Stripe/Gun、背景伺服器預熱。',en:'v2.17.5 server strengthen + load optimize: non-blocking boot, preconnect, lazy Stripe/Gun, background warmup.'}},",
    "hist",
)
rep("SAVE_VERSION=51", "SAVE_VERSION=52", "save")

rep(
    'logBalanceV2175:"[優化 v2.17.5] 伺服器預熱與加載加速：啟動不再等待 Gun 中繼、延遲載入付款腳本、背景連線雲端。",logBalanceV2174:',
    'logBalanceV2176:"[修復 v2.17.6] 修復等級異常歸 1 與跨裝置無法讀取進度；雲端同步不再覆寫較高進度。",logBalanceV2175:"[優化 v2.17.5] 伺服器預熱與加載加速：啟動不再等待 Gun 中繼、延遲載入付款腳本、背景連線雲端。",logBalanceV2174:',
    "i18n zh log",
)
rep(
    'logBalanceV2175:"[Optimize v2.17.5] Server warmup + faster load: non-blocking boot, lazy Stripe, background cloud connect.",logBalanceV2174:',
    'logBalanceV2176:"[Fix v2.17.6] Level rollback and cross-device progress restore; cloud sync no longer overwrites higher saves.",logBalanceV2175:"[Optimize v2.17.5] Server warmup + faster load: non-blocking boot, lazy Stripe, background cloud connect.",logBalanceV2174:',
    "i18n en log",
)
# richer progress score + parse helper
rep(
    "function getPlayerProgressScore(p){if(!p)return 0;const lv=Math.max(1,Math.floor(Number(p.level)||1)),peak=Math.max(lv,Math.floor(Number(p.stats&&p.stats.peakLevel)||0)),xp=Math.max(0,Math.floor(Number(p.xp)||0));return peak*1e12+xp;}",
    "function getPlayerProgressScore(p){if(!p)return 0;const lv=Math.max(1,Math.floor(Number(p.level)||1)),peak=Math.max(lv,Math.floor(Number(p.stats&&p.stats.peakLevel)||0)),xp=Math.max(0,Math.floor(Number(p.xp)||0)),gold=Math.max(0,Math.floor(Number(p.gold)||0)),clears=Math.max(0,Math.floor(Number(p.stats&&p.stats.dungeonClears)||0)),equip=Array.isArray(p.equipInventory)?p.equipInventory.length:0;return peak*1e15+xp*1e9+gold*1e3+clears*1e6+equip;}function getSaveProgressScoreFromPlayer(player){return getPlayerProgressScore(player);}function parseSavePlayer(raw){try{const data=typeof raw==='string'?JSON.parse(raw):raw;return data&&data.player?data.player:null;}catch(e){return null;}}",
    "progress score",
)

rep(
    "function getSaveProgressScore(saveRaw){try{const data=JSON.parse(saveRaw);return getPlayerProgressScore(data&&data.player);}catch(e){return 0;}}",
    "function getSaveProgressScore(saveRaw){const p=parseSavePlayer(saveRaw);return p?getPlayerProgressScore(p):0;}",
    "save progress score",
)

# merge guard: never accept empty cloud over local progress
rep(
    "function mergeSaveData(localRaw,cloudRaw){if(!cloudRaw)return{save:localRaw,pulled:false};if(!localRaw)return{save:cloudRaw,pulled:true};const lp=getSaveProgressScore(localRaw),cp=getSaveProgressScore(cloudRaw),lt=getSaveUpdatedAt(localRaw),ct=getSaveUpdatedAt(cloudRaw);if(cp>lp)return{save:cloudRaw,pulled:true};if(lp>cp)return{save:localRaw,pulled:false};if(ct>lt)return{save:cloudRaw,pulled:true};return{save:localRaw,pulled:false};}",
    "function mergeSaveData(localRaw,cloudRaw){if(!cloudRaw)return{save:localRaw,pulled:false};if(!localRaw)return{save:cloudRaw,pulled:true};const lp=getSaveProgressScore(localRaw),cp=getSaveProgressScore(cloudRaw);if(cp<=0&&lp>0)return{save:localRaw,pulled:false};if(lp<=0&&cp>0)return{save:cloudRaw,pulled:true};const lt=getSaveUpdatedAt(localRaw),ct=getSaveUpdatedAt(cloudRaw);if(cp>lp)return{save:cloudRaw,pulled:true};if(lp>cp)return{save:localRaw,pulled:false};if(ct>lt)return{save:cloudRaw,pulled:true};return{save:localRaw,pulled:false};}",
    "merge save",
)

# fetch cloud with login retries
rep(
    "async function fetchCloudAccount(key,timeoutMs=10000){for(let attempt=0;attempt<2;attempt++){const data=await fetchCloudAccountOnce(key,timeoutMs);if(data!==undefined)return data;if(attempt===0){resetGameGun();await refreshGunPeers();}}return null;}",
    "async function fetchCloudAccount(key,timeoutMs=10000,opts){const login=!!(opts&&opts.login);const attempts=login?5:2;const perTry=login?Math.max(8000,timeoutMs):timeoutMs;for(let attempt=0;attempt<attempts;attempt++){const data=await fetchCloudAccountOnce(key,perTry);if(data!==undefined)return data;if(attempt<attempts-1){resetGameGun();await refreshGunPeers(login?{skipWiki:attempt<2}:undefined);}}return null;}",
    "fetch cloud",
)

# safe cloud apply + refresh helper
rep(
    "async function applyCloudRecordToAccount(acc,cloud,password){if(cloud.gameVersion&&compareGameVersion(cloud.gameVersion,GAME_VERSION)>0){showVersionUpdateNotice({version:cloud.gameVersion,summary:(getVersionHistoryEntry(cloud.gameVersion)||{}).summary});throw new Error('version');}const profile=cloud.encProfile?JSON.parse(await decryptString(cloud.encProfile,password,cloud.salt)):{displayName:acc.displayName,avatar:acc.avatar};let cloudSave=null;if(cloud.encSave){cloudSave=await decryptString(cloud.encSave,password,cloud.salt);}const merged=mergeSaveData(acc.save,cloudSave);acc.displayName=(profile.displayName||acc.displayName||acc.username).substring(0,12);acc.avatar=profile.avatar||acc.avatar||'';acc.save=merged.save;acc.cloudSalt=cloud.salt;acc.passHash=cloud.passHash;return merged.pulled;}",
    "async function applyCloudRecordToAccount(acc,cloud,password){if(cloud.gameVersion&&compareGameVersion(cloud.gameVersion,GAME_VERSION)>0){showVersionUpdateNotice({version:cloud.gameVersion,summary:(getVersionHistoryEntry(cloud.gameVersion)||{}).summary});throw new Error('version');}let profile={displayName:acc.displayName,avatar:acc.avatar};if(cloud.encProfile){try{profile=JSON.parse(await decryptString(cloud.encProfile,password,cloud.salt));}catch(e){bugClientSignals.add('cloud_decrypt_fail');}}let cloudSave=null;if(cloud.encSave){try{cloudSave=await decryptString(cloud.encSave,password,cloud.salt);}catch(e){bugClientSignals.add('cloud_decrypt_fail');cloudSave=null;}}const merged=mergeSaveData(acc.save,cloudSave);acc.displayName=(profile.displayName||acc.displayName||acc.username).substring(0,12);acc.avatar=profile.avatar||acc.avatar||'';acc.save=merged.save;acc.cloudSalt=cloud.salt;acc.passHash=cloud.passHash;if(acc.save){const score=getSaveProgressScore(acc.save);acc.lastKnownProgress=Math.max(Math.floor(Number(acc.lastKnownProgress)||0),score);}return merged.pulled;}async function refreshAccountSaveFromCloud(){const key=getSessionKey();const secret=restoreSessionAccountSecret();if(!key||!secret||secret.key!==key)return false;const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;const cloud=await fetchCloudAccount(key,12000,{login:true});if(!cloud||cloud.passHash!==acc.passHash)return false;const pulled=await applyCloudRecordToAccount(acc,cloud,secret.password);saveAccountStore(store);return pulled;}",
    "apply cloud",
)

# upload anti-wipe + downgrade block
rep(
    "async function uploadCloudAccount(key,acc,password){try{const payload=await buildCloudPayload(acc,password);await putCloudAccount(key,payload);acc.cloudSalt=payload.salt;markAccountCloudPushed();return true;}catch(e){return false;}}",
    "async function uploadCloudAccount(key,acc,password){try{const remote=await fetchCloudAccountOnce(key,8000);if(remote&&remote.passHash&&remote.passHash!==acc.passHash)throw new Error('auth');if(!acc.save){if(remote&&remote.encSave)return false;}else if(remote&&remote.encSave){try{const remoteSave=await decryptString(remote.encSave,password,remote.salt||acc.cloudSalt);const localScore=getSaveProgressScore(acc.save),remoteScore=getSaveProgressScore(remoteSave);if(remoteScore>localScore){const merged=mergeSaveData(acc.save,remoteSave);acc.save=merged.save;const store=loadAccountStore();store.byKey[key]=acc;saveAccountStore(store);markAccountCloudPushed();return true;}if(localScore<remoteScore)return false;}catch(e){if(remote&&remote.encSave)return false;}}const payload=await buildCloudPayload(acc,password);if(!payload.encSave&&remote&&remote.encSave)return false;await putCloudAccount(key,payload);acc.cloudSalt=payload.salt;markAccountCloudPushed();return true;}catch(e){return false;}}",
    "upload cloud",
)

# login: relay vs password errors + login fetch retries
rep(
    "const cloud=devLogin?null:await fetchCloudAccount(key);",
    "const cloud=devLogin?null:await fetchCloudAccount(key,12000,{login:true});",
    "login fetch",
)
rep(
    "}else{if(!acc||acc.passHash!==passHash)return{ok:false,msg:'accountErrorLogin'};}",
    "}else{if(!acc||acc.passHash!==passHash)return{ok:false,msg:!acc?'cloudSyncRelayBlocked':'accountErrorLogin'};}",
    "login no cloud",
)

# handleAccountSubmit: allow login attempt when relay slow on new device
rep(
    "const relayOk=await ensureGunRelayReady(12000);if(!relayOk&&!hasLocal){showAccountError(t('cloudSyncRelayBlocked'));return;}if(!relayOk)logInfo(t('cloudSyncRelayBlocked'));}",
    "const relayOk=await ensureGunRelayReady(hasLocal?10000:20000);if(!relayOk)logInfo(t('cloudSyncRelayBlocked'));}",
    "login relay",
)

# beginGameAfterAccount: pull cloud before init, guarded upload
rep(
    "function beginGameAfterAccount(pulled){hideAccountOverlay();loadAccountProfile();initGame();applyDevAccountBootstrap();if(pulled)logInfo(t('cloudSyncPulled'));requestAnimationFrame(updateLayoutMode);restartCloudSyncRuntime();void uploadCurrentAccountToCloud({silent:true}).catch(()=>{});publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "async function beginGameAfterAccount(pulled){hideAccountOverlay();loadAccountProfile();if(restoreSessionAccountSecret()){try{const fresh=await refreshAccountSaveFromCloud();if(fresh)pulled=true;}catch(e){}}initGame();applyDevAccountBootstrap();if(pulled)logInfo(t('cloudSyncPulled'));requestAnimationFrame(updateLayoutMode);restartCloudSyncRuntime();if(getAccountSaveRaw()&&getSaveProgressScore(getAccountSaveRaw())>0)void uploadCurrentAccountToCloud({silent:true}).catch(()=>{});publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "begin game",
)

# continueGameBoot awaits cloud refresh path via beginGameAfterAccount
rep(
    "function continueGameBoot(){if(gameBooted)return;gameBooted=true;if(getSessionKey()&&getActiveAccount()){restoreSessionAccountSecret();beginGameAfterAccount(false);}else{showAccountOverlay();refreshCloudSyncDisplay();}requestAnimationFrame(updateLayoutMode);}",
    "function continueGameBoot(){if(gameBooted)return;gameBooted=true;if(getSessionKey()&&getActiveAccount()){restoreSessionAccountSecret();void beginGameAfterAccount(false);}else{showAccountOverlay();refreshCloudSyncDisplay();}requestAnimationFrame(updateLayoutMode);}",
    "continue boot",
)

# saveGame: block significant progress regression writes
rep(
    "function saveGame(){if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};reconcilePlayerXpProgress({skipRecalc:true});initTalentPoints();const state={version:SAVE_VERSION,savedAt:Date.now(),player,currentDungeon,mapData,playerPos,monstersRemaining,inDungeon,bossDefeated,bossLeaveAvailable,lockedEquipment:[...lockedEquipment],autoHerbSettings:{...settings.autoHerb}};state.checksum=generateChecksum(state);",
    "function saveGame(){if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};reconcilePlayerXpProgress({skipRecalc:true});initTalentPoints();const prevRaw=getSessionKey()?getAccountSaveRaw():localStorage.getItem('td_full_save');if(prevRaw){try{const prevPlayer=parseSavePlayer(prevRaw);const prevScore=prevPlayer?getPlayerProgressScore(prevPlayer):0,nextScore=getPlayerProgressScore(player);if(prevScore>0&&nextScore+1e12<prevScore){bugClientSignals.add('level_regression');return;}}catch(e){}}const state={version:SAVE_VERSION,savedAt:Date.now(),player,currentDungeon,mapData,playerPos,monstersRemaining,inDungeon,bossDefeated,bossLeaveAvailable,lockedEquipment:[...lockedEquipment],autoHerbSettings:{...settings.autoHerb}};state.checksum=generateChecksum(state);",
    "save guard",
)

# reconcile: signal regression
rep(
    "const peak=Math.floor(Number(player.stats.peakLevel)||0);if(peak>player.level)player.level=peak;",
    "const peak=Math.floor(Number(player.stats.peakLevel)||0);if(peak>player.level){bugClientSignals.add('level_regression');player.level=peak;}",
    "reconcile peak",
)

# loadGame: checksum fail signal
rep(
    "if(generateChecksum(data)!==expected)return false;",
    "if(generateChecksum(data)!==expected){bugClientSignals.add('save_checksum_fail');return false;}",
    "checksum fail",
)

# migrate v52
rep(
    "function migrateSave(data){if(data.version<46){data._balanceV217Notice=true;data.version=46;}",
    "function migrateSave(data){if(data.version<52){if(data.player){const lv=Math.max(1,Math.floor(Number(data.player.level)||1));if(!data.player.stats)data.player.stats={};data.player.stats.peakLevel=Math.max(lv,Math.floor(Number(data.player.stats.peakLevel)||0));}data._balanceV2176Notice=true;data.version=52;}if(data.version<46){data._balanceV217Notice=true;data.version=46;}",
    "migrate",
)
rep(
    "const _balanceV217Notice=!!data._balanceV217Notice;delete data._balanceV217Notice;if(data.autoHerbSettings)",
    "const _balanceV217Notice=!!data._balanceV217Notice;delete data._balanceV217Notice;const _balanceV2176Notice=!!data._balanceV2176Notice;delete data._balanceV2176Notice;if(data.autoHerbSettings)",
    "load notice var",
)
rep(
    "if(_balanceV214Notice)logInfo(t('logBalanceV214'));if(_balanceV215Notice)logInfo(t('logBalanceV215'));if(_balanceV216Notice)logInfo(t('logBalanceV216'));if(_balanceV217Notice)logInfo(t('logBalanceV2175'));logInfo(t('logBalanceV2174'));logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'));leaderboardTrackedLevel=-1;",
    "if(_balanceV214Notice)logInfo(t('logBalanceV214'));if(_balanceV215Notice)logInfo(t('logBalanceV215'));if(_balanceV216Notice)logInfo(t('logBalanceV216'));if(_balanceV217Notice)logInfo(t('logBalanceV217'));if(_balanceV2176Notice)logInfo(t('logBalanceV2176'));logInfo(t('logBalanceV2175'));logInfo(t('logBalanceV2174'));logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'));leaderboardTrackedLevel=-1;",
    "load notice log",
)

# bug catalog local fix version
rep(
    "LOCAL_KNOWN_BUG_FIXES={'level-rollback':'2.14.3',",
    "LOCAL_KNOWN_BUG_FIXES={'level-rollback':'2.17.6',",
    "bug catalog",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (v2.17.6 level rollback + cross-device fix)")
