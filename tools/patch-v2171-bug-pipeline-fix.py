#!/usr/bin/env python3
"""v2.17.1: Fix cloud-sync unhandled rejections; improve bug pipeline triage."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")


def rep(old, new, label, count=1):
    global text
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:200]}")
    text = text.replace(old, new, 1)


# version
rep("GAME_VERSION='2.17.0'", "GAME_VERSION='2.17.1'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.0',date:'2026-06-08',summary:{zh:'v2.17.0 版本統一：部署後自動同步 version.json 至伺服器，強制所有玩家使用同一遊戲版本；雲端存檔標記版本。',en:'v2.17.0 unified version: deploy writes version.json; all players must run the same game version; cloud saves tagged.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.1',date:'2026-06-08',summary:{zh:'v2.17.1 Bug 監測修復：雲端同步未捕獲錯誤、中繼探測與分類優化。',en:'v2.17.1 bug-monitor fixes: cloud sync promise handling, relay probes, triage.'}},{version:'2.17.0',date:'2026-06-08',summary:{zh:'v2.17.0 版本統一：部署後自動同步 version.json 至伺服器，強制所有玩家使用同一遊戲版本；雲端存檔標記版本。',en:'v2.17.0 unified version: deploy writes version.json; all players must run the same game version; cloud saves tagged.'}},",
    "hist",
)
rep("SAVE_VERSION=46", "SAVE_VERSION=47", "save")

rep(
    'logBalanceV217:"[更新 v2.17] 版本統一：遊戲更新會同步至伺服器 version.json，所有玩家須使用相同版本才能遊玩。",logBalanceV216:',
    'logBalanceV2171:"[修復 v2.17.1] 依 Bug 監測修復雲端同步未捕獲錯誤；優化中繼重試與問題分類。",logBalanceV217:"[更新 v2.17] 版本統一：遊戲更新會同步至伺服器 version.json，所有玩家須使用相同版本才能遊玩。",logBalanceV216:',
    "i18n zh log",
)
rep(
    'logBalanceV217:"[Update v2.17] Unified version: deploy syncs version.json; all players must run the same version to play.",logBalanceV216:',
    'logBalanceV2171:"[Fix v2.17.1] Bug-monitor fixes: cloud sync promise handling, relay retry, and triage.",logBalanceV217:"[Update v2.17] Unified version: deploy syncs version.json; all players must run the same version to play.",logBalanceV216:',
    "i18n en log",
)

rep("logInfo(t('logBalanceV217'))", "logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'))", "boot log")

# cloud sync: no throw from putCloudAccount
rep(
    "async function putCloudAccount(key,payload,timeoutMs=14000){for(let attempt=0;attempt<2;attempt++){try{await putCloudAccountOnce(key,payload,timeoutMs);return true;}catch(e){if(attempt===0){resetGameGun();await refreshGunPeers();}else throw e;}}return false;}",
    "async function putCloudAccount(key,payload,timeoutMs=14000){for(let attempt=0;attempt<2;attempt++){try{await putCloudAccountOnce(key,payload,timeoutMs);return true;}catch(e){if(attempt===0){resetGameGun();await refreshGunPeers();}}}return false;}",
    "putCloudAccount",
)

# tick: safe async + relay catch
rep(
    "function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession()){stopCloudAutoSync();return;}if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(!gunPeerConnected&&Date.now()-lastGunRelayProbeAt>15000){lastGunRelayProbeAt=Date.now();ensureGunRelayReady(8000).then(ok=>{if(ok&&typeof restartCloudSyncRuntime==='function')restartCloudSyncRuntime();else if(typeof refreshCloudSyncDisplay==='function')refreshCloudSyncDisplay();});return;}if(accountNeedsCloudPush()){forceCloudSyncFromLocal();return;}tickCloudIdleSync();}",
    "function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession()){stopCloudAutoSync();return;}if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(!gunPeerConnected&&Date.now()-lastGunRelayProbeAt>15000){lastGunRelayProbeAt=Date.now();ensureGunRelayReady(8000).then(ok=>{if(ok&&typeof restartCloudSyncRuntime==='function')restartCloudSyncRuntime();else if(typeof refreshCloudSyncDisplay==='function')refreshCloudSyncDisplay();}).catch(()=>{if(typeof refreshCloudSyncDisplay==='function')refreshCloudSyncDisplay();});return;}if(accountNeedsCloudPush()){void forceCloudSyncFromLocal().catch(()=>{});return;}void tickCloudIdleSync().catch(()=>{});}",
    "tickCloudAutoSync",
)

# forceCloudSync: safe saveGame
rep(
    "if(typeof saveGame==='function')saveGame();const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;cloudUploadBusy=true;let ok=false;try{const cloud=await fetchCloudAccount(key);",
    "try{if(typeof saveGame==='function')saveGame();}catch(e){}const store=loadAccountStore();const acc=store.byKey[key];if(!acc)return false;cloudUploadBusy=true;let ok=false;try{const cloud=await fetchCloudAccount(key);",
    "forceCloud saveGame",
)

# uploadCurrentAccountToCloud: catch failures
rep(
    "showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}}finally{cloudUploadBusy=false;refreshCloudSyncDisplay();}return ok;}",
    "showNetworkOverlay(currentLang==='zh'?'伺服器同步失敗，連線可能不穩定。請重新連接後繼續遊戲。':'Server sync failed. Your connection may be unstable. Reconnect before continuing.');}if(!ok)bugClientSignals.add('cloud_upload_fail');}catch(e){ok=false;bugClientSignals.add('cloud_upload_fail');}finally{cloudUploadBusy=false;refreshCloudSyncDisplay();}return ok;}",
    "upload catch",
)

# beginGameAfterAccount + reconnect silent uploads
rep(
    "uploadCurrentAccountToCloud({silent:true});publishLeaderboardEntry(true);prefetchLeaderboardCache();",
    "void uploadCurrentAccountToCloud({silent:true}).catch(()=>{});publishLeaderboardEntry(true);prefetchLeaderboardCache();",
    "beginGame upload",
)
rep(
    "restartCloudSyncRuntime();uploadCurrentAccountToCloud({silent:true});publishLeaderboardEntry(true);ensureGameGun(gun",
    "restartCloudSyncRuntime();void uploadCurrentAccountToCloud({silent:true}).catch(()=>{});publishLeaderboardEntry(true);ensureGameGun(gun",
    "reconnect upload",
)

# cloud sync display when relay down
rep(
    "function resolveCloudSyncDisplayState(){if(cloudUploadBusy||cloudSyncInProgress)return'syncing';if(!hasActiveCloudSession())return'local';if(typeof navigator!=='undefined'&&navigator.onLine===false)return'offline';if(accountNeedsCloudPush())return'local';return'synced';}",
    "function resolveCloudSyncDisplayState(){if(cloudUploadBusy||cloudSyncInProgress)return'syncing';if(!hasActiveCloudSession())return'local';if(typeof navigator!=='undefined'&&navigator.onLine===false)return'offline';if(!gunPeerConnected)return'offline';if(accountNeedsCloudPush())return'local';return'synced';}",
    "resolveCloudState",
)

# bug pipeline client
rep(
    "let bugPipelineStatus=null,bugPipelineProbeTimer=null,bugLastReportAt=0,bugClientSignals=new Set();",
    "let bugPipelineStatus=null,bugPipelineProbeTimer=null,bugLastReportAt=0,bugLastRejectionAt=0,bugLastRejectionMsg='',bugClientSignals=new Set();",
    "bug vars",
)

rep(
    "if(typeof inDungeon!=='undefined'&&inDungeon&&typeof currentDungeon!=='undefined'&&!currentDungeon)signals.add('dungeon_state_invalid');}return[...signals];}",
    "if(typeof inDungeon!=='undefined'&&inDungeon&&typeof currentDungeon!=='undefined'&&!currentDungeon)signals.add('dungeon_state_invalid');}try{if(typeof hasActiveCloudSession==='function'&&hasActiveCloudSession()){if(typeof gunPeerConnected!=='undefined'&&!gunPeerConnected)signals.add('gun_relay_blocked');if(typeof accountNeedsCloudPush==='function'&&accountNeedsCloudPush()&&gunPeerConnected)signals.add('cloud_upload_fail');if(typeof requiresPaymentVerification==='function'&&requiresPaymentVerification()&&!PAYMENT_CONFIG.verifyEndpoint)signals.add('stripe_verify_unconfigured');}}catch(e){}return[...signals];}",
    "collect signals",
)

rep(
    "const activeIssues=(bugPipelineStatus&&bugPipelineStatus.activeIssues||[]).filter(it=>it.bugId&&it.bugId!=='unknown');",
    "const activeIssues=(bugPipelineStatus&&bugPipelineStatus.activeIssues||[]).filter(it=>it.bugId&&it.bugId!=='unknown'&&!(it.fixVersion&&typeof compareGameVersion==='function'&&compareGameVersion(GAME_VERSION,it.fixVersion)>=0));",
    "filter fixed bugs ui",
)

rep(
    "window.addEventListener('unhandledrejection',e=>{bugClientSignals.add('unhandled_rejection');const reason=e.reason;submitBugReport(buildBugReportPayload({message:String(reason&&reason.message||reason),stack:String(reason&&reason.stack||'').slice(0,800),source:'unhandledrejection'}));});",
    "window.addEventListener('unhandledrejection',e=>{const reason=e.reason;const msg=String(reason&&reason.message||reason||'');const stack=String(reason&&reason.stack||'');const now=Date.now();if(msg&&msg===bugLastRejectionMsg&&now-bugLastRejectionAt<300000)return;bugLastRejectionMsg=msg;bugLastRejectionAt=now;if(typeof e.preventDefault==='function')e.preventDefault();if(/putCloudAccount|fetchCloudAccount|uploadCloudAccount|forceCloudSync|tickCloudIdle/i.test(stack+msg))bugClientSignals.add('cloud_upload_fail');if(typeof hasActiveCloudSession==='function'&&hasActiveCloudSession()&&!gunPeerConnected)bugClientSignals.add('gun_relay_blocked');bugClientSignals.add('unhandled_rejection');submitBugReport(buildBugReportPayload({message:msg,stack:stack.slice(0,800),source:'unhandledrejection'}));});",
    "rejection hook",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (v2.17.1 bug pipeline fix)")
