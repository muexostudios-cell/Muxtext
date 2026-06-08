#!/usr/bin/env python3
"""v2.17.4: Fix v2.17.3 regression — getCloudSyncDetailText TDZ crash on boot."""
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


rep("GAME_VERSION='2.17.3'", "GAME_VERSION='2.17.4'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.3',date:'2026-06-08',summary:{zh:'v2.17.3 修復設定內雲端同步誤顯示「本地存檔」；已登入帳號正確顯示同步狀態。',en:'v2.17.3 fix cloud sync status in settings showing local-only when logged in.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.4',date:'2026-06-08',summary:{zh:'v2.17.4 修復 v2.17.3 啟動時雲端同步狀態初始化崩潰，設定畫面可正確顯示同步狀態。',en:'v2.17.4 fix v2.17.3 boot crash in cloud sync detail; settings show correct status.'}},{version:'2.17.3',date:'2026-06-08',summary:{zh:'v2.17.3 修復設定內雲端同步誤顯示「本地存檔」；已登入帳號正確顯示同步狀態。',en:'v2.17.3 fix cloud sync status in settings showing local-only when logged in.'}},",
    "hist",
)
rep("SAVE_VERSION=49", "SAVE_VERSION=50", "save")

rep(
    'logBalanceV2173:"[修復 v2.17.3] 設定內雲端同步狀態：已登入帳號不再誤顯示「本地存檔」。",logBalanceV2172:',
    'logBalanceV2174:"[修復 v2.17.4] 修復啟動時雲端同步狀態初始化錯誤，設定畫面可正確顯示已登入同步狀態。",logBalanceV2173:"[修復 v2.17.3] 設定內雲端同步狀態：已登入帳號不再誤顯示「本地存檔」。",logBalanceV2172:',
    "i18n zh log",
)
rep(
    'logBalanceV2173:"[Fix v2.17.3] Settings cloud sync status no longer shows local-only when logged in.",logBalanceV2172:',
    'logBalanceV2174:"[Fix v2.17.4] Fix cloud sync status init crash on boot; settings show logged-in sync state.",logBalanceV2173:"[Fix v2.17.3] Settings cloud sync status no longer shows local-only when logged in.",logBalanceV2172:',
    "i18n en log",
)

rep(
    "logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'))",
    "logInfo(t('logBalanceV2174'));logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'))",
    "boot log",
)

OLD_DETAIL = (
    "function getCloudSyncDetailText(){const st=cloudSyncState;const acc=getActiveAccount();"
    "const name=(acc&&(acc.displayName||acc.username))||'--';"
    "const lv=(typeof player!=='undefined'&&player)?Math.floor(Number(player.level)||1):1;"
    "if(st==='syncing')return t('cloudSyncDetailSyncing');if(st==='local')return t('cloudSyncDetailLocal');"
    "if(st==='relogin')return t('cloudSyncDetailRelogin',name);"
    "if(st==='offline'){if(hasCloudAccountLoggedIn()&&!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));"
    "return t('cloudSyncDetailOffline');}if(st==='pending')return t('cloudSyncDetailLocalPending',name);"
    "if(st==='synced'||st==='connected'){if(!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));"
    "return st==='synced'?t('cloudSyncDetailSynced',name,String(lv)):t('cloudSyncDetailConnected',name,String(lv));}return '';}"
)
NEW_DETAIL = (
    "function safePlayerLevelForCloudSync(){try{if(player)return Math.floor(Number(player.level)||1);}catch(e){}return 1;}"
    "function getCloudSyncDetailText(){const st=cloudSyncState;"
    "if(st==='syncing')return t('cloudSyncDetailSyncing');if(st==='local')return t('cloudSyncDetailLocal');"
    "const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';"
    "const lv=safePlayerLevelForCloudSync();"
    "if(st==='relogin')return t('cloudSyncDetailRelogin',name);"
    "if(st==='offline'){if(hasCloudAccountLoggedIn()&&!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));"
    "return t('cloudSyncDetailOffline');}if(st==='pending')return t('cloudSyncDetailLocalPending',name);"
    "if(st==='synced'||st==='connected'){if(!gunPeerConnected)return t('cloudSyncDetailRelayPending',name,String(lv));"
    "return st==='synced'?t('cloudSyncDetailSynced',name,String(lv)):t('cloudSyncDetailConnected',name,String(lv));}return '';}"
)
rep(OLD_DETAIL, NEW_DETAIL, "detail text")

rep(
    "if(typeof updateCloudSyncUI==='function')updateCloudSyncUI(cloudSyncState);",
    "if(typeof refreshCloudSyncDisplay==='function')refreshCloudSyncDisplay();",
    "apply account lang refresh",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (v2.17.4 cloud sync boot fix)")
