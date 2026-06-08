#!/usr/bin/env python3
"""Change cloud account upload from 30s debounce to 2s interval auto-sync."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:240]}")
    s = s.replace(old, new, 1)


rep(
    "cloudUploadTimeout=null,cloudSyncInProgress=false",
    "CLOUD_AUTO_SYNC_MS=2000,cloudUploadTimeout=null,cloudUploadInterval=null,cloudUploadBusy=false,cloudSyncInProgress=false",
    "cloud sync interval vars",
)

rep(
    "function scheduleCloudUpload(){if(!restoreSessionAccountSecret())return;if(cloudUploadTimeout)clearTimeout(cloudUploadTimeout);cloudUploadTimeout=setTimeout(()=>{uploadCurrentAccountToCloud();cloudUploadTimeout=null;},30000);}",
    "function stopCloudAutoSync(){if(cloudUploadInterval){clearInterval(cloudUploadInterval);cloudUploadInterval=null;}if(cloudUploadTimeout){clearTimeout(cloudUploadTimeout);cloudUploadTimeout=null;}}function startCloudAutoSync(){if(!restoreSessionAccountSecret()){stopCloudAutoSync();return;}if(cloudUploadInterval)return;cloudUploadInterval=setInterval(()=>tickCloudAutoSync(),CLOUD_AUTO_SYNC_MS);tickCloudAutoSync();}function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession())return;if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(typeof saveGame==='function')saveGame();uploadCurrentAccountToCloud({silent:true});}function scheduleCloudUpload(){startCloudAutoSync();}",
    "interval auto sync",
)

rep(
    "async function uploadCurrentAccountToCloud(){const key=getSessionKey();const secret=restoreSessionAccountSecret();if(!key||!secret||secret.key!==key)return false;if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');showNetworkOverlay();return false;}const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;updateCloudSyncUI('syncing');const ok=await uploadCloudAccount(key,acc,secret.password);if(ok){saveAccountStore(store);publishLeaderboardEntry(true);}else{refreshCloudSyncDisplay();showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}return ok;}",
    "async function uploadCurrentAccountToCloud(opts){const silent=!!(opts&&opts.silent);if(cloudUploadBusy)return false;const key=getSessionKey();const secret=restoreSessionAccountSecret();if(!key||!secret||secret.key!==key)return false;if(typeof navigator!=='undefined'&&navigator.onLine===false){if(!silent){updateCloudSyncUI('offline');showNetworkOverlay();}return false;}const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;cloudUploadBusy=true;if(!silent)updateCloudSyncUI('syncing');let ok=false;try{ok=await uploadCloudAccount(key,acc,secret.password);if(ok){saveAccountStore(store);publishLeaderboardEntry(true);if(!silent)refreshCloudSyncDisplay();}else if(!silent){refreshCloudSyncDisplay();showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}}finally{cloudUploadBusy=false;if(silent)refreshCloudSyncDisplay();}return ok;}",
    "silent background upload",
)

rep(
    "function logoutAccount(){saveGame();uploadCurrentAccountToCloud().finally(()=>{clearSessionKey();",
    "function logoutAccount(){stopCloudAutoSync();saveGame();uploadCurrentAccountToCloud().finally(()=>{clearSessionKey();",
    "logout stop sync",
)

rep(
    "requestAnimationFrame(updateLayoutMode);uploadCurrentAccountToCloud();publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "requestAnimationFrame(updateLayoutMode);startCloudAutoSync();uploadCurrentAccountToCloud();publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "begin game start sync",
)

rep(
    'cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 雲端中繼已連線，變更會自動同步"',
    'cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 雲端中繼已連線，每 2 秒自動同步"',
    "i18n zh 2s",
)

rep(
    "cloudSyncDetailConnected:\"Account {0} · Lv.{1} · Cloud relay connected; changes sync automatically\"",
    "cloudSyncDetailConnected:\"Account {0} · Lv.{1} · Cloud relay connected; auto-sync every 2s\"",
    "i18n en 2s",
)

rep(
    "addEventListener('online',()=>{refreshCloudSyncNetworkStatus();});",
    "addEventListener('online',()=>{refreshCloudSyncNetworkStatus();startCloudAutoSync();});",
    "online restart sync",
)

path.write_text(s)
print("Patched cloud auto-sync 2s interval")
