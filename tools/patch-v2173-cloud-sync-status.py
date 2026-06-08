#!/usr/bin/env python3
"""v2.17.3: Fix settings cloud sync showing 本地存檔 when logged in."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")


def rep(old, new, label, count=1):
    global text
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:220]}")
    text = text.replace(old, new, 1)


rep("GAME_VERSION='2.17.2'", "GAME_VERSION='2.17.3'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.2',date:'2026-06-08',summary:{zh:'v2.17.2 伺服器全面檢查：Bug 監測本地目錄備援、停止付款雜訊回報、Gun 節點優化。',en:'v2.17.2 server audit: local bug catalog fallback, payment noise filter, Gun peers.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.3',date:'2026-06-08',summary:{zh:'v2.17.3 修復設定內雲端同步誤顯示「本地存檔」；已登入帳號正確顯示同步狀態。',en:'v2.17.3 fix cloud sync status in settings showing local-only when logged in.'}},{version:'2.17.2',date:'2026-06-08',summary:{zh:'v2.17.2 伺服器全面檢查：Bug 監測本地目錄備援、停止付款雜訊回報、Gun 節點優化。',en:'v2.17.2 server audit: local bug catalog fallback, payment noise filter, Gun peers.'}},",
    "hist",
)
rep("SAVE_VERSION=48", "SAVE_VERSION=49", "save")

rep(
    'cloudSyncLocal:"本地存檔",cloudSyncConnected:"已連線",',
    'cloudSyncLocal:"本地存檔",cloudSyncPending:"待上傳",cloudSyncRelogin:"請重新登入",cloudSyncConnected:"已連線",',
    "i18n zh status",
)
rep(
    'cloudSyncDetailLocal:"未登入雲端帳號。進度僅存於本機；登入後每 2 秒自動同步（端到端加密）。",',
    'cloudSyncDetailLocal:"未登入雲端帳號。進度僅存於本機；登入後每 2 秒自動同步（端到端加密）。",cloudSyncDetailRelogin:"帳號 {0} · 請重新登入以啟用雲端同步",',
    "i18n zh detail",
)

rep(
    'cloudSyncLocal:"Local save",cloudSyncConnected:"Connected",',
    'cloudSyncLocal:"Local save",cloudSyncPending:"Pending upload",cloudSyncRelogin:"Re-login",cloudSyncConnected:"Connected",',
    "i18n en status",
)
rep(
    'cloudSyncDetailLocal:"Not signed in. Progress stays on this device; after login, auto-sync every 2s (E2E encrypted).",',
    'cloudSyncDetailLocal:"Not signed in. Progress stays on this device; after login, auto-sync every 2s (E2E encrypted).",cloudSyncDetailRelogin:"Account {0} · Re-login to enable cloud sync",',
    "i18n en detail",
)

rep(
    "logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'))",
    "logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'))",
    "boot log",
)

rep(
    'logBalanceV2172:"[修復 v2.17.2] 伺服器全面檢查：Bug 監測本地修復目錄、過濾付款雜訊回報、優化 Gun 節點。",logBalanceV2171:',
    'logBalanceV2173:"[修復 v2.17.3] 設定內雲端同步狀態：已登入帳號不再誤顯示「本地存檔」。",logBalanceV2172:"[修復 v2.17.2] 伺服器全面檢查：Bug 監測本地修復目錄、過濾付款雜訊回報、優化 Gun 節點。",logBalanceV2171:',
    "i18n zh log",
)
rep(
    'logBalanceV2172:"[Fix v2.17.2] Server audit: local bug-fix catalog, payment noise filter, Gun peers.",logBalanceV2171:',
    'logBalanceV2173:"[Fix v2.17.3] Settings cloud sync status no longer shows local-only when logged in.",logBalanceV2172:"[Fix v2.17.2] Server audit: local bug-fix catalog, payment noise filter, Gun peers.",logBalanceV2171:',
    "i18n en log",
)

rep(
    "function resolveCloudSyncDisplayState(){if(cloudUploadBusy||cloudSyncInProgress)return'syncing';if(!hasActiveCloudSession())return'local';if(typeof navigator!=='undefined'&&navigator.onLine===false)return'offline';if(!gunPeerConnected)return'offline';if(accountNeedsCloudPush())return'local';return'synced';}",
    "function hasCloudAccountLoggedIn(){return !!(getSessionKey()&&getActiveAccount());}function resolveCloudSyncDisplayState(){if(cloudUploadBusy||cloudSyncInProgress)return'syncing';if(!hasCloudAccountLoggedIn())return'local';if(!hasActiveCloudSession())return'relogin';if(typeof navigator!=='undefined'&&navigator.onLine===false)return'offline';if(!gunPeerConnected)return'offline';if(accountNeedsCloudPush())return'pending';return'synced';}",
    "resolve state",
)

rep(
    "function getCloudSyncDetailText(){const st=cloudSyncState;if(st==='syncing')return t('cloudSyncDetailSyncing');if(st==='local'){if(hasActiveCloudSession()){const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';return t('cloudSyncDetailLocalPending',name);}return t('cloudSyncDetailLocal');}if(st==='offline')return t('cloudSyncDetailOffline');if(st==='synced'||st==='connected'){const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';const lv=(typeof player!=='undefined'&&player)?Math.floor(Number(player.level)||1):1;if(!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));return st==='synced'?t('cloudSyncDetailSynced',name,String(lv)):t('cloudSyncDetailConnected',name,String(lv));}return '';}",
    "function getCloudSyncDetailText(){const st=cloudSyncState;const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';const lv=(typeof player!=='undefined'&&player)?Math.floor(Number(player.level)||1):1;if(st==='syncing')return t('cloudSyncDetailSyncing');if(st==='local')return t('cloudSyncDetailLocal');if(st==='relogin')return t('cloudSyncDetailRelogin',name);if(st==='offline'){if(hasCloudAccountLoggedIn()&&!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));return t('cloudSyncDetailOffline');}if(st==='pending')return t('cloudSyncDetailLocalPending',name);if(st==='synced'||st==='connected'){if(!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));return st==='synced'?t('cloudSyncDetailSynced',name,String(lv)):t('cloudSyncDetailConnected',name,String(lv));}return '';}",
    "detail text",
)

rep(
    "const map={synced:'cloudSyncSynced',connected:'cloudSyncSynced',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline',local:'cloudSyncLocal'};",
    "const map={synced:'cloudSyncSynced',connected:'cloudSyncSynced',syncing:'cloudSyncSyncing',offline:'cloudSyncOffline',local:'cloudSyncLocal',pending:'cloudSyncPending',relogin:'cloudSyncRelogin'};",
    "ui map",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (v2.17.3 cloud sync status)")
