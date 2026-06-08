#!/usr/bin/env python3
"""Fix cloud sync only updating after logout — live runtime refresh + sync restart."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:320]}")
    s = s.replace(old, new, 1)


rep(
    "if(typeof updateCloudSyncDetail==='function')updateCloudSyncDetail();}function waitForGunRelay",
    "if(typeof refreshCloudSyncDisplay==='function')refreshCloudSyncDisplay();}function waitForGunRelay",
    "relay refresh display",
)
rep(
    "let cloudSyncSettingsTimer=null;function stopCloudSyncSettingsRefresh()",
    "let cloudSyncSettingsTimer=null,cloudSyncUiTimer=null;function stopCloudSyncUiRefresh(){if(cloudSyncUiTimer){clearInterval(cloudSyncUiTimer);cloudSyncUiTimer=null;}}function startCloudSyncUiRefresh(){stopCloudSyncUiRefresh();if(!hasActiveCloudSession())return;refreshCloudSyncDisplay();cloudSyncUiTimer=setInterval(()=>{if(!hasActiveCloudSession()){stopCloudSyncUiRefresh();return;}refreshCloudSyncDisplay();},CLOUD_AUTO_SYNC_MS);}function restartCloudSyncRuntime(){if(hasActiveCloudSession()){startCloudAutoSync();startCloudSyncUiRefresh();}else{stopCloudAutoSync();stopCloudSyncUiRefresh();refreshCloudSyncDisplay();}}function stopCloudSyncSettingsRefresh()",
    "runtime refresh helpers",
)
rep(
    "function refreshCloudSyncOnSettingsOpen(){refreshCloudSyncNetworkStatus();updateCloudSyncDetail();}",
    "function refreshCloudSyncOnSettingsOpen(){restartCloudSyncRuntime();}",
    "settings open restart",
)
rep(
    "if(cloudUploadInterval)return;cloudUploadInterval=setInterval(()=>tickCloudAutoSync(),CLOUD_AUTO_SYNC_MS);tickCloudAutoSync();}",
    "if(!cloudUploadInterval){cloudUploadInterval=setInterval(()=>tickCloudAutoSync(),CLOUD_AUTO_SYNC_MS);}tickCloudAutoSync();}",
    "auto sync always tick",
)
rep("function scheduleCloudUpload(){startCloudAutoSync();}", "function scheduleCloudUpload(){restartCloudSyncRuntime();}", "schedule restart")
rep(
    "markAccountCloudPushed();refreshCloudSyncDisplay();return true;}catch(e){refreshCloudSyncDisplay();return false;}}async function applyCloudRecordToAccount",
    "markAccountCloudPushed();return true;}catch(e){return false;}}async function applyCloudRecordToAccount",
    "upload no mid refresh",
)
rep(
    "function beginGameAfterAccount(pulled){hideAccountOverlay();refreshCloudSyncDisplay();loadAccountProfile();initGame();applyDevAccountBootstrap();if(pulled)logInfo(t('cloudSyncPulled'));requestAnimationFrame(updateLayoutMode);startCloudAutoSync();uploadCurrentAccountToCloud();publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "function beginGameAfterAccount(pulled){hideAccountOverlay();loadAccountProfile();initGame();applyDevAccountBootstrap();if(pulled)logInfo(t('cloudSyncPulled'));requestAnimationFrame(updateLayoutMode);restartCloudSyncRuntime();uploadCurrentAccountToCloud({silent:true});publishLeaderboardEntry(true);prefetchLeaderboardCache();}",
    "begin restart",
)
rep(
    "function logoutAccount(){stopCloudAutoSync();saveGame();",
    "function logoutAccount(){stopCloudSyncUiRefresh();stopCloudSyncSettingsRefresh();stopCloudAutoSync();saveGame();",
    "logout stop timers",
)
rep(
    "refreshCloudSyncNetworkStatus();}function loadAccountProfile(){const acc=getActiveAccount();",
    "restartCloudSyncRuntime();}function loadAccountProfile(){const acc=getActiveAccount();",
    "profile ui restart",
)
rep(
    "addEventListener('online',()=>{refreshCloudSyncNetworkStatus();startCloudAutoSync();});",
    "addEventListener('online',()=>{refreshCloudSyncNetworkStatus();restartCloudSyncRuntime();});",
    "online restart",
)
rep(
    "beginGameAfterAccount(false);refreshCloudSyncDisplay();}else{showAccountOverlay();",
    "beginGameAfterAccount(false);}else{showAccountOverlay();",
    "boot dedupe refresh",
)
rep(
    "else{uploadCurrentAccountToCloud();publishLeaderboardEntry(true);ensureGameGun(gun=>publishGameVersionToGun(gun));}prefetchLeaderboardCache();",
    "else{restartCloudSyncRuntime();uploadCurrentAccountToCloud({silent:true});publishLeaderboardEntry(true);ensureGameGun(gun=>publishGameVersionToGun(gun));}prefetchLeaderboardCache();",
    "reconnect restart",
)

path.write_text(s)
print("Patched cloud sync live refresh")
