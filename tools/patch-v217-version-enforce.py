#!/usr/bin/env python3
"""v2.17.0: server-authoritative version.json + enforce same client version for all players."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:320]}")
    s = s.replace(old, new, 1)


OLD_VERSION_BLOCK = (
    "let versionGunNode=null,pendingRemoteVersion=null,pendingLocalRelease=false,versionUpdateShown=false,versionUpdateMandatory=false;"
    "function isVersionUpdateBlocking(){const ol=document.getElementById('version-update-overlay');return versionUpdateMandatory||(ol&&ol.style.display==='flex');}"
    "function setVersionGameBlocked(blocked){const gv=document.getElementById('game-viewport');if(gv)gv.classList.toggle('version-blocked',!!blocked);}"
    "function getVersionSeen(){try{return localStorage.getItem(VERSION_SEEN_KEY)||'';}catch(e){return'';}}"
    "function setVersionSeen(ver){try{localStorage.setItem(VERSION_SEEN_KEY,ver);}catch(e){}}"
    "function wireVersionUpdateButtons(isRemoteNewer){const btnRefresh=document.getElementById('btn-version-update-refresh');if(btnRefresh){btnRefresh.textContent=isRemoteNewer?t('versionUpdateRefresh'):t('versionUpdateOk');btnRefresh.onclick=isRemoteNewer?()=>location.reload():()=>{setVersionSeen(GAME_VERSION);hideVersionUpdateOverlay(false);};}}"
    "function showVersionUpdateNotice(data){if(!data||!data.version||versionUpdateShown)return;const isRemoteNewer=compareGameVersion(data.version,GAME_VERSION)>0;const isLocalRelease=!isRemoteNewer&&data.version===GAME_VERSION&&getVersionSeen()!==GAME_VERSION;if(!isRemoteNewer&&!isLocalRelease)return;versionUpdateShown=true;versionUpdateMandatory=isRemoteNewer;pendingRemoteVersion=isRemoteNewer?data.version:null;pendingLocalRelease=isLocalRelease;const entry=getVersionHistoryEntry(data.version);const summary=(data.summary&&(data.summary[currentLang]||data.summary.zh))||(entry?getVersionSummary(entry):'');const msgKey=isRemoteNewer?'versionUpdateMsg':'versionReleaseMsg';const msg=t(msgKey).replace('{v}',formatGameVersion(data.version))+(summary?'<br><br>'+escapeChatHtml(summary):'');const sumEl=document.getElementById('version-update-summary');if(sumEl)sumEl.innerHTML=msg;const ol=document.getElementById('version-update-overlay');if(ol){ol.style.display='flex';ol.classList.toggle('mandatory',isRemoteNewer);}setVersionGameBlocked(true);wireVersionUpdateButtons(isRemoteNewer);logInfo(t('logVersionUpdate').replace('{v}',formatGameVersion(data.version)).replace('{summary}',summary||'--'));}"
    "function hideVersionUpdateOverlay(dismiss){if(versionUpdateMandatory)return;const ol=document.getElementById('version-update-overlay');if(ol){ol.style.display='none';ol.classList.remove('mandatory');}setVersionGameBlocked(false);if(pendingLocalRelease)setVersionSeen(GAME_VERSION);pendingRemoteVersion=null;pendingLocalRelease=false;versionUpdateShown=false;}"
    "function publishGameVersionToGun(gun){if(!gun||!GAME_VERSION)return;const entry=getVersionHistoryEntry(GAME_VERSION);const payload={version:GAME_VERSION,summary:entry?entry.summary:{zh:'',en:''},publishedAt:Date.now()};gun.get(CLOUD_ROOT).get('game-version').get('current').put(payload);}"
    "function checkLocalVersionRelease(){if(getVersionSeen()===GAME_VERSION)return;const entry=getVersionHistoryEntry(GAME_VERSION);if(!entry)return;setTimeout(()=>showVersionUpdateNotice({version:GAME_VERSION,summary:entry.summary}),800);}"
    "function initVersionWatch(){ensureGameGun(gun=>{if(!versionGunNode){versionGunNode=gun.get(CLOUD_ROOT).get('game-version').get('current');versionGunNode.on(data=>{if(data&&data.version)showVersionUpdateNotice(data);});}versionGunNode.once(data=>{if(!data||compareGameVersion(GAME_VERSION,data.version)>=0)publishGameVersionToGun(gun);});});}"
)

NEW_VERSION_BLOCK = (
    "let versionGunNode=null,pendingRemoteVersion=null,pendingLocalRelease=false,versionUpdateShown=false,versionUpdateMandatory=false,serverCanonicalVersion=null,versionCheckTimer=null;"
    "function isVersionUpdateBlocking(){const ol=document.getElementById('version-update-overlay');return versionUpdateMandatory||(ol&&ol.style.display==='flex');}"
    "function setVersionGameBlocked(blocked){const gv=document.getElementById('game-viewport');if(gv)gv.classList.toggle('version-blocked',!!blocked);}"
    "function getVersionSeen(){try{return localStorage.getItem(VERSION_SEEN_KEY)||'';}catch(e){return'';}}"
    "function setVersionSeen(ver){try{localStorage.setItem(VERSION_SEEN_KEY,ver);}catch(e){}}"
    "function getVersionJsonUrl(){const path=location.pathname||'/';const base=path.endsWith('/')?path:path.replace(/[^/]+$/,'');return location.origin+(base||'/')+'version.json';}"
    "function shouldPublishGameVersionToGun(gunData){if(serverCanonicalVersion&&compareGameVersion(GAME_VERSION,serverCanonicalVersion)!==0)return false;if(!gunData||!gunData.version)return true;return compareGameVersion(GAME_VERSION,gunData.version)>0;}"
    "async function fetchServerGameVersion(){try{const res=await fetch(getVersionJsonUrl()+'?_='+Date.now(),{cache:'no-store'});if(!res.ok)return null;const data=await res.json();return data&&data.version?String(data.version):null;}catch(e){return null;}}"
    "function maybePublishCanonicalVersionToGun(){if(serverCanonicalVersion&&compareGameVersion(GAME_VERSION,serverCanonicalVersion)!==0)return;ensureGameGun(gun=>{if(!versionGunNode)versionGunNode=gun.get(CLOUD_ROOT).get('game-version').get('current');versionGunNode.once(data=>{if(shouldPublishGameVersionToGun(data))publishGameVersionToGun(gun);});});}"
    "async function syncServerGameVersion(){const remote=await fetchServerGameVersion();if(!remote)return;serverCanonicalVersion=remote;if(compareGameVersion(remote,GAME_VERSION)!==0){showVersionUpdateNotice({version:remote,summary:(getVersionHistoryEntry(remote)||{}).summary});return;}maybePublishCanonicalVersionToGun();checkLocalVersionRelease();}"
    "function startServerVersionWatch(){syncServerGameVersion();if(versionCheckTimer)clearInterval(versionCheckTimer);versionCheckTimer=setInterval(()=>syncServerGameVersion(),VERSION_CHECK_MS);}"
    "function wireVersionUpdateButtons(mandatoryRefresh){const btnRefresh=document.getElementById('btn-version-update-refresh');if(btnRefresh){btnRefresh.textContent=mandatoryRefresh?t('versionUpdateRefresh'):t('versionUpdateOk');btnRefresh.onclick=mandatoryRefresh?()=>location.reload():()=>{setVersionSeen(GAME_VERSION);hideVersionUpdateOverlay(false);};}}"
    "function showVersionUpdateNotice(data){if(!data||!data.version)return;const cmp=compareGameVersion(data.version,GAME_VERSION);const isMismatch=cmp!==0;const isLocalRelease=!isMismatch&&getVersionSeen()!==GAME_VERSION;if(!isMismatch&&!isLocalRelease)return;if(versionUpdateShown&&versionUpdateMandatory&&isMismatch)return;versionUpdateShown=true;versionUpdateMandatory=isMismatch;pendingRemoteVersion=isMismatch?data.version:null;pendingLocalRelease=isLocalRelease;const entry=getVersionHistoryEntry(data.version);const summary=(data.summary&&(data.summary[currentLang]||data.summary.zh))||(entry?getVersionSummary(entry):'');const msgKey=isMismatch?(cmp>0?'versionUpdateMsg':'versionMismatchMsg'):'versionReleaseMsg';const msg=t(msgKey).replace('{v}',formatGameVersion(data.version))+(summary?'<br><br>'+escapeChatHtml(summary):'');const sumEl=document.getElementById('version-update-summary');if(sumEl)sumEl.innerHTML=msg;const ol=document.getElementById('version-update-overlay');if(ol){ol.style.display='flex';ol.classList.toggle('mandatory',isMismatch);}setVersionGameBlocked(true);wireVersionUpdateButtons(isMismatch);if(isMismatch||isLocalRelease)logInfo(t('logVersionUpdate').replace('{v}',formatGameVersion(data.version)).replace('{summary}',summary||'--'));}"
    "function hideVersionUpdateOverlay(dismiss){if(versionUpdateMandatory)return;const ol=document.getElementById('version-update-overlay');if(ol){ol.style.display='none';ol.classList.remove('mandatory');}setVersionGameBlocked(false);if(pendingLocalRelease)setVersionSeen(GAME_VERSION);pendingRemoteVersion=null;pendingLocalRelease=false;versionUpdateShown=false;}"
    "function publishGameVersionToGun(gun){if(!gun||!GAME_VERSION)return;if(serverCanonicalVersion&&compareGameVersion(GAME_VERSION,serverCanonicalVersion)!==0)return;const entry=getVersionHistoryEntry(GAME_VERSION);const payload={version:GAME_VERSION,summary:entry?entry.summary:{zh:'',en:''},publishedAt:Date.now()};gun.get(CLOUD_ROOT).get('game-version').get('current').put(payload);}"
    "function checkLocalVersionRelease(){if(getVersionSeen()===GAME_VERSION)return;const entry=getVersionHistoryEntry(GAME_VERSION);if(!entry)return;setTimeout(()=>showVersionUpdateNotice({version:GAME_VERSION,summary:entry.summary}),800);}"
    "function initVersionWatch(){startServerVersionWatch();ensureGameGun(gun=>{if(!versionGunNode){versionGunNode=gun.get(CLOUD_ROOT).get('game-version').get('current');versionGunNode.on(data=>{if(!data||!data.version)return;if(serverCanonicalVersion&&compareGameVersion(data.version,serverCanonicalVersion)!==0)return;showVersionUpdateNotice(data);});}versionGunNode.once(data=>{if(shouldPublishGameVersionToGun(data))publishGameVersionToGun(gun);});});if(!window.__tdVersionVisBound){window.__tdVersionVisBound=true;document.addEventListener('visibilitychange',()=>{if(!document.hidden)syncServerGameVersion();});window.addEventListener('online',()=>syncServerGameVersion());}}"
)

rep(OLD_VERSION_BLOCK, NEW_VERSION_BLOCK, "version block")

rep("VERSION_SEEN_KEY='td_version_seen',GUN_PEERS_DEFAULT", "VERSION_SEEN_KEY='td_version_seen',VERSION_CHECK_MS=120000,GUN_PEERS_DEFAULT", "version check ms")

rep("GAME_VERSION='2.16.0'", "GAME_VERSION='2.17.0'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.16.0'",
    "GAME_VERSION_HISTORY=[{version:'2.17.0',date:'2026-06-08',summary:{zh:'v2.17.0 版本統一：部署後自動同步 version.json 至伺服器，強制所有玩家使用同一遊戲版本；雲端存檔標記版本。',en:'v2.17.0 unified version: deploy writes version.json; all players must run the same game version; cloud saves tagged.'}},{version:'2.16.0'",
    "hist",
)

rep(
    'logBalanceV216:"[更新 v2.16] 雲端同步：登入後每 2 秒自動上傳；本地存檔待同步時強制上傳；設定內可查看即時狀態說明。",',
    'logBalanceV217:"[更新 v2.17] 版本統一：遊戲更新會同步至伺服器 version.json，所有玩家須使用相同版本才能遊玩。",logBalanceV216:"[更新 v2.16] 雲端同步：登入後每 2 秒自動上傳；本地存檔待同步時強制上傳；設定內可查看即時狀態說明。",',
    "i18n zh log",
)
rep(
    'logBalanceV216:"[Update v2.16] Cloud sync: auto-upload every 2s when logged in; force push pending local saves; live status in Settings.",',
    'logBalanceV217:"[Update v2.17] Unified version: deploy syncs version.json; all players must run the same version to play.",logBalanceV216:"[Update v2.16] Cloud sync: auto-upload every 2s when logged in; force push pending local saves; live status in Settings.",',
    "i18n en log",
)
rep(
    'versionUpdateMsg:"新版本 <b>{v}</b> 已發布，<b>必須重新整理後才能繼續遊戲</b>。",versionUpdateRefresh:"立即更新"',
    'versionUpdateMsg:"新版本 <b>{v}</b> 已發布，<b>必須重新整理後才能繼續遊戲</b>。",versionMismatchMsg:"伺服器版本為 <b>{v}</b>，與你目前的客戶端不同，<b>必須重新整理</b>才能與其他玩家使用同一版本。",versionUpdateRefresh:"立即更新"',
    "zh mismatch",
)
rep(
    'versionUpdateMsg:"New version <b>{v}</b> is available. <b>You must refresh to continue playing.</b>",versionUpdateRefresh:"Refresh now"',
    'versionUpdateMsg:"New version <b>{v}</b> is available. <b>You must refresh to continue playing.</b>",versionMismatchMsg:"Server version is <b>{v}</b>. Your client differs — <b>refresh required</b> to play on the same version.",versionUpdateRefresh:"Refresh now"',
    "en mismatch",
)

rep("SAVE_VERSION=45", "SAVE_VERSION=46", "save")
rep(
    "function migrateSave(data){if(data.version<45){data._balanceV216Notice=true;data.version=45;}",
    "function migrateSave(data){if(data.version<46){data._balanceV217Notice=true;data.version=46;}if(data.version<45){data._balanceV216Notice=true;data.version=45;}",
    "migrate v217",
)
rep(
    "const _balanceV216Notice=!!data._balanceV216Notice;delete data._balanceV216Notice;if(data.autoHerbSettings)",
    "const _balanceV216Notice=!!data._balanceV216Notice;delete data._balanceV216Notice;const _balanceV217Notice=!!data._balanceV217Notice;delete data._balanceV217Notice;if(data.autoHerbSettings)",
    "migrate var",
)
rep(
    "if(_balanceV216Notice)logInfo(t('logBalanceV216'));leaderboardTrackedLevel=-1;",
    "if(_balanceV216Notice)logInfo(t('logBalanceV216'));if(_balanceV217Notice)logInfo(t('logBalanceV217'));leaderboardTrackedLevel=-1;",
    "migrate log",
)

rep(
    "return{v:1,passHash:acc.passHash,salt,encProfile,encSave,updatedAt:Date.now(),createdAt:acc.createdAt||Date.now()}",
    "return{v:1,passHash:acc.passHash,salt,encProfile,encSave,gameVersion:GAME_VERSION,updatedAt:Date.now(),createdAt:acc.createdAt||Date.now()}",
    "cloud gameVersion",
)
rep(
    "async function applyCloudRecordToAccount(acc,cloud,password){const profile=cloud.encProfile?",
    "async function applyCloudRecordToAccount(acc,cloud,password){if(cloud.gameVersion&&compareGameVersion(cloud.gameVersion,GAME_VERSION)>0){showVersionUpdateNotice({version:cloud.gameVersion,summary:(getVersionHistoryEntry(cloud.gameVersion)||{}).summary});throw new Error('version');}const profile=cloud.encProfile?",
    "cloud version gate",
)

path.write_text(s)
print("Patched index.html for v2.17.0 version enforce")
