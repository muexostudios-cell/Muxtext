#!/usr/bin/env python3
"""Optimize cloud sync: fix force-pull bug, skip redundant 2s uploads, idle cloud pull."""
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
    "cloudSyncState='local',CLOUD_AUTO_SYNC_MS=2000,cloudUploadTimeout=null,cloudUploadInterval=null,cloudUploadBusy=false",
    "cloudSyncState='local',CLOUD_AUTO_SYNC_MS=2000,cloudUploadInterval=null,cloudUploadBusy=false",
    "drop upload timeout var",
)
rep(
    "acc.lastCloudPushAt=Date.now();saveAccountStore(store);}function stopCloudAutoSync()",
    "acc.lastCloudPushAt=getSaveUpdatedAt(acc.save)||Date.now();saveAccountStore(store);}function stopCloudAutoSync()",
    "push mark uses savedAt",
)
rep(
    "function stopCloudAutoSync(){if(cloudUploadInterval){clearInterval(cloudUploadInterval);cloudUploadInterval=null;}if(cloudUploadTimeout){clearTimeout(cloudUploadTimeout);cloudUploadTimeout=null;}}",
    "function stopCloudAutoSync(){if(cloudUploadInterval){clearInterval(cloudUploadInterval);cloudUploadInterval=null;}}",
    "stop sync no timeout",
)
rep(
    "if(cloud){const merged=await applyCloudRecordToAccount(acc,cloud,secret.password);if(merged.pulled){",
    "if(cloud){const pulled=await applyCloudRecordToAccount(acc,cloud,secret.password);if(pulled){",
    "fix force pull boolean",
)
rep(
    "ok=await uploadCloudAccount(key,acc,secret.password);if(ok){markAccountCloudPushed();saveAccountStore(store);publishLeaderboardEntry(true);}}catch(e){ok=false;}finally{cloudUploadBusy=false;refreshCloudSyncDisplay();}return ok;}function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession())return;if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(cloudSyncState==='local'||accountNeedsCloudPush()){forceCloudSyncFromLocal();return;}if(typeof saveGame==='function')saveGame();uploadCurrentAccountToCloud({silent:true});}",
    "ok=await uploadCloudAccount(key,acc,secret.password);if(ok){saveAccountStore(store);publishLeaderboardEntry(true);}}catch(e){ok=false;}finally{cloudUploadBusy=false;refreshCloudSyncDisplay();}return ok;}async function tickCloudIdleSync(){if(cloudSyncInProgress||cloudUploadBusy||inCombat||inDungeon)return;const key=getSessionKey();const secret=restoreSessionAccountSecret();if(!key||!secret||secret.key!==key)return;cloudUploadBusy=true;try{const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return;const cloud=await fetchCloudAccount(key,5000);if(!cloud||cloud.passHash!==acc.passHash)return;const pulled=await applyCloudRecordToAccount(acc,cloud,secret.password);if(pulled){saveAccountStore(store);if(loadGame()){renderAllPanels();updateStatusBar();updateButtons();renderDungeonAdventure();}}}catch(e){}finally{cloudUploadBusy=false;refreshCloudSyncDisplay();}}function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession()){stopCloudAutoSync();return;}if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(accountNeedsCloudPush()){forceCloudSyncFromLocal();return;}tickCloudIdleSync();}",
    "tick idle pull + push only when needed",
)
rep(
    "ok=await uploadCloudAccount(key,acc,secret.password);if(ok){markAccountCloudPushed();saveAccountStore(store);publishLeaderboardEntry(true);if(!silent)refreshCloudSyncDisplay();",
    "ok=await uploadCloudAccount(key,acc,secret.password);if(ok){saveAccountStore(store);publishLeaderboardEntry(true);if(!silent)refreshCloudSyncDisplay();",
    "upload current dedupe mark",
)
rep(
    "const uploaded=await uploadCloudAccount(key,acc,secret.password);if(!uploaded)throw new Error('upload');markAccountCloudPushed();saveAccountStore(store);updateCloudSyncUI('connected');",
    "const uploaded=await uploadCloudAccount(key,acc,secret.password);if(!uploaded)throw new Error('upload');saveAccountStore(store);refreshCloudSyncDisplay();",
    "manual sync dedupe mark",
)

path.write_text(s)
print("Patched cloud sync optimize")
