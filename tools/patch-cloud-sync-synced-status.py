#!/usr/bin/env python3
"""Fix cloud sync stuck on syncing; show completed status after sync."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:280]}")
    s = s.replace(old, new, 1)


rep('cloudSyncSynced:"已同步"', 'cloudSyncSynced:"雲端同步已完成"', "zh synced label")
rep(
    'cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 已連線，每 2 秒自動上傳最新進度",cloudSyncDetailRelayPending:',
    'cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 已連線，每 2 秒自動上傳最新進度",cloudSyncDetailSynced:"帳號 {0} · Lv.{1} · 雲端同步已完成，每 2 秒自動檢查更新",cloudSyncDetailRelayPending:',
    "zh synced detail",
)
rep('cloudSyncSynced:"Synced"', 'cloudSyncSynced:"Cloud sync completed"', "en synced label")
rep(
    'cloudSyncDetailConnected:"Account {0} · Lv.{1} · connected; auto-upload every 2s",cloudSyncDetailRelayPending:',
    'cloudSyncDetailConnected:"Account {0} · Lv.{1} · connected; auto-upload every 2s",cloudSyncDetailSynced:"Account {0} · Lv.{1} · Cloud sync completed; auto-check every 2s",cloudSyncDetailRelayPending:',
    "en synced detail",
)
rep(
    "#cloud-sync-detail.connected{color:#6a8}",
    "#cloud-sync-detail.connected,#cloud-sync-detail.synced{color:#6a8}.setting-val.synced{color:#6a8}",
    "css synced",
)
rep(
    "function normalizeCloudSyncDisplayState(state){if(state==='synced'||state==='online')return'connected';if(state==='error')return'offline';return state||'local';}function hasActiveCloudSession(){",
    "function normalizeCloudSyncDisplayState(state){if(state==='connected'||state==='online')return'synced';if(state==='error')return'offline';return state||'local';}function resolveCloudSyncDisplayState(){if(cloudUploadBusy||cloudSyncInProgress)return'syncing';if(!hasActiveCloudSession())return'local';if(typeof navigator!=='undefined'&&navigator.onLine===false)return'offline';if(accountNeedsCloudPush())return'local';return'synced';}function hasActiveCloudSession(){",
    "resolve state",
)
rep(
    "function refreshCloudSyncDisplay(){if(cloudSyncState==='syncing'){updateCloudSyncDetail();return;}if(!hasActiveCloudSession()){updateCloudSyncUI('local');return;}if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');return;}if(accountNeedsCloudPush()){updateCloudSyncUI('local');return;}updateCloudSyncUI('connected');}function refreshCloudSyncNetworkStatus(){if(cloudSyncState==='syncing'){updateCloudSyncDetail();return;}if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');return;}refreshCloudSyncDisplay();}",
    "function refreshCloudSyncDisplay(){updateCloudSyncUI(resolveCloudSyncDisplayState());}function refreshCloudSyncNetworkStatus(){if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');return;}refreshCloudSyncDisplay();}",
    "refresh display",
)
rep(
    "if(st==='offline')return t('cloudSyncDetailOffline');if(st==='connected'){const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';const lv=(typeof player!=='undefined'&&player)?Math.floor(Number(player.level)||1):1;return gunPeerConnected?t('cloudSyncDetailConnected',name,String(lv)):t('cloudSyncDetailRelayPending',name,String(lv));}return '';}",
    "if(st==='offline')return t('cloudSyncDetailOffline');if(st==='synced'||st==='connected'){const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';const lv=(typeof player!=='undefined'&&player)?Math.floor(Number(player.level)||1):1;if(!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));return st==='synced'?t('cloudSyncDetailSynced',name,String(lv)):t('cloudSyncDetailConnected',name,String(lv));}return '';}",
    "detail synced",
)
rep(
    "const map={connected:'cloudSyncConnected',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline',local:'cloudSyncLocal'};",
    "const map={synced:'cloudSyncSynced',connected:'cloudSyncSynced',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline',local:'cloudSyncLocal'};",
    "ui map synced",
)
rep(
    "}finally{cloudUploadBusy=false;if(silent)refreshCloudSyncDisplay();}return ok;}async function manualCloudSync(){",
    "}finally{cloudUploadBusy=false;refreshCloudSyncDisplay();}return ok;}async function manualCloudSync(){",
    "upload finally refresh",
)
rep(
    "}finally{cloudSyncInProgress=false;}}function accountNeedsCloudPush(){",
    "}finally{cloudSyncInProgress=false;refreshCloudSyncDisplay();}}function accountNeedsCloudPush(){",
    "manual finally refresh",
)

path.write_text(s)
print("Patched cloud sync synced status")
