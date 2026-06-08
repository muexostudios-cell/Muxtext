#!/usr/bin/env python3
"""v2.17.5: Server warmup + faster boot (defer Stripe/Gun, non-blocking reconnect)."""
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


# --- version ---
rep("GAME_VERSION='2.17.4'", "GAME_VERSION='2.17.5'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.4',date:'2026-06-08',summary:{zh:'v2.17.4 修復 v2.17.3 啟動時雲端同步狀態初始化崩潰，設定畫面可正確顯示同步狀態。',en:'v2.17.4 fix v2.17.3 boot crash in cloud sync detail; settings show correct status.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.5',date:'2026-06-08',summary:{zh:'v2.17.5 伺服器強化與加載優化：非阻塞啟動、預連線、延遲載入 Stripe/Gun、背景伺服器預熱。',en:'v2.17.5 server strengthen + load optimize: non-blocking boot, preconnect, lazy Stripe/Gun, background warmup.'}},{version:'2.17.4',date:'2026-06-08',summary:{zh:'v2.17.4 修復 v2.17.3 啟動時雲端同步狀態初始化崩潰，設定畫面可正確顯示同步狀態。',en:'v2.17.4 fix v2.17.3 boot crash in cloud sync detail; settings show correct status.'}},",
    "hist",
)
rep("SAVE_VERSION=50", "SAVE_VERSION=51", "save")

rep(
    'logBalanceV2174:"[修復 v2.17.4] 修復啟動時雲端同步狀態初始化錯誤，設定畫面可正確顯示已登入同步狀態。",logBalanceV2173:',
    'logBalanceV2175:"[優化 v2.17.5] 伺服器預熱與加載加速：啟動不再等待 Gun 中繼、延遲載入付款腳本、背景連線雲端。",logBalanceV2174:"[修復 v2.17.4] 修復啟動時雲端同步狀態初始化錯誤，設定畫面可正確顯示已登入同步狀態。",logBalanceV2173:',
    "i18n zh log",
)
rep(
    'logBalanceV2174:"[Fix v2.17.4] Fix cloud sync status init crash on boot; settings show logged-in sync state.",logBalanceV2173:',
    'logBalanceV2175:"[Optimize v2.17.5] Server warmup + faster load: non-blocking boot, lazy Stripe, background cloud connect.",logBalanceV2174:"[Fix v2.17.4] Fix cloud sync status init crash on boot; settings show logged-in sync state.",logBalanceV2173:',
    "i18n en log",
)
rep(
    "logInfo(t('logBalanceV2174'));logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'));leaderboardTrackedLevel=-1;",
    "logInfo(t('logBalanceV2175'));logInfo(t('logBalanceV2174'));logInfo(t('logBalanceV2173'));logInfo(t('logBalanceV2172'));logInfo(t('logBalanceV2171'));logInfo(t('logBalanceV217'));leaderboardTrackedLevel=-1;",
    "boot log",
)

# --- head: preconnect + remove blocking Stripe ---
rep(
    "<script src=\"https://js.stripe.com/v3/\"></script>",
    "<link rel=\"preconnect\" href=\"https://js.stripe.com\" crossorigin>"
    "<link rel=\"preconnect\" href=\"https://cdn.jsdelivr.net\" crossorigin>"
    "<link rel=\"preconnect\" href=\"https://gun.o8.is\" crossorigin>"
    "<link rel=\"preconnect\" href=\"https://muxtext-chat.muexostudios.workers.dev\" crossorigin>"
    "<link rel=\"dns-prefetch\" href=\"https://gun.defucc.me\">"
    "<link rel=\"dns-prefetch\" href=\"https://muxtext-bug-pipeline.muexostudios.workers.dev\">"
    "<link rel=\"preload\" href=\"https://cdn.jsdelivr.net/npm/gun/gun.js\" as=\"script\" crossorigin>",
    "head preconnect",
)

# --- lazy Stripe loader ---
rep(
    "let stripeJsInstance=null;function getStripeJs(){const pk=getStripePublishableKey();if(!pk||!window.Stripe)return null;",
    "let stripeJsInstance=null,stripeJsLoadPromise=null;function ensureStripeJs(){if(window.Stripe)return Promise.resolve(window.Stripe);if(!stripeJsLoadPromise){stripeJsLoadPromise=new Promise((resolve,reject)=>{const s=document.createElement('script');s.src='https://js.stripe.com/v3/';s.async=true;s.onload=()=>resolve(window.Stripe);s.onerror=()=>reject(new Error('stripe_load'));document.head.appendChild(s);});}return stripeJsLoadPromise;}function getStripeJs(){const pk=getStripePublishableKey();if(!pk||!window.Stripe)return null;",
    "stripe lazy",
)

rep(
    "async function startCardPayment(){if(!selectedRechargePkg)return;const pkg=selectedRechargePkg;",
    "async function startCardPayment(){if(!selectedRechargePkg)return;try{await ensureStripeJs();}catch(e){logInfo(t('rechargeCardPending'));return;}const pkg=selectedRechargePkg;",
    "stripe await",
)

# --- Gun peers: cache + defer wiki on boot ---
rep(
    "GUN_PEERS_DEFAULT=['https://gun.o8.is/gun','https://gun.defucc.me/gun'];let gunPeersActive=[...GUN_PEERS_DEFAULT]",
    "GUN_PEERS_DEFAULT=['https://gun.o8.is/gun','https://gun.defucc.me/gun'],GUN_PEERS_CACHE_KEY='td_gun_peers_v1',GUN_PEERS_CACHE_MS=3600000;let gunPeersActive=[...GUN_PEERS_DEFAULT],gunPeersWikiRefreshing=false",
    "gun cache vars",
)

rep(
    "async function refreshGunPeers(){try{const res=await fetch('https://raw.githubusercontent.com/wiki/amark/gun/volunteer.dht.md',{cache:'no-store'});",
    "function readGunPeersCache(){try{const raw=sessionStorage.getItem(GUN_PEERS_CACHE_KEY);if(!raw)return null;const data=JSON.parse(raw);if(!data||!Array.isArray(data.peers)||!data.at||Date.now()-data.at>GUN_PEERS_CACHE_MS)return null;return mergeGunPeers(data.peers);}catch(e){return null;}}function writeGunPeersCache(peers){try{sessionStorage.setItem(GUN_PEERS_CACHE_KEY,JSON.stringify({at:Date.now(),peers}));}catch(e){}}async function refreshGunPeers(opts){const skipWiki=!!(opts&&opts.skipWiki);const cached=readGunPeersCache();if(cached)gunPeersActive=cached;if(skipWiki){if(!gunPeersWikiRefreshing){gunPeersWikiRefreshing=true;void refreshGunPeers().finally(()=>{gunPeersWikiRefreshing=false;});}return gunPeersActive;}try{const res=await fetch('https://raw.githubusercontent.com/wiki/amark/gun/volunteer.dht.md',{cache:'no-store'});",
    "gun peers cache",
)

rep(
    "if(JSON.stringify(next)!==JSON.stringify(gunPeersActive)){gunPeersActive=next;if(gameGun)resetGameGun();}}catch(e){}return gunPeersActive;}",
    "if(JSON.stringify(next)!==JSON.stringify(gunPeersActive)){gunPeersActive=next;if(gameGun)resetGameGun();}writeGunPeersCache(gunPeersActive);}catch(e){}return gunPeersActive;}",
    "gun peers write cache",
)

rep(
    "async function ensureGunRelayReady(timeoutMs=12000){await refreshGunPeers();ensureGameGun(()=>{});",
    "async function ensureGunRelayReady(timeoutMs=12000,opts){const skipWiki=!!(opts&&opts.skipWiki);await refreshGunPeers(skipWiki?{skipWiki:true}:undefined);ensureGameGun(()=>{});",
    "gun relay skip wiki",
)

# --- non-blocking boot + faster loading overlay ---
rep(
    "gameBooted=false,networkReconnectBusy=false;function getNetworkOverlayMessage()",
    "gameBooted=false,networkReconnectBusy=false,serverWarmupStarted=false;function getNetworkOverlayMessage()",
    "warmup flag",
)

rep(
    "async function tryReconnectServer(initial=false){if(networkReconnectBusy)return false;setNetworkReconnectBusy(true);const offline=typeof navigator!=='undefined'&&navigator.onLine===false;if(offline){updateCloudSyncUI('offline');showNetworkOverlay();setNetworkReconnectBusy(false);return false;}showNetworkOverlay(currentLang==='zh'?'正在連接伺服器，請稍候…':'Connecting to server, please wait...');refreshCloudSyncNetworkStatus();const ok=await ensureGunRelayReady(10000);if(!ok){refreshCloudSyncDisplay();showNetworkOverlay(t('cloudSyncRelayBlocked'));setNetworkReconnectBusy(false);if(!gameBooted)continueGameBoot();return false;}hideNetworkOverlay();setNetworkReconnectBusy(false);if(!gameBooted)continueGameBoot();else{restartCloudSyncRuntime();void uploadCurrentAccountToCloud({silent:true}).catch(()=>{});publishLeaderboardEntry(true);ensureGameGun(gun=>publishGameVersionToGun(gun));}prefetchLeaderboardCache();return true;}",
    "function startServerWarmup(){if(serverWarmupStarted)return;serverWarmupStarted=true;loadGunScript(()=>{});void syncServerGameVersion();void tryReconnectServer(true,{background:true});}async function tryReconnectServer(initial=false,opts){const background=!!(opts&&opts.background);if(networkReconnectBusy&&!background)return false;setNetworkReconnectBusy(true);const offline=typeof navigator!=='undefined'&&navigator.onLine===false;if(offline){updateCloudSyncUI('offline');if(!background)showNetworkOverlay();setNetworkReconnectBusy(false);if(!gameBooted)continueGameBoot();return false;}if(!background)showNetworkOverlay(currentLang==='zh'?'正在連接伺服器，請稍候…':'Connecting to server, please wait...');refreshCloudSyncNetworkStatus();const timeout=background?4500:10000;const ok=await ensureGunRelayReady(timeout,background?{skipWiki:true}:undefined);if(!ok){refreshCloudSyncDisplay();if(!background)showNetworkOverlay(t('cloudSyncRelayBlocked'));setNetworkReconnectBusy(false);if(!gameBooted)continueGameBoot();return false;}hideNetworkOverlay();setNetworkReconnectBusy(false);if(!gameBooted)continueGameBoot();else{restartCloudSyncRuntime();void uploadCurrentAccountToCloud({silent:true}).catch(()=>{});publishLeaderboardEntry(true);ensureGameGun(gun=>publishGameVersionToGun(gun));}prefetchLeaderboardCache();return true;}",
    "tryReconnect",
)

rep(
    "function runBootSequence(){const overlay=document.getElementById('loading-overlay');const textEl=document.getElementById('loading-text');const barFill=document.getElementById('loading-bar-fill');if(textEl)textEl.textContent=t('loadingText');if(overlay)overlay.style.display='flex';if(barFill){barFill.style.animation='none';void barFill.offsetWidth;barFill.style.animation='';}setTimeout(()=>{if(overlay)overlay.classList.add('fade-out');setTimeout(()=>{if(overlay){overlay.style.display='none';overlay.classList.remove('fade-out');}tryReconnectServer(true);},450);},2400);}",
    "function runBootSequence(){const overlay=document.getElementById('loading-overlay');const textEl=document.getElementById('loading-text');const barFill=document.getElementById('loading-bar-fill');if(textEl)textEl.textContent=t('loadingText');if(overlay)overlay.style.display='flex';if(barFill){barFill.style.animation='none';void barFill.offsetWidth;barFill.style.animation='';barFill.style.animationDuration='1.1s';}startServerWarmup();const finishBoot=()=>{if(overlay)overlay.classList.add('fade-out');setTimeout(()=>{if(overlay){overlay.style.display='none';overlay.classList.remove('fade-out');}continueGameBoot();},320);};setTimeout(finishBoot,900);}",
    "boot sequence",
)

# --- defer bug pipeline probe on boot ---
rep(
    "function scheduleBugPipelineProbe(){if(bugPipelineProbeTimer)clearInterval(bugPipelineProbeTimer);if(!getBugPipelineEndpoint()){updateBugPipelineUI();return;}refreshBugPipeline();bugPipelineProbeTimer=setInterval(refreshBugPipeline,BUG_PIPELINE_CONFIG.pollIntervalMs);}",
    "function scheduleBugPipelineProbe(){if(bugPipelineProbeTimer)clearInterval(bugPipelineProbeTimer);if(!getBugPipelineEndpoint()){updateBugPipelineUI();return;}const runProbe=()=>refreshBugPipeline();if(typeof requestIdleCallback==='function')requestIdleCallback(()=>setTimeout(runProbe,1200),{timeout:4000});else setTimeout(runProbe,2500);bugPipelineProbeTimer=setInterval(refreshBugPipeline,BUG_PIPELINE_CONFIG.pollIntervalMs);}",
    "bug probe defer",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (v2.17.5 server load optimize)")
