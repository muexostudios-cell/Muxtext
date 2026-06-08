#!/usr/bin/env python3
"""2s cloud sync loop; when status is local-save pending, force upload to server."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:260]}")
    s = s.replace(old, new, 1)


rep(
    "cloudUploadTimeout=null,cloudSyncInProgress=false",
    "CLOUD_AUTO_SYNC_MS=2000,cloudUploadTimeout=null,cloudUploadInterval=null,cloudUploadBusy=false,cloudSyncInProgress=false",
    "interval vars",
)

rep(
    'cloudSyncDetailLocal:"尚未登入雲端帳號，進度僅儲存於本機瀏覽器。"',
    'cloudSyncDetailLocal:"尚未登入雲端帳號，進度僅儲存於本機瀏覽器。",cloudSyncDetailLocalPending:"本機進度尚未同步至雲端，每 2 秒強制上傳…"',
    "i18n zh local pending",
)

rep(
    'cloudSyncDetailLocal:"Not signed in. Progress is stored only in this browser."',
    'cloudSyncDetailLocal:"Not signed in. Progress is stored only in this browser.",cloudSyncDetailLocalPending:"Local progress not on cloud yet; force upload every 2s…"',
    "i18n en local pending",
)

rep(
    'cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 雲端中繼已連線，變更會自動同步"',
    'cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 雲端中繼已連線，每 2 秒自動同步"',
    "i18n zh connected 2s",
)

rep(
    "cloudSyncDetailConnected:\"Account {0} · Lv.{1} · Cloud relay connected; changes sync automatically\"",
    "cloudSyncDetailConnected:\"Account {0} · Lv.{1} · Cloud relay connected; auto-sync every 2s\"",
    "i18n en connected 2s",
)

rep(
    "function scheduleCloudUpload(){if(!restoreSessionAccountSecret())return;if(cloudUploadTimeout)clearTimeout(cloudUploadTimeout);cloudUploadTimeout=setTimeout(()=>{uploadCurrentAccountToCloud();cloudUploadTimeout=null;},30000);}",
    "function accountNeedsCloudPush(){if(!hasActiveCloudSession())return false;const acc=getActiveAccount();if(!acc||!acc.save)return false;const localAt=getSaveUpdatedAt(acc.save)||0;return !acc.lastCloudPushAt||localAt>acc.lastCloudPushAt;}function markAccountCloudPushed(){const key=getSessionKey();if(!key)return;const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return;acc.lastCloudPushAt=Date.now();saveAccountStore(store);}function stopCloudAutoSync(){if(cloudUploadInterval){clearInterval(cloudUploadInterval);cloudUploadInterval=null;}if(cloudUploadTimeout){clearTimeout(cloudUploadTimeout);cloudUploadTimeout=null;}}function startCloudAutoSync(){if(!hasActiveCloudSession()){stopCloudAutoSync();return;}if(cloudUploadInterval)return;cloudUploadInterval=setInterval(()=>tickCloudAutoSync(),CLOUD_AUTO_SYNC_MS);tickCloudAutoSync();}async function forceCloudSyncFromLocal(){const key=getSessionKey();const secret=restoreSessionAccountSecret();if(!key||!secret||secret.key!==key)return false;if(cloudSyncInProgress||cloudUploadBusy)return false;if(typeof navigator!=='undefined'&&navigator.onLine===false)return false;if(typeof saveGame==='function')saveGame();const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;cloudUploadBusy=true;let ok=false;try{const cloud=await fetchCloudAccount(key);if(cloud&&cloud.passHash!==acc.passHash)throw new Error('auth');if(cloud){const merged=await applyCloudRecordToAccount(acc,cloud,secret.password);if(merged.pulled){saveAccountStore(store);if(loadGame()){renderAllPanels();updateStatusBar();updateButtons();renderDungeonAdventure();}}}ok=await uploadCloudAccount(key,acc,secret.password);if(ok){markAccountCloudPushed();saveAccountStore(store);publishLeaderboardEntry(true);}}catch(e){ok=false;}finally{cloudUploadBusy=false;refreshCloudSyncDisplay();}return ok;}function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession())return;if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(cloudSyncState==='local'||accountNeedsCloudPush()){forceCloudSyncFromLocal();return;}if(typeof saveGame==='function')saveGame();uploadCurrentAccountToCloud({silent:true});}function scheduleCloudUpload(){startCloudAutoSync();}",
    "auto sync loop",
)

rep(
    "function refreshCloudSyncDisplay(){if(cloudSyncState==='syncing'){updateCloudSyncDetail();return;}if(!hasActiveCloudSession()){updateCloudSyncUI('local');return;}if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');return;}updateCloudSyncUI('connected');}",
    "function refreshCloudSyncDisplay(){if(cloudSyncState==='syncing'){updateCloudSyncDetail();return;}if(!hasActiveCloudSession()){updateCloudSyncUI('local');return;}if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');return;}if(accountNeedsCloudPush()){updateCloudSyncUI('local');return;}updateCloudSyncUI('connected');}",
    "local until cloud pushed",
)

rep(
    "if(st==='local')return t('cloudSyncDetailLocal');",
    "if(st==='local')return hasActiveCloudSession()?t('cloudSyncDetailLocalPending'):t('cloudSyncDetailLocal');",
    "detail local pending",
)

rep(
    "async function uploadCurrentAccountToCloud(){const key=getSessionKey();const secret=restoreSessionAccountSecret();if(!key||!secret||secret.key!==key)return false;if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');showNetworkOverlay();return false;}const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;updateCloudSyncUI('syncing');const ok=await uploadCloudAccount(key,acc,secret.password);if(ok){saveAccountStore(store);publishLeaderboardEntry(true);}else{refreshCloudSyncDisplay();showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}return ok;}",
    "async function uploadCurrentAccountToCloud(opts){const silent=!!(opts&&opts.silent);if(cloudUploadBusy)return false;const key=getSessionKey();const secret=restoreSessionAccountSecret();if(!key||!secret||secret.key!==key)return false;if(typeof navigator!=='undefined'&&navigator.onLine===false){if(!silent){updateCloudSyncUI('offline');showNetworkOverlay();}return false;}const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;cloudUploadBusy=true;if(!silent)updateCloudSyncUI('syncing');let ok=false;try{ok=await uploadCloudAccount(key,acc,secret.password);if(ok){markAccountCloudPushed();saveAccountStore(store);publishLeaderboardEntry(true);if(!silent)refreshCloudSyncDisplay();}else if(!silent){refreshCloudSyncDisplay();showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}}finally{cloudUploadBusy=false;if(silent)refreshCloudSyncDisplay();}return ok;}",
    "silent upload + push mark",
)

rep(
    "const uploaded=await uploadCloudAccount(key,acc,secret.password);if(!uploaded)throw new Error('upload');saveAccountStore(store);updateCloudSyncUI('connected');",
    "const uploaded=await uploadCloudAccount(key,acc,secret.password);if(!uploaded)throw new Error('upload');markAccountCloudPushed();saveAccountStore(store);updateCloudSyncUI('connected');",
    "manual sync mark pushed",
)

rep(
    "function logoutAccount(){saveGame();uploadCurrentAccountToCloud().finally(()=>{clearSessionKey();",
    "function logoutAccount(){stopCloudAutoSync();saveGame();uploadCurrentAccountToCloud().finally(()=>{clearSessionKey();",
    "logout stop",
)

rep(
    "requestAnimationFrame(updateLayoutMode);uploadCurrentAccountToCloud();publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "requestAnimationFrame(updateLayoutMode);startCloudAutoSync();uploadCurrentAccountToCloud();publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "begin game start",
)

rep(
    "addEventListener('online',()=>{refreshCloudSyncNetworkStatus();});",
    "addEventListener('online',()=>{refreshCloudSyncNetworkStatus();startCloudAutoSync();});",
    "online restart",
)

rep(
    "acc.cloudSalt=payload.salt;updateCloudSyncUI('connected');return true;}catch(e){refreshCloudSyncDisplay();return false;}}async function applyCloudRecordToAccount",
    "acc.cloudSalt=payload.salt;markAccountCloudPushed();refreshCloudSyncDisplay();return true;}catch(e){refreshCloudSyncDisplay();return false;}}async function applyCloudRecordToAccount",
    "upload mark pushed",
)

path.write_text(s)
print("Patched cloud local-force 2s sync")
