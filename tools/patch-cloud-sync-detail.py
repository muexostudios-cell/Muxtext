#!/usr/bin/env python3
"""Add contextual detail text under cloud sync status in settings."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:220]}")
    s = s.replace(old, new, 1)


rep(
    '<div class="setting-row"><label id="label-cloud-sync">雲端同步</label><span id="cloud-sync-status" class="setting-val">--</span></div>',
    '<div class="setting-row" id="cloud-sync-row"><label id="label-cloud-sync">雲端同步</label><div class="cloud-sync-status-wrap"><span id="cloud-sync-status" class="setting-val">--</span><div id="cloud-sync-detail" class="cloud-sync-detail" aria-live="polite"></div></div></div>',
    "html cloud sync row",
)

rep(
    ".setting-val{margin-left:.5rem;color:#fff;min-width:3rem;text-align:right}",
    ".setting-val{margin-left:.5rem;color:#fff;min-width:3rem;text-align:right}#cloud-sync-row{align-items:flex-start}.cloud-sync-status-wrap{display:flex;flex-direction:column;align-items:flex-end;margin-left:.5rem;max-width:11rem;min-width:3rem}#cloud-sync-detail{font-size:.5rem;line-height:1.35;color:#888;margin-top:.15rem;white-space:normal;word-break:break-word;text-align:right}#cloud-sync-detail.syncing{color:#fa0}#cloud-sync-detail.offline{color:#f84}#cloud-sync-detail.connected{color:#6a8}",
    "css cloud sync detail",
)

rep(
    'cloudSyncRelayBlocked:"雲端中繼無法連線（網路或代理可能被阻擋）",accountErrorCloudExists:"此帳號已在雲端註冊"',
    'cloudSyncRelayBlocked:"雲端中繼無法連線（網路或代理可能被阻擋）",cloudSyncDetailLocal:"尚未登入雲端帳號，進度僅儲存於本機瀏覽器。",cloudSyncDetailOffline:"裝置已離線，無法同步；恢復網路後會自動上傳。",cloudSyncDetailSyncing:"正在端到端加密並上傳進度至雲端…",cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 雲端中繼已連線，變更會自動同步",cloudSyncDetailRelayPending:"帳號 {0} · Lv.{1} · 等待雲端中繼連線（網路或代理可能受阻）",accountErrorCloudExists:"此帳號已在雲端註冊"',
    "i18n zh detail",
)

rep(
    'cloudSyncRelayBlocked:"Cloud relay unreachable (network or proxy may be blocked)",accountErrorCloudExists:"Account already registered on cloud"',
    'cloudSyncRelayBlocked:"Cloud relay unreachable (network or proxy may be blocked)",cloudSyncDetailLocal:"Not signed in. Progress is stored only in this browser.",cloudSyncDetailOffline:"Device offline. Sync paused; uploads resume when online.",cloudSyncDetailSyncing:"Encrypting and uploading progress to cloud…",cloudSyncDetailConnected:"Account {0} · Lv.{1} · Cloud relay connected; changes sync automatically",cloudSyncDetailRelayPending:"Account {0} · Lv.{1} · Waiting for cloud relay (network or proxy may be blocked)",accountErrorCloudExists:"Account already registered on cloud"',
    "i18n en detail",
)

rep(
    "function markGunRelayConnected(){if(gunPeerConnected)return;gunPeerConnected=true;gunPeerWaiters.splice(0).forEach(fn=>fn(true));}",
    "function markGunRelayConnected(){if(gunPeerConnected)return;gunPeerConnected=true;gunPeerWaiters.splice(0).forEach(fn=>fn(true));if(typeof updateCloudSyncDetail==='function')updateCloudSyncDetail();}",
    "relay detail refresh",
)

rep(
    "function updateCloudSyncUI(state){cloudSyncState=normalizeCloudSyncDisplayState(state);const el=document.getElementById('cloud-sync-status');if(!el)return;const map={connected:'cloudSyncConnected',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline',local:'cloudSyncLocal'};el.textContent=t(map[cloudSyncState]||'cloudSyncLocal');el.className='setting-val '+cloudSyncState;}",
    "function getCloudSyncDetailText(){const st=cloudSyncState;if(st==='syncing')return t('cloudSyncDetailSyncing');if(st==='local')return t('cloudSyncDetailLocal');if(st==='offline')return t('cloudSyncDetailOffline');if(st==='connected'){const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';const lv=(typeof player!=='undefined'&&player)?Math.floor(Number(player.level)||1):1;return gunPeerConnected?t('cloudSyncDetailConnected',name,String(lv)):t('cloudSyncDetailRelayPending',name,String(lv));}return '';}function updateCloudSyncDetail(){const el=document.getElementById('cloud-sync-detail');if(!el)return;const text=getCloudSyncDetailText();el.textContent=text;el.className='cloud-sync-detail'+(cloudSyncState?' '+cloudSyncState:'');el.style.display=text?'block':'none';}function updateCloudSyncUI(state){cloudSyncState=normalizeCloudSyncDisplayState(state);const el=document.getElementById('cloud-sync-status');if(!el)return;const map={connected:'cloudSyncConnected',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline',local:'cloudSyncLocal'};el.textContent=t(map[cloudSyncState]||'cloudSyncLocal');el.className='setting-val '+cloudSyncState;updateCloudSyncDetail();}",
    "cloud sync detail ui",
)

path.write_text(s)
print("Patched cloud sync detail display")
