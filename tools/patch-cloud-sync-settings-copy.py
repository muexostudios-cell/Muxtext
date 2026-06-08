#!/usr/bin/env python3
"""Update cloud sync settings copy and refresh UI every 2s while settings open."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:280]}")
    s = s.replace(old, new, 1)


rep(
    'accountDesc:"登入或註冊雲端帳號，進度可跨裝置同步（端到端加密）",accountCloudHint:"雲端帳號服務 · 需網路連線"',
    'accountDesc:"登入或註冊雲端帳號，進度每 2 秒自動同步至雲端（端到端加密、跨裝置）。",accountCloudHint:"每 2 秒自動同步 · 端到端加密 · 需網路"',
    "zh account copy",
)

rep(
    'accountDesc:"Cloud account — sync progress across devices (E2E encrypted)",accountCloudHint:"Cloud account service · network required"',
    'accountDesc:"Cloud account — progress auto-syncs every 2s (E2E encrypted, cross-device).",accountCloudHint:"Auto-sync every 2s · E2E encrypted · network required"',
    "en account copy",
)

rep(
    'cloudSyncDetailLocal:"尚未登入雲端帳號，進度僅儲存於本機瀏覽器。",cloudSyncDetailLocalPending:"本機進度尚未同步至雲端，每 2 秒強制上傳…",cloudSyncDetailOffline:"裝置已離線，無法同步；恢復網路後會自動上傳。",cloudSyncDetailSyncing:"正在端到端加密並上傳進度至雲端…",cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 雲端中繼已連線，每 2 秒自動同步",cloudSyncDetailRelayPending:"帳號 {0} · Lv.{1} · 等待雲端中繼連線（網路或代理可能受阻）"',
    'cloudSyncDetailLocal:"未登入雲端帳號。進度僅存於本機；登入後每 2 秒自動同步（端到端加密）。",cloudSyncDetailLocalPending:"帳號 {0} · 本機進度待上傳。每 2 秒檢查並強制同步至雲端…",cloudSyncDetailOffline:"裝置已離線，同步暫停。恢復網路後每 2 秒自動上傳。",cloudSyncDetailSyncing:"正在端到端加密並上傳進度至雲端伺服器…",cloudSyncDetailConnected:"帳號 {0} · Lv.{1} · 已連線，每 2 秒自動上傳最新進度",cloudSyncDetailRelayPending:"帳號 {0} · Lv.{1} · 雲端中繼連線中；連線後每 2 秒自動同步"',
    "zh detail copy",
)

rep(
    'cloudSyncDetailLocal:"Not signed in. Progress is stored only in this browser.",cloudSyncDetailLocalPending:"Local progress not on cloud yet; force upload every 2s…",cloudSyncDetailOffline:"Device offline. Sync paused; uploads resume when online.",cloudSyncDetailSyncing:"Encrypting and uploading progress to cloud…",cloudSyncDetailConnected:"Account {0} · Lv.{1} · Cloud relay connected; auto-sync every 2s",cloudSyncDetailRelayPending:"Account {0} · Lv.{1} · Waiting for cloud relay (network or proxy may be blocked)"',
    'cloudSyncDetailLocal:"Not signed in. Progress stays on this device; after login, auto-sync every 2s (E2E encrypted).",cloudSyncDetailLocalPending:"Account {0} · local save pending upload. Checked and force-synced every 2s…",cloudSyncDetailOffline:"Device offline. Sync paused; auto-upload every 2s when back online.",cloudSyncDetailSyncing:"Encrypting and uploading progress to cloud…",cloudSyncDetailConnected:"Account {0} · Lv.{1} · connected; auto-upload every 2s",cloudSyncDetailRelayPending:"Account {0} · Lv.{1} · cloud relay connecting; syncs every 2s when ready"',
    "en detail copy",
)

rep(
    "if(st==='local')return hasActiveCloudSession()?t('cloudSyncDetailLocalPending'):t('cloudSyncDetailLocal');",
    "if(st==='local'){if(hasActiveCloudSession()){const acc=getActiveAccount();const name=(acc&&(acc.displayName||acc.username))||'--';return t('cloudSyncDetailLocalPending',name);}return t('cloudSyncDetailLocal');}",
    "detail local pending name",
)

rep(
    "function refreshCloudSyncOnSettingsOpen(){refreshCloudSyncNetworkStatus();updateCloudSyncDetail();}",
    "let cloudSyncSettingsTimer=null;function stopCloudSyncSettingsRefresh(){if(cloudSyncSettingsTimer){clearInterval(cloudSyncSettingsTimer);cloudSyncSettingsTimer=null;}}function startCloudSyncSettingsRefresh(){stopCloudSyncSettingsRefresh();refreshCloudSyncOnSettingsOpen();cloudSyncSettingsTimer=setInterval(()=>refreshCloudSyncOnSettingsOpen(),CLOUD_AUTO_SYNC_MS);}function refreshCloudSyncOnSettingsOpen(){refreshCloudSyncNetworkStatus();updateCloudSyncDetail();}",
    "settings 2s refresh timer",
)

rep(
    "syncAccountProfileToUI();refreshCloudSyncOnSettingsOpen();clearCloudSyncFeedback();settingsOverlayEl.style.display='flex';",
    "syncAccountProfileToUI();startCloudSyncSettingsRefresh();clearCloudSyncFeedback();settingsOverlayEl.style.display='flex';",
    "settings open timer",
)

rep(
    "document.getElementById('btn-close-settings').addEventListener('click',()=>{settingsOverlayEl.style.display='none';});",
    "document.getElementById('btn-close-settings').addEventListener('click',()=>{stopCloudSyncSettingsRefresh();settingsOverlayEl.style.display='none';});",
    "settings close stop timer",
)

rep(
    "settingsOverlayEl.addEventListener('click',e=>{if(e.target===settingsOverlayEl)settingsOverlayEl.style.display='none';});",
    "settingsOverlayEl.addEventListener('click',e=>{if(e.target===settingsOverlayEl){stopCloudSyncSettingsRefresh();settingsOverlayEl.style.display='none';}});",
    "settings backdrop close stop timer",
)

rep(
    '首次進入會看到「MTO MUX TEXT ONLINE 帳號」視窗，可「登入」或「註冊」雲端帳號。雲端存檔端到端加密，可跨裝置同步。',
    '首次進入會看到「MTO MUX TEXT ONLINE 帳號」視窗，可「登入」或「註冊」雲端帳號。雲端存檔端到端加密，登入後每 2 秒自動同步、可跨裝置。',
    "tutorial zh account",
)

rep(
    '狀態欄「設定」可調整介面縮放、文字大小、語言，查看帳號與雲端同步，並開啟「新手教學」與「歷史遊戲版本」。',
    '狀態欄「設定」可調整介面縮放、文字大小、語言；「雲端同步」顯示狀態與說明（開啟設定時每 2 秒更新），並可查看帳號、新手教學與歷史版本。',
    "tutorial zh settings",
)

rep(
    "On first launch you see the MTO account overlay—register or log in for encrypted cloud saves across devices.",
    "On first launch you see the MTO account overlay—register or log in for E2E encrypted cloud saves that auto-sync every 2s across devices.",
    "tutorial en account",
)

rep(
    "Settings adjusts UI scale, text size, language, account info, cloud sync, Beginner Tutorial, and version history.",
    "Settings adjusts UI scale, text size, and language; Cloud sync shows status and help (refreshes every 2s while open), plus account, tutorial, and version history.",
    "tutorial en settings",
)

path.write_text(s)
print("Patched cloud sync settings copy + 2s UI refresh")
