#!/usr/bin/env python3
"""v2.17.2: Server bug audit — client catalog fallback, auto-report noise filter."""
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


rep("GAME_VERSION='2.17.1'", "GAME_VERSION='2.17.2'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.1',date:'2026-06-08',summary:{zh:'v2.17.1 Bug 監測修復：雲端同步未捕獲錯誤、中繼探測與分類優化。',en:'v2.17.1 bug-monitor fixes: cloud sync promise handling, relay probes, triage.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.2',date:'2026-06-08',summary:{zh:'v2.17.2 伺服器全面檢查：Bug 監測本地目錄備援、停止付款雜訊回報、Gun 節點優化。',en:'v2.17.2 server audit: local bug catalog fallback, payment noise filter, Gun peers.'}},{version:'2.17.1',date:'2026-06-08',summary:{zh:'v2.17.1 Bug 監測修復：雲端同步未捕獲錯誤、中繼探測與分類優化。',en:'v2.17.1 bug-monitor fixes: cloud sync promise handling, relay probes, triage.'}},",
    "hist",
)
rep("SAVE_VERSION=47", "SAVE_VERSION=48", "save")

rep(
    'logBalanceV2171:"[修復 v2.17.1] 依 Bug 監測修復雲端同步未捕獲錯誤；優化中繼重試與問題分類。",logBalanceV217:',
    'logBalanceV2172:"[修復 v2.17.2] 伺服器全面檢查：Bug 監測本地修復目錄、過濾付款雜訊回報、優化 Gun 節點。",logBalanceV2171:"[修復 v2.17.1] 依 Bug 監測修復雲端同步未捕獲錯誤；優化中繼重試與問題分類。",logBalanceV217:',
    "i18n zh log",
)
rep(
    'logBalanceV2171:"[Fix v2.17.1] Bug-monitor fixes: cloud sync promise handling, relay retry, and triage.",logBalanceV217:',
    'logBalanceV2172:"[Fix v2.17.2] Server audit: local bug-fix catalog, payment noise filter, Gun peers.",logBalanceV2171:"[Fix v2.17.1] Bug-monitor fixes: cloud sync promise handling, relay retry, and triage.",logBalanceV217:',
    "i18n en log",
)
rep("logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'))", "logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'))", "boot log")

rep(
    "GUN_PEERS_DEFAULT=['https://gun.o8.is/gun','https://relay.peer.ooo/gun','https://gun.defucc.me/gun'];",
    "GUN_PEERS_DEFAULT=['https://gun.o8.is/gun','https://gun.defucc.me/gun'];",
    "gun peers",
)

rep(
    "let bugPipelineStatus=null,bugPipelineProbeTimer=null,bugLastReportAt=0,bugLastRejectionAt=0,bugLastRejectionMsg='',bugClientSignals=new Set();",
    "let bugPipelineStatus=null,bugPipelineProbeTimer=null,bugLastReportAt=0,bugLastRejectionAt=0,bugLastRejectionMsg='',bugClientSignals=new Set();const LOCAL_KNOWN_BUG_FIXES={'level-rollback':'2.14.3','cloud-sync-fail':'2.17.1','xp-bar-stale':'2.6.6','leaderboard-stale':'2.8.6'};const AUTO_REPORT_IGNORE_SIGNALS=new Set(['stripe_verify_unconfigured','health_check']);function getBugCatalogFixVersion(bugId){const remote=(bugPipelineStatus&&bugPipelineStatus.knownBugs||[]).find(b=>b.id===bugId);if(remote&&remote.fixedVersion)return remote.fixedVersion;return LOCAL_KNOWN_BUG_FIXES[bugId]||null;}function isBugFixedForClient(issue){if(!issue||!issue.bugId)return false;const fix=issue.fixVersion||getBugCatalogFixVersion(issue.bugId);return !!(fix&&typeof compareGameVersion==='function'&&compareGameVersion(GAME_VERSION,fix)>=0);}function filterActiveBugIssues(list){return (list||[]).filter(it=>it.bugId&&it.bugId!=='unknown'&&!isBugFixedForClient(it));}function getAutoReportSignals(){return collectBugClientSignals().filter(s=>!AUTO_REPORT_IGNORE_SIGNALS.has(s));}",
    "bug helpers",
)

rep(
    "const activeIssues=(bugPipelineStatus&&bugPipelineStatus.activeIssues||[]).filter(it=>it.bugId&&it.bugId!=='unknown'&&!(it.fixVersion&&typeof compareGameVersion==='function'&&compareGameVersion(GAME_VERSION,it.fixVersion)>=0));",
    "const activeIssues=filterActiveBugIssues(bugPipelineStatus&&bugPipelineStatus.activeIssues);",
    "updateUI filter",
)

rep(
    "const issues=((bugPipelineStatus&&bugPipelineStatus.activeIssues)||[]).filter(it=>it.bugId&&it.bugId!=='unknown'&&!(it.fixVersion&&typeof compareGameVersion==='function'&&compareGameVersion(GAME_VERSION,it.fixVersion)>=0));",
    "const issues=filterActiveBugIssues(bugPipelineStatus&&bugPipelineStatus.activeIssues);",
    "lifecycle filter",
)

rep(
    "async function refreshBugPipeline(){const data=await fetchBugPipelineStatus();if(data)bugPipelineStatus=data;updateBugPipelineUI();const signals=collectBugClientSignals();if(signals.length)await submitBugReport(buildBugReportPayload({message:'auto-detect: '+signals.join(','),source:'auto-probe'}));}",
    "async function refreshBugPipeline(){const data=await fetchBugPipelineStatus();if(data)bugPipelineStatus=data;updateBugPipelineUI();const signals=getAutoReportSignals();if(signals.length)await submitBugReport(buildBugReportPayload({message:'auto-detect: '+signals.join(','),source:'auto-probe'}));}",
    "refreshBugPipeline",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (v2.17.2 server audit)")
