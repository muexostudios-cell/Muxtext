#!/usr/bin/env python3
"""v2.17.8: Fix version overlay blocking, offline registration, dev level flash, duplicate version log."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")


def rep(old, new, label, count=1):
    global text
    n = text.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:280]}")
    text = text.replace(old, new, 1)


# version
rep("GAME_VERSION='2.17.7'", "GAME_VERSION='2.17.8'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.7',date:'2026-06-08',summary:{zh:'v2.17.7 地下城效能優化：地圖增量渲染、戰鬥 UI 快取、地城內延後雲端同步與存檔。',en:'v2.17.7 dungeon perf: incremental map, battle UI cache, deferred cloud sync/save in dungeon.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.8',date:'2026-06-08',summary:{zh:'v2.17.8 實機測試修復：版本提示不阻擋操作、離線可註冊本機帳號、開發帳號等級顯示與重複日誌。',en:'v2.17.8 audit fixes: non-blocking version notice, offline local registration, dev level flash and duplicate log.'}},{version:'2.17.7',date:'2026-06-08',summary:{zh:'v2.17.7 地下城效能優化：地圖增量渲染、戰鬥 UI 快取、地城內延後雲端同步與存檔。',en:'v2.17.7 dungeon perf: incremental map, battle UI cache, deferred cloud sync/save in dungeon.'}},",
    "hist",
)

rep(
    'logBalanceV2177:"[優化 v2.17.7] 地下城卡頓優化：地圖增量更新、戰鬥介面快取、地城內延後雲端同步。",logBalanceV2176:',
    'logBalanceV2178:"[修復 v2.17.8] 版本提示不阻擋操作、離線可註冊本機帳號、修正開發帳號等級閃爍與重複更新日誌。",logBalanceV2177:"[優化 v2.17.7] 地下城卡頓優化：地圖增量更新、戰鬥介面快取、地城內延後雲端同步。",logBalanceV2176:',
    "i18n zh log",
)
rep(
    'logBalanceV2177:"[Optimize v2.17.7] Dungeon lag fixes: incremental map, battle UI cache, deferred cloud sync in dungeon.",logBalanceV2176:',
    'logBalanceV2178:"[Fix v2.17.8] Non-blocking version notice, offline local registration, dev level flash and duplicate update log.",logBalanceV2177:"[Optimize v2.17.7] Dungeon lag fixes: incremental map, battle UI cache, deferred cloud sync in dungeon.",logBalanceV2176:',
    "i18n en log",
)
rep(
    "registerThinkAgain:\"再想想\",btnAccountLogin:\"登入\"",
    "registerThinkAgain:\"再想想\",registerLocalOnly:\"已建立本機帳號；連上雲端中繼後將自動同步進度。\",registerLocalOnlyHint:\"無法連線雲端中繼，已改為本機註冊。\",btnAccountLogin:\"登入\"",
    "i18n zh reg",
)
rep(
    "registerThinkAgain:\"THINK AGAIN\",btnAccountLogin:\"LOGIN\"",
    "registerThinkAgain:\"THINK AGAIN\",registerLocalOnly:\"Local account created; progress will sync when the cloud relay is available.\",registerLocalOnlyHint:\"Cloud relay unavailable — registered locally only.\",btnAccountLogin:\"LOGIN\"",
    "i18n en reg",
)

rep(
    "if(_balanceV2177Notice)logInfo(t('logBalanceV2177'));logInfo(t('logBalanceV2175'));",
    "if(_balanceV2177Notice)logInfo(t('logBalanceV2177'));if(_balanceV2178Notice)logInfo(t('logBalanceV2178'));logInfo(t('logBalanceV2175'));",
    "load log",
)
rep(
    "function migrateSave(data){if(data.version<53){",
    "function migrateSave(data){if(data.version<54){data._balanceV2178Notice=true;data.version=54;}if(data.version<53){",
    "migrate",
)
rep(
    "const _balanceV2177Notice=!!data._balanceV2177Notice;delete data._balanceV2177Notice;if(data.autoHerbSettings)",
    "const _balanceV2177Notice=!!data._balanceV2177Notice;delete data._balanceV2177Notice;const _balanceV2178Notice=!!data._balanceV2178Notice;delete data._balanceV2178Notice;if(data.autoHerbSettings)",
    "load notice var",
)
rep("SAVE_VERSION=53", "SAVE_VERSION=54", "save")

# CSS: local version notice non-blocking (clicks pass through except dialog box)
rep(
    "#version-update-overlay.mandatory{background:rgba(0,0,0,.95)}",
    "#version-update-overlay:not(.mandatory){pointer-events:none;background:rgba(0,0,0,.45);align-items:flex-end;padding:0 0 calc(env(safe-area-inset-bottom,0) + 12px)}#version-update-overlay:not(.mandatory) #version-update-box{pointer-events:auto;width:min(92vw,360px);margin:0 auto}#version-update-overlay.mandatory{background:rgba(0,0,0,.95)}",
    "css version overlay",
)

# Only mandatory version mismatch blocks gameplay
rep(
    "function isVersionUpdateBlocking(){const ol=document.getElementById('version-update-overlay');return versionUpdateMandatory||(ol&&ol.style.display==='flex');}",
    "function isVersionUpdateBlocking(){return !!versionUpdateMandatory;}",
    "isVersionUpdateBlocking",
)

# version notice log dedupe + non-blocking local release
rep(
    "pendingRemoteVersion=null,pendingLocalRelease=false,versionUpdateShown=false,versionUpdateMandatory=false,serverCanonicalVersion=null",
    "pendingRemoteVersion=null,pendingLocalRelease=false,versionUpdateShown=false,versionUpdateMandatory=false,versionNoticeLogKey='',serverCanonicalVersion=null",
    "version vars",
)

rep(
    "setVersionGameBlocked(true);wireVersionUpdateButtons(isMismatch);if(isMismatch||isLocalRelease)logInfo(t('logVersionUpdate').replace('{v}',formatGameVersion(data.version)).replace('{summary}',summary||'--'));}",
    "setVersionGameBlocked(!!isMismatch);wireVersionUpdateButtons(isMismatch);if(isMismatch||isLocalRelease){const logKey=String(data.version||'');if(versionNoticeLogKey!==logKey){versionNoticeLogKey=logKey;logInfo(t('logVersionUpdate').replace('{v}',formatGameVersion(data.version)).replace('{summary}',summary||'--'));}}}",
    "showVersionUpdateNotice block",
)

# Remove duplicate checkLocalVersionRelease from continueInit (initVersionWatch already syncs)
rep(
    "ensureChatLazyInit();initVersionWatch();checkLocalVersionRelease();applyPendingOverloadPayment().catch(()=>{});};",
    "ensureChatLazyInit();initVersionWatch();applyPendingOverloadPayment().catch(()=>{});};",
    "continueInit dedupe",
)

# Dev account: skip premature status bar before bootstrap
rep(
    "player.hp=clamp(player.hp,0,player.maxHp);renderAllPanels();updateStatusBar();updateButtons();switchTab('log');if(!player.shopItems||player.shopItems.length===0||Date.now()>=player.shopRefreshTime){refreshShop();}startPlaytimeCounter();ensureChatLazyInit();initVersionWatch();applyPendingOverloadPayment().catch(()=>{});};",
    "player.hp=clamp(player.hp,0,player.maxHp);renderAllPanels();if(!isDevAccount())updateStatusBar();updateButtons();switchTab('log');if(!player.shopItems||player.shopItems.length===0||Date.now()>=player.shopRefreshTime){refreshShop();}startPlaytimeCounter();ensureChatLazyInit();initVersionWatch();applyPendingOverloadPayment().catch(()=>{});};",
    "dev skip status",
)

# Offline-friendly registration
rep(
    "await uploadCloudAccount(key,acc,password);return{ok:true};}async function loginAccount(username,password){",
    "if(!opts||!opts.localOnly)await uploadCloudAccount(key,acc,password);return{ok:true,localOnly:!!(opts&&opts.localOnly)};}async function loginAccount(username,password){",
    "registerAccount upload",
)

rep(
    "async function registerAccount(username,password,displayName){const key=normalizeAccountKey(username);if(!isValidUsername(username))return{ok:false,msg:'accountErrorUsername'};if(password.length<4)return{ok:false,msg:'accountErrorPassword'};const passHash=await hashPassword(password);const cloud=await fetchCloudAccount(key);",
    "async function registerAccount(username,password,displayName,opts){const key=normalizeAccountKey(username);if(!isValidUsername(username))return{ok:false,msg:'accountErrorUsername'};if(password.length<4)return{ok:false,msg:'accountErrorPassword'};const passHash=await hashPassword(password);const cloud=(opts&&opts.localOnly)?null:await fetchCloudAccount(key);",
    "registerAccount local",
)

rep(
    "async function proceedWithRegistration(username,password,displayName){setAccountSubmitting(true);try{if(!(await ensureGunRelayReady(10000))){showAccountError(t('cloudSyncRelayBlocked'));return;}const res=await registerAccount(username,password,displayName);if(!res.ok){showAccountError(t(res.msg));return;}beginGameAfterAccount(false);}finally{setAccountSubmitting(false);}}",
    "async function proceedWithRegistration(username,password,displayName){setAccountSubmitting(true);try{const relayOk=await ensureGunRelayReady(8000);const res=await registerAccount(username,password,displayName,relayOk?undefined:{localOnly:true});if(!res.ok){showAccountError(t(res.msg));return;}if(res.localOnly)logInfo(t('registerLocalOnly'));beginGameAfterAccount(false);}finally{setAccountSubmitting(false);}}",
    "proceedWithRegistration",
)

rep(
    "async function beginGameAfterAccount(pulled){hideAccountOverlay();loadAccountProfile();",
    "async function beginGameAfterAccount(pulled){hideAccountOverlay();loadAccountProfile();if(isDevAccount()){const _dl=document.getElementById('lvl-display');if(_dl)_dl.textContent=DEV_ACCOUNT_LEVEL;}",
    "dev level preseed",
)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html -> v2.17.8")
