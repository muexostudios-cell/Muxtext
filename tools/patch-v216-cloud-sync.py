#!/usr/bin/env python3
"""v2.16.0: cloud sync every 2s, force local upload, settings live status — version release."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:280]}")
    s = s.replace(old, new, 1)


rep("GAME_VERSION='2.15.0'", "GAME_VERSION='2.16.0'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.15.0'",
    "GAME_VERSION_HISTORY=[{version:'2.16.0',date:'2026-06-08',summary:{zh:'v2.16.0 雲端同步強化：每 2 秒自動同步、本地進度強制上傳、設定內狀態說明即時更新；修復離線誤報。',en:'v2.16.0 cloud sync: auto-sync every 2s, force-upload local saves, live settings status; fix false offline.'}},{version:'2.15.0'",
    "hist",
)
rep("SAVE_VERSION=44", "SAVE_VERSION=45", "save")

rep(
    'logBalanceV215:"[更新 v2.15] Bug 生命週期：設定可查看狀態與回報；客戶端會自動偵測常見問題。",',
    'logBalanceV216:"[更新 v2.16] 雲端同步：登入後每 2 秒自動上傳；本地存檔待同步時強制上傳；設定內可查看即時狀態說明。",logBalanceV215:"[更新 v2.15] Bug 生命週期：設定可查看狀態與回報；客戶端會自動偵測常見問題。",',
    "i18n zh log",
)
rep(
    'logBalanceV215:"[Update v2.15] Bug lifecycle: check status and report in Settings; common issues are auto-detected.",',
    'logBalanceV216:"[Update v2.16] Cloud sync: auto-upload every 2s when logged in; force push pending local saves; live status in Settings.",logBalanceV215:"[Update v2.15] Bug lifecycle: check status and report in Settings; common issues are auto-detected.",',
    "i18n en log",
)

rep(
    "function migrateSave(data){if(data.version<44){data._balanceV215Notice=true;data.version=44;}",
    "function migrateSave(data){if(data.version<45){data._balanceV216Notice=true;data.version=45;}if(data.version<44){data._balanceV215Notice=true;data.version=44;}",
    "migrate v216",
)
rep(
    "const _balanceV215Notice=!!data._balanceV215Notice;delete data._balanceV215Notice;if(data.autoHerbSettings)",
    "const _balanceV215Notice=!!data._balanceV215Notice;delete data._balanceV215Notice;const _balanceV216Notice=!!data._balanceV216Notice;delete data._balanceV216Notice;if(data.autoHerbSettings)",
    "migrate var",
)
rep(
    "if(_balanceV215Notice)logInfo(t('logBalanceV215'));leaderboardTrackedLevel=-1;",
    "if(_balanceV215Notice)logInfo(t('logBalanceV215'));if(_balanceV216Notice)logInfo(t('logBalanceV216'));leaderboardTrackedLevel=-1;",
    "migrate log",
)

path.write_text(s)
print("Patched index.html for v2.16.0 cloud sync release")
