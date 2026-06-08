#!/usr/bin/env python3
"""Fix cloud sync falsely showing 已離線 when session is valid or Gun relay works."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:200]}")
    s = s.replace(old, new, 1)


rep("cloudSyncState='offline'", "cloudSyncState='local'", "default state")

rep(
    'cloudSyncLabel:"雲端同步",cloudSyncConnected:"已連線"',
    'cloudSyncLabel:"雲端同步",cloudSyncLocal:"本地存檔",cloudSyncConnected:"已連線"',
    "i18n zh local",
)
rep(
    'cloudSyncLabel:"Cloud sync",cloudSyncConnected:"Connected"',
    'cloudSyncLabel:"Cloud sync",cloudSyncLocal:"Local save",cloudSyncConnected:"Connected"',
    "i18n en local",
)

rep(
    "gun.on('hi',()=>{gunPeerConnected=true;gunPeerWaiters.splice(0).forEach(fn=>fn(true));});}",
    "gun.on('hi',()=>{markGunRelayConnected();});}function markGunRelayConnected(){if(gunPeerConnected)return;gunPeerConnected=true;gunPeerWaiters.splice(0).forEach(fn=>fn(true));}",
    "mark relay",
)

rep(
    "gun.get(CLOUD_ROOT).get('accounts').get(key).once(data=>{if(done)return;done=true;clearTimeout(timer);resolve(data&&data.passHash?data:null);});",
    "gun.get(CLOUD_ROOT).get('accounts').get(key).once(data=>{if(done)return;done=true;clearTimeout(timer);markGunRelayConnected();resolve(data&&data.passHash?data:null);});",
    "fetch mark relay",
)

rep(
    "if(ack&&ack.err)reject(ack.err);else resolve(true);});",
    "if(ack&&ack.err)reject(ack.err);else{markGunRelayConnected();resolve(true);}});",
    "put mark relay",
)

rep(
    "function normalizeCloudSyncDisplayState(state){if(state==='synced'||state==='online')return'connected';if(state==='error')return'offline';return state||'offline';}function refreshCloudSyncNetworkStatus(){if(cloudSyncState==='syncing')return;if(typeof navigator!=='undefined'&&navigator.onLine===false)updateCloudSyncUI('offline');}function updateCloudSyncUI(state){cloudSyncState=normalizeCloudSyncDisplayState(state);const el=document.getElementById('cloud-sync-status');if(!el)return;const map={connected:'cloudSyncConnected',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline'};el.textContent=t(map[cloudSyncState]||'cloudSyncOffline');el.className='setting-val '+cloudSyncState;}",
    "function normalizeCloudSyncDisplayState(state){if(state==='synced'||state==='online')return'connected';if(state==='error')return'offline';return state||'local';}function hasActiveCloudSession(){const key=getSessionKey();const secret=restoreSessionAccountSecret();return !!(key&&getActiveAccount()&&secret&&secret.key===key);}function refreshCloudSyncDisplay(){if(cloudSyncState==='syncing')return;if(!hasActiveCloudSession()){updateCloudSyncUI('local');return;}if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');return;}updateCloudSyncUI('connected');}function refreshCloudSyncNetworkStatus(){if(cloudSyncState==='syncing')return;if(typeof navigator!=='undefined'&&navigator.onLine===false){updateCloudSyncUI('offline');return;}refreshCloudSyncDisplay();}function updateCloudSyncUI(state){cloudSyncState=normalizeCloudSyncDisplayState(state);const el=document.getElementById('cloud-sync-status');if(!el)return;const map={connected:'cloudSyncConnected',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline',local:'cloudSyncLocal'};el.textContent=t(map[cloudSyncState]||'cloudSyncLocal');el.className='setting-val '+cloudSyncState;}",
    "cloud sync ui",
)

rep(
    "function beginGameAfterAccount(pulled){hideAccountOverlay();loadAccountProfile();initGame();",
    "function beginGameAfterAccount(pulled){hideAccountOverlay();refreshCloudSyncDisplay();loadAccountProfile();initGame();",
    "begin after account",
)

rep(
    "beginGameAfterAccount(false);refreshCloudSyncNetworkStatus();}else{showAccountOverlay();}",
    "beginGameAfterAccount(false);refreshCloudSyncDisplay();}else{showAccountOverlay();refreshCloudSyncDisplay();}",
    "continue boot",
)

rep(
    "const ok=await ensureGunRelayReady(10000);if(!ok){updateCloudSyncUI('offline');showNetworkOverlay(t('cloudSyncRelayBlocked'));",
    "const ok=await ensureGunRelayReady(10000);if(!ok){refreshCloudSyncDisplay();showNetworkOverlay(t('cloudSyncRelayBlocked'));",
    "try reconnect fail",
)

rep(
    "}else{updateCloudSyncUI('offline');showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}return ok;}",
    "}else{refreshCloudSyncDisplay();showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}return ok;}",
    "upload fail ui",
)

rep(
    'const cloudTxt=(document.getElementById(\'cloud-sync-status\')?.textContent||\'\').toLowerCase();if(cloudTxt.includes(\'offline\')||cloudTxt.includes(\'中斷\')||cloudTxt.includes(\'失敗\'))signals.add(\'cloud_sync_offline\');',
    "const cloudSt=document.getElementById('cloud-sync-status');if(cloudSt&&cloudSt.classList.contains('offline'))signals.add('cloud_sync_offline');",
    "bug detect cloud",
)

rep(
    "}catch(e){updateCloudSyncUI('offline');return false;}}async function applyCloudRecordToAccount",
    "}catch(e){refreshCloudSyncDisplay();return false;}}async function applyCloudRecordToAccount",
    "upload cloud catch",
)

rep(
    "if(!(await ensureGunRelayReady(10000))){updateCloudSyncUI('offline');showCloudSyncFeedback(t('cloudSyncRelayBlocked'),'error');",
    "if(!(await ensureGunRelayReady(10000))){refreshCloudSyncDisplay();showCloudSyncFeedback(t('cloudSyncRelayBlocked'),'error');",
    "manual sync relay",
)

path.write_text(s)
print("Patched cloud sync offline display fix")
