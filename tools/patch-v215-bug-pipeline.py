#!/usr/bin/env python3
"""v2.15.0: Bug lifecycle pipeline — client detectors, report UI, worker integration."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:240]}")
    s = s.replace(old, new, 1)


BUG_CONFIG = "const BUG_PIPELINE_CONFIG={endpoint:'',pollIntervalMs:120000,reportCooldownMs:60000};"

BUG_JS = r"""let bugPipelineStatus=null,bugPipelineProbeTimer=null,bugLastReportAt=0,bugClientSignals=new Set();function getBugPipelineEndpoint(){return(BUG_PIPELINE_CONFIG.endpoint||'').replace(/\/$/,'');}function collectBugClientSignals(){const signals=new Set(bugClientSignals);if(typeof player!=='undefined'&&player){const peak=Math.floor(Number(player.stats&&player.stats.peakLevel)||0),lv=Math.floor(Number(player.level)||1);if(peak>lv)signals.add('peak_level_mismatch');const cloudTxt=(document.getElementById('cloud-sync-status')?.textContent||'').toLowerCase();if(cloudTxt.includes('offline')||cloudTxt.includes('中斷')||cloudTxt.includes('失敗'))signals.add('cloud_sync_offline');const chatSt=document.getElementById('chat-status');if(chatSt&&(chatSt.classList.contains('offline')||chatSt.textContent==='offline'))signals.add('chat_offline');if(typeof inCombat!=='undefined'&&inCombat&&typeof attackQueue!=='undefined'&&attackQueue.length>0&&typeof isProcessingQueue!=='undefined'&&!isProcessingQueue)signals.add('combat_queue_stuck');if(typeof inDungeon!=='undefined'&&inDungeon&&typeof currentDungeon!=='undefined'&&!currentDungeon)signals.add('dungeon_state_invalid');try{if(typeof requiresPaymentVerification==='function'&&requiresPaymentVerification()&&!PAYMENT_CONFIG.verifyEndpoint)signals.add('payment_verify_unconfigured');}catch(e){}}return[...signals];}function buildBugReportPayload(extra={}){const vp=typeof getLayoutViewport==='function'?getLayoutViewport():{};return{gameVersion:GAME_VERSION,saveVersion:SAVE_VERSION,message:String(extra.message||'').slice(0,500),stack:String(extra.stack||'').slice(0,1000),signals:collectBugClientSignals(),context:{lang:currentLang,inDungeon:!!inDungeon,inCombat:!!inCombat,hasAccount:!!(typeof getSessionKey==='function'&&getSessionKey()),online:typeof navigator==='undefined'||navigator.onLine!==false,viewport:vp},source:extra.source||'client'};}async function fetchBugPipelineStatus(){const base=getBugPipelineEndpoint();if(!base)return null;try{const r=await fetch(base+'/status',{cache:'no-store'});if(!r.ok)return null;return await r.json();}catch(e){return null;}}async function submitBugReport(payload){const base=getBugPipelineEndpoint();if(!base)return{ok:false};const now=Date.now();if(!payload.force&&now-bugLastReportAt<BUG_PIPELINE_CONFIG.reportCooldownMs)return{ok:false,reason:'cooldown'};try{const r=await fetch(base+'/report',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});bugLastReportAt=now;if(!r.ok)return{ok:false};return await r.json();}catch(e){return{ok:false};}}function updateBugPipelineUI(){const stEl=document.getElementById('bug-pipeline-status');if(!stEl)return;if(!getBugPipelineEndpoint()){stEl.textContent=t('bugPipelineDisabled');stEl.className='setting-val';return;}if(!bugPipelineStatus||!bugPipelineStatus.activeIssues||!bugPipelineStatus.activeIssues.length){stEl.textContent=t('bugPipelineOk');stEl.className='setting-val bug-pipeline-ok';return;}const top=bugPipelineStatus.activeIssues[0];const sum=(top.summary&&top.summary[currentLang])||(top.summary&&top.summary.zh)||top.bugId||'';stEl.textContent=sum;stEl.className='setting-val bug-pipeline-warn';}async function refreshBugPipeline(){const data=await fetchBugPipelineStatus();if(data)bugPipelineStatus=data;updateBugPipelineUI();const signals=collectBugClientSignals();if(signals.length)await submitBugReport(buildBugReportPayload({message:'auto-detect: '+signals.join(','),source:'auto-probe'}));}function scheduleBugPipelineProbe(){if(bugPipelineProbeTimer)clearInterval(bugPipelineProbeTimer);if(!getBugPipelineEndpoint()){updateBugPipelineUI();return;}refreshBugPipeline();bugPipelineProbeTimer=setInterval(refreshBugPipeline,BUG_PIPELINE_CONFIG.pollIntervalMs);}function setupBugPipelineErrorHooks(){window.addEventListener('error',e=>{bugClientSignals.add('js_error');submitBugReport(buildBugReportPayload({message:e.message||'error',stack:(e.error&&e.error.stack||'').slice(0,800),source:'onerror'}));});window.addEventListener('unhandledrejection',e=>{bugClientSignals.add('unhandled_rejection');const reason=e.reason;submitBugReport(buildBugReportPayload({message:String(reason&&reason.message||reason),stack:String(reason&&reason.stack||'').slice(0,800),source:'unhandledrejection'}));});}function renderBugLifecycleOverlay(){const list=document.getElementById('bug-lifecycle-list');if(!list)return;const issues=(bugPipelineStatus&&bugPipelineStatus.activeIssues)||[];const stages=(bugPipelineStatus&&bugPipelineStatus.stages)||[];let html='<p class="bug-lifecycle-intro">'+t('bugLifecycleIntro')+'</p>';if(!getBugPipelineEndpoint()){html+='<p>'+t('bugPipelineDisabled')+'</p>';}else if(!issues.length){html+='<p class="bug-pipeline-ok">'+t('bugPipelineOk')+'</p>';}else{html+='<ul class="bug-lifecycle-items">';issues.forEach(it=>{const sum=(it.summary&&it.summary[currentLang])||(it.summary&&it.summary.zh)||it.bugId;const fix=it.fixVersion?' → v'+it.fixVersion:'';html+='<li><b>'+it.stage+'</b> · '+sum+fix+' <span class="bug-sev-'+it.severity+'">'+it.severity+'</span></li>';});html+='</ul>';}if(stages.length)html+='<p class="bug-lifecycle-stages">'+t('bugLifecycleStages')+': '+stages.join(' → ')+'</p>';list.innerHTML=html;}function openBugLifecycleOverlay(){renderBugLifecycleOverlay();const ol=document.getElementById('bug-lifecycle-overlay');if(ol)ol.style.display='flex';}function closeBugLifecycleOverlay(){const ol=document.getElementById('bug-lifecycle-overlay');if(ol)ol.style.display='none';}function promptBugReport(){const base=getBugPipelineEndpoint();if(!base){showAlert(t('bugPipelineDisabled'));return;}showConfirm(t('bugReportPrompt'),()=>{const extra=window.prompt(currentLang==='zh'?'補充說明（可留空）':'Details (optional)','')||'';submitBugReport(buildBugReportPayload({message:extra||'player-report',source:'manual',force:true})).then(res=>{if(res&&res.ok){const hint=res.fixVersion&&res.fixVersion!==GAME_VERSION?t('bugPipelineFixHint',res.fixVersion):t('bugReportThanks');showAlert(hint);logInfo(t('bugReportLogged'));refreshBugPipeline();}else showAlert(t('bugReportFail'));});});}function setupBugPipelineUI(){setupBugPipelineErrorHooks();scheduleBugPipelineProbe();const btnLife=document.getElementById('btn-bug-lifecycle');if(btnLife)btnLife.addEventListener('click',openBugLifecycleOverlay);const btnClose=document.getElementById('btn-close-bug-lifecycle');if(btnClose)btnClose.addEventListener('click',closeBugLifecycleOverlay);const ol=document.getElementById('bug-lifecycle-overlay');if(ol)ol.addEventListener('click',e=>{if(e.target===ol)closeBugLifecycleOverlay();});const btnReport=document.getElementById('btn-bug-report');if(btnReport)btnReport.addEventListener('click',promptBugReport);}"""

# version
rep("GAME_VERSION='2.14.3'", "GAME_VERSION='2.15.0'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.14.3'",
    "GAME_VERSION_HISTORY=[{version:'2.15.0',date:'2026-06-08',summary:{zh:'v2.15.0 Bug 生命週期流水線：自動偵測、回報與伺服器健康檢查。',en:'v2.15.0 bug lifecycle pipeline: auto-detect, report, and server health probes.'}},{version:'2.14.3'",
    "hist",
)
rep("SAVE_VERSION=43", "SAVE_VERSION=44", "save")

# i18n zh
rep(
    'btnTutorial:"新手教學",',
    'btnTutorial:"新手教學",labelBugPipeline:"Bug 監測",bugPipelineOk:"正常",bugPipelineDisabled:"未連線",bugPipelineFixHint:"已知修復版本 v{0}，請重新整理。",btnBugLifecycle:"Bug 生命週期",btnBugReport:"回報問題",bugLifecycleTitle:"Bug 生命週期",bugLifecycleIntro:"依玩家回報與後台探測自動分類；伺服器問題經 AI／規則確認後進入修復流程。",bugLifecycleStages:"階段",bugReportPrompt:"將自動附帶版本與診斷資訊並送出，是否回報？",bugReportThanks:"已送出，感謝回報。",bugReportFail:"送出失敗，請稍後再試。",bugReportLogged:"[Bug] 問題已記錄至生命週期流水線。",logBalanceV215:"[更新 v2.15] Bug 生命週期：設定可查看狀態與回報；客戶端會自動偵測常見問題。",',
    "i18n zh",
)
rep(
    'btnLeaderboard:"RANKINGS",',
    'btnLeaderboard:"RANKINGS",labelBugPipeline:"BUG MONITOR",bugPipelineOk:"OK",bugPipelineDisabled:"OFFLINE",bugPipelineFixHint:"Fix available in v{0} — please refresh.",btnBugLifecycle:"BUG LIFECYCLE",btnBugReport:"REPORT BUG",bugLifecycleTitle:"BUG LIFECYCLE",bugLifecycleIntro:"Reports and backend probes are auto-classified; server issues are confirmed before fixes ship.",bugLifecycleStages:"Stages",bugReportPrompt:"Send version and diagnostics to the bug pipeline?",bugReportThanks:"Report sent. Thank you.",bugReportFail:"Could not send report. Try again later.",bugReportLogged:"[Bug] Issue logged to lifecycle pipeline.",logBalanceV215:"[Update v2.15] Bug lifecycle: check status and report in Settings; common issues are auto-detected.",',
    "i18n en",
)

# CSS
rep(
    "#btn-version-history,#btn-tutorial{background:0 0;border:1px solid #333;color:#888;font-family:inherit;font-size:.55rem;padding:.3rem;margin-top:.5rem;width:100%;cursor:pointer}",
    "#btn-version-history,#btn-tutorial,#btn-bug-lifecycle,#btn-bug-report{background:0 0;border:1px solid #333;color:#888;font-family:inherit;font-size:.55rem;padding:.3rem;margin-top:.5rem;width:100%;cursor:pointer}",
    "css btn",
)
rep(
    "#btn-version-history:active,#btn-tutorial:active{color:var(--accent);border-color:var(--accent)}",
    "#btn-version-history:active,#btn-tutorial:active,#btn-bug-lifecycle:active,#btn-bug-report:active{color:var(--accent);border-color:var(--accent)}",
    "css btn active",
)
rep(
    "#version-history-overlay,#version-update-overlay,",
    "#bug-lifecycle-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:10050;justify-content:center;align-items:center;padding:1rem}#bug-lifecycle-panel{background:#000;border:1px solid #333;max-width:420px;width:100%;max-height:80dvh;overflow:auto;padding:1rem}.bug-lifecycle-intro{font-size:.55rem;color:#888;margin-bottom:.5rem}.bug-lifecycle-items{font-size:.55rem;padding-left:1rem;margin:.5rem 0}.bug-lifecycle-items li{margin:.25rem 0}.bug-lifecycle-stages{font-size:.5rem;color:#666}.bug-pipeline-ok{color:#4f4!important}.bug-pipeline-warn{color:#fa0!important}.bug-sev-critical{color:#f44}.bug-sev-high{color:#f84}.bug-sev-medium{color:#fa0}.bug-sev-low{color:#888}#version-history-overlay,#version-update-overlay,",
    "css overlay",
)

# settings HTML
rep(
    '<button id="btn-version-history">歷史遊戲版本</button><button id="btn-tutorial">新手教學</button>',
    '<div class="setting-row" id="bug-pipeline-row"><label id="label-bug-pipeline">Bug 監測</label><span id="bug-pipeline-status" class="setting-val">--</span></div><button id="btn-bug-lifecycle">Bug 生命週期</button><button id="btn-bug-report">回報問題</button><button id="btn-version-history">歷史遊戲版本</button><button id="btn-tutorial">新手教學</button>',
    "settings html",
)

# overlay HTML
rep(
    '<div id="version-history-overlay">',
    '<div id="bug-lifecycle-overlay"><div id="bug-lifecycle-panel"><h3 id="bug-lifecycle-title">Bug 生命週期</h3><div id="bug-lifecycle-list"></div><button id="btn-close-bug-lifecycle">關閉</button></div></div><div id="version-history-overlay">',
    "overlay html",
)

# applyLanguage
rep(
    "const _btut=document.getElementById('btn-tutorial');if(_btut)_btut.textContent=t('btnTutorial');",
    "const _lbp=document.getElementById('label-bug-pipeline');if(_lbp)_lbp.textContent=t('labelBugPipeline');const _bbl=document.getElementById('btn-bug-lifecycle');if(_bbl)_bbl.textContent=t('btnBugLifecycle');const _bbr=document.getElementById('btn-bug-report');if(_bbr)_bbr.textContent=t('btnBugReport');const _blt=document.getElementById('bug-lifecycle-title');if(_blt)_blt.textContent=t('bugLifecycleTitle');const _bcb=document.getElementById('btn-close-bug-lifecycle');if(_bcb)_bcb.textContent=t('btnClose');const _btut=document.getElementById('btn-tutorial');if(_btut)_btut.textContent=t('btnTutorial');",
    "apply lang",
)

# CHAT_CONFIG + BUG_PIPELINE_CONFIG
rep(
    "CHAT_CONFIG={endpoint:'https://muxtext-chat.muexostudios.workers.dev',pollIntervalMs:5000};",
    "CHAT_CONFIG={endpoint:'https://muxtext-chat.muexostudios.workers.dev',pollIntervalMs:5000};" + BUG_CONFIG,
    "bug config",
)

# bug pipeline JS before restartGame
rep("function restartGame(){", BUG_JS + "function restartGame(){", "bug js")

# migrate notice
rep(
    "function migrateSave(data){if(data.version<43){",
    "function migrateSave(data){if(data.version<44){data._balanceV215Notice=true;data.version=44;}if(data.version<43){",
    "migrate",
)
rep(
    "const _balanceV214Notice=!!data._balanceV214Notice;delete data._balanceV214Notice;if(data.autoHerbSettings)",
    "const _balanceV214Notice=!!data._balanceV214Notice;delete data._balanceV214Notice;const _balanceV215Notice=!!data._balanceV215Notice;delete data._balanceV215Notice;if(data.autoHerbSettings)",
    "migrate var",
)
rep(
    "if(_balanceV214Notice)logInfo(t('logBalanceV214'));leaderboardTrackedLevel=-1;",
    "if(_balanceV214Notice)logInfo(t('logBalanceV214'));if(_balanceV215Notice)logInfo(t('logBalanceV215'));leaderboardTrackedLevel=-1;",
    "migrate log",
)

# boot
rep(
    "setupVersionUI();setupLeaderboardUI();runBootSequence();",
    "setupVersionUI();setupLeaderboardUI();setupBugPipelineUI();runBootSequence();",
    "boot",
)

path.write_text(s)
print("Patched index.html for v2.15.0 bug lifecycle pipeline")
