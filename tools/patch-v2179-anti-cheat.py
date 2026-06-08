#!/usr/bin/env python3
"""v2.17.9: Anti-cheat system — runtime seal, integrity audit, equipment/talent validation."""
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


ANTI_CHEAT_BLOCK = (
    "const ANTI_CHEAT_KEY=0x6d755874;let _acSeal=null,_acSnapshot=null,_acWatchdog=null,_acAuditBusy=false;"
    "function acMix(h,v){h=(h^(((v|0)*ANTI_CHEAT_KEY)&0xffffffff))>>>0;h=(h+((h<<5)|(h>>>27)))>>>0;return h>>>0;}"
    "function computePlayerSeal(p){if(!p)return'';let h=0x811c9dc5;"
    "h=acMix(h,p.level);h=acMix(h,p.xp);h=acMix(h,p.gold);h=acMix(h,p.overloadChips||0);"
    "h=acMix(h,p.atk|0);h=acMix(h,p.maxHp|0);h=acMix(h,p.def|0);"
    "let tp=0;TALENT_STATS.forEach(s=>{tp+=(p.talents&&p.talents[s.key])||0;});"
    "h=acMix(h,tp);h=acMix(h,p.talentPoints||0);"
    "h=acMix(h,Array.isArray(p.equipInventory)?p.equipInventory.filter(Boolean).length:0);"
    "let ic=0;for(const id in(p.items||{}))ic+=(p.items[id]||0);h=acMix(h,ic);"
    "return h.toString(16).padStart(8,'0');}"
    "function sealPlayerState(){if(typeof player!=='undefined'&&player&&!isDevAccount())_acSeal=computePlayerSeal(player);}"
    "function captureGoodSaveSnapshot(raw){if(raw&&typeof raw==='string')_acSnapshot=raw;}"
    "function getAffixBounds(stat,isHidden){const pools=[WEAPON_AFFIXES,ARMOR_AFFIXES];"
    "if(isHidden)pools.push(HIDDEN_AFFIXES);let lo=0,hi=99999,found=false;"
    "for(const pool of pools)for(const a of pool)if(a.stat===stat){lo=Math.min(lo,a.min);hi=Math.max(hi,a.max);found=true;}"
    "if(stat==='avoidDeath')return{min:0,max:1};return found?{min:lo,max:hi}:{min:0,max:99999};}"
    "function validateEquipmentItem(eq){if(!eq||!eq.id||!eq.type||!eq.rarity)return false;"
    "if(!['common','rare','epic','legendary','hidden'].includes(eq.rarity))return false;"
    "if(eq.level<1||eq.level>2000)return false;if(eq.upgradeLv!=null&&(eq.upgradeLv<0||eq.upgradeLv>50))return false;"
    "if(!Array.isArray(eq.affixes))return false;"
    "const maxAff=(RARITY_AFFIX_COUNT[eq.rarity]||3)+2;if(eq.affixes.length>maxAff)return false;"
    "for(const a of eq.affixes){if(!a||!a.stat)return false;const b=getAffixBounds(a.stat,eq.rarity==='hidden');"
    "const v=Number(a.value);const tol=eq.rarity==='hidden'?b.max*0.35:Math.max(5,b.max*0.25);"
    "if(!Number.isFinite(v)||v<b.min-tol||v>b.max+tol+(eq.upgradeLv||0)*5)return false;}return true;}"
    "function validateAllEquipment(){let ok=true;const fix=eq=>{if(eq&&!validateEquipmentItem(eq)){bugClientSignals.add('invalid_equipment');ok=false;return null;}return eq;};"
    "for(const slot in player.equipment)player.equipment[slot]=fix(player.equipment[slot]);"
    "player.equipInventory=player.equipInventory.map(eq=>fix(eq));return ok;}"
    "function getTalentBudgetUsed(){let spent=0;TALENT_STATS.forEach(s=>{spent+=(player.talents[s.key]||0);});return spent+(player.talentPoints||0);}"
    "function getTalentBudgetMax(){return Math.max(0,(player.level||1)-1);}"
    "function validateTalentBudget(){if(getTalentBudgetUsed()<=getTalentBudgetMax()+2)return true;bugClientSignals.add('talent_overflow');return false;}"
    "function validateStatDerivation(){const atk=player.atk,def=player.def,maxHp=player.maxHp,spd=player.spd;"
    "recalcPlayerStats();const drift=Math.abs(player.atk-atk)+Math.abs(player.def-def)+Math.abs(player.maxHp-maxHp)+Math.abs(player.spd-spd);"
    "if(drift>2){bugClientSignals.add('stat_inflation');return false;}return true;}"
    "function validateProgressBounds(){let ok=true;const peak=Math.floor(Number(player.stats&&player.stats.peakLevel)||0);"
    "const lv=Math.floor(Number(player.level)||1);if(lv>peak+1){bugClientSignals.add('level_overflow');player.level=Math.max(1,peak);ok=false;}"
    "if(player.xp<0){player.xp=0;ok=false;}if(player.xp>(player.xpToNext||1)*1.5){bugClientSignals.add('xp_overflow');player.xp=Math.min(player.xp,Math.max(0,(player.xpToNext||1)-1));ok=false;}"
    "if(player.gold<0){player.gold=0;ok=false;}if(player.gold>999999999){bugClientSignals.add('gold_overflow');player.gold=999999999;ok=false;}"
    "if((player.overloadChips||0)<0){player.overloadChips=0;ok=false;}return ok;}"
    "function verifyPlayerSeal(){if(isDevAccount()||!_acSeal)return true;"
    "if(computePlayerSeal(player)!==_acSeal){bugClientSignals.add('runtime_tamper');return false;}return true;}"
    "function rollbackFromSnapshot(){if(!_acSnapshot)return false;try{const data=JSON.parse(_acSnapshot);const expected=data.checksum;delete data.checksum;"
    "if(generateChecksum(data)!==expected)return false;"
    "if(getSessionKey())setAccountSaveRaw(_acSnapshot);else localStorage.setItem('td_full_save',_acSnapshot);return loadGame();}catch(e){return false;}}"
    "function repairPlayerIntegrity(reason){initTalentPoints();reconcilePlayerXpProgress({skipRecalc:true});validateAllEquipment();recalcPlayerStats();updateDroneStats();"
    "if(reason==='runtime_tamper'||reason==='stat_inflation'||reason==='talent_overflow'){"
    "if(rollbackFromSnapshot()){logInfo(t('antiCheatRollback'));renderAllPanels();updateStatusBar();sealPlayerState();return true;}}"
    "sealPlayerState();renderAllPanels();updateStatusBar();return true;}"
    "function auditPlayerIntegrity(opts={}){if(_acAuditBusy||typeof player==='undefined'||!player||isDevAccount())return true;"
    "_acAuditBusy=true;let tampered=false,reason='';try{"
    "if(!verifyPlayerSeal()){tampered=true;reason='runtime_tamper';}"
    "if(!validateProgressBounds())tampered=true;if(!validateTalentBudget()){tampered=true;if(!reason)reason='talent_overflow';}"
    "if(!validateAllEquipment())tampered=true;if(!validateStatDerivation()){tampered=true;if(!reason)reason='stat_inflation';}"
    "if(tampered&&opts.repair!==false)repairPlayerIntegrity(reason);else if(!tampered)sealPlayerState();"
    "}finally{_acAuditBusy=false;}return !tampered;}"
    "function startAntiCheatWatchdog(){if(_acWatchdog||isDevAccount())return;"
    "_acWatchdog=setInterval(()=>{if(!document.hidden&&!gameOver)auditPlayerIntegrity();},12000);}"
    "function stopAntiCheatWatchdog(){if(_acWatchdog){clearInterval(_acWatchdog);_acWatchdog=null;}}"
)

# version
rep("GAME_VERSION='2.17.8'", "GAME_VERSION='2.17.9'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.17.8',date:'2026-06-08',summary:{zh:'v2.17.8 實機測試修復：版本提示不阻擋操作、離線可註冊本機帳號、開發帳號等級顯示與重複日誌。',en:'v2.17.8 audit fixes: non-blocking version notice, offline local registration, dev level flash and duplicate log.'}},",
    "GAME_VERSION_HISTORY=[{version:'2.17.9',date:'2026-06-08',summary:{zh:'v2.17.9 防作弊系統：執行期狀態封印、裝備／天賦驗證、異常自動回復上次合法存檔。',en:'v2.17.9 anti-cheat: runtime state seal, equipment/talent validation, auto-rollback on tamper.'}},{version:'2.17.8',date:'2026-06-08',summary:{zh:'v2.17.8 實機測試修復：版本提示不阻擋操作、離線可註冊本機帳號、開發帳號等級顯示與重複日誌。',en:'v2.17.8 audit fixes: non-blocking version notice, offline local registration, dev level flash and duplicate log.'}},",
    "hist",
)
rep("SAVE_VERSION=54", "SAVE_VERSION=55", "save")

# i18n
rep(
    'logBalanceV2178:"[修復 v2.17.8] 版本提示不阻擋操作、離線可註冊本機帳號、修正開發帳號等級閃爍與重複更新日誌。",logBalanceV2177:',
    'logBalanceV2179:"[安全 v2.17.9] 防作弊系統：偵測本地變數竄改、驗證裝備與天賦、異常時回復合法存檔。",logBalanceV2178:"[修復 v2.17.8] 版本提示不阻擋操作、離線可註冊本機帳號、修正開發帳號等級閃爍與重複更新日誌。",logBalanceV2177:',
    "i18n zh log",
)
rep(
    'logBalanceV2178:"[Fix v2.17.8] Non-blocking version notice, offline local registration, dev level flash and duplicate update log.",logBalanceV2177:',
    'logBalanceV2179:"[Security v2.17.9] Anti-cheat: detect local variable tampering, validate gear/talents, rollback on anomaly.",logBalanceV2178:"[Fix v2.17.8] Non-blocking version notice, offline local registration, dev level flash and duplicate update log.",logBalanceV2177:',
    "i18n en log",
)
rep(
    'registerThinkAgain:"再想想",registerLocalOnly:',
    'antiCheatRollback:"[安全] 偵測到異常數值，已回復至上次合法存檔。",registerThinkAgain:"再想想",registerLocalOnly:',
    "i18n zh ac",
)
rep(
    'registerThinkAgain:"THINK AGAIN",registerLocalOnly:',
    'antiCheatRollback:"[Security] Abnormal values detected — restored last valid save.",registerThinkAgain:"THINK AGAIN",registerLocalOnly:',
    "i18n en ac",
)

# anti-cheat module before checksum
rep(
    "function generateChecksum(data){",
    ANTI_CHEAT_BLOCK + "function generateChecksum(data){",
    "anti-cheat block",
)

# saveGame: audit before save, snapshot after
rep(
    "function saveGame(){if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};reconcilePlayerXpProgress({skipRecalc:true});initTalentPoints();",
    "function saveGame(){if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};auditPlayerIntegrity({repair:true});reconcilePlayerXpProgress({skipRecalc:true});initTalentPoints();",
    "save audit",
)
rep(
    "state.checksum=generateChecksum(state);try{if(getSessionKey()){setAccountSaveRaw(JSON.stringify(state));}else{localStorage.setItem('td_full_save',JSON.stringify(state));}}catch(e){}scheduleLeaderboardPublish();}",
    "state.checksum=generateChecksum(state);const _saveJson=JSON.stringify(state);try{if(getSessionKey()){setAccountSaveRaw(_saveJson);}else{localStorage.setItem('td_full_save',_saveJson);}captureGoodSaveSnapshot(_saveJson);sealPlayerState();}catch(e){}scheduleLeaderboardPublish();}",
    "save snapshot",
)

# loadGame: snapshot + seal on success
rep(
    "leaderboardTrackedLevel=-1;publishLeaderboardEntry(true);return true;}catch(e){return false;}}function applyPlayerDefaults(p){",
    "leaderboardTrackedLevel=-1;publishLeaderboardEntry(true);captureGoodSaveSnapshot(raw);sealPlayerState();return true;}catch(e){return false;}}function applyPlayerDefaults(p){",
    "load seal",
)

# loadGame: v2179 notice
rep(
    "const _balanceV2178Notice=!!data._balanceV2178Notice;delete data._balanceV2178Notice;if(data.autoHerbSettings)",
    "const _balanceV2178Notice=!!data._balanceV2178Notice;delete data._balanceV2178Notice;const _balanceV2179Notice=!!data._balanceV2179Notice;delete data._balanceV2179Notice;if(data.autoHerbSettings)",
    "load notice var",
)
rep(
    "if(_balanceV2178Notice)logInfo(t('logBalanceV2178'));logInfo(t('logBalanceV2175'));",
    "if(_balanceV2178Notice)logInfo(t('logBalanceV2178'));if(_balanceV2179Notice)logInfo(t('logBalanceV2179'));logInfo(t('logBalanceV2175'));",
    "load log",
)

# migrate v55
rep(
    "function migrateSave(data){if(data.version<54){",
    "function migrateSave(data){if(data.version<55){data._balanceV2179Notice=true;data.version=55;}if(data.version<54){",
    "migrate",
)

# combat: lightweight seal check
rep(
    "function queueAttack(useMain){if(isVersionUpdateBlocking())return;if(!inCombat||!currentEnemy||gameOver||player.isPermanentlyDead||isProcessingQueue)return;",
    "function queueAttack(useMain){if(isVersionUpdateBlocking())return;if(!verifyPlayerSeal()){auditPlayerIntegrity();return;}if(!inCombat||!currentEnemy||gameOver||player.isPermanentlyDead||isProcessingQueue)return;",
    "combat seal",
)

# collectBugClientSignals: extra checks
rep(
    "if(peak>lv)signals.add('peak_level_mismatch');const cloudSt=document.getElementById('cloud-sync-status');",
    "if(peak>lv)signals.add('peak_level_mismatch');if(typeof getTalentBudgetUsed==='function'&&getTalentBudgetUsed()>getTalentBudgetMax()+2)signals.add('talent_overflow');if(typeof _acSeal!=='undefined'&&_acSeal&&typeof computePlayerSeal==='function'&&computePlayerSeal(player)!==_acSeal)signals.add('runtime_tamper');const cloudSt=document.getElementById('cloud-sync-status');",
    "signals",
)

# initGame: seal + watchdog on both new-game and loaded-save paths
rep(
    "startPlaytimeCounter();ensureChatLazyInit();initVersionWatch();applyPendingOverloadPayment().catch(()=>{});};if(!savedName",
    "startPlaytimeCounter();sealPlayerState();startAntiCheatWatchdog();ensureChatLazyInit();initVersionWatch();applyPendingOverloadPayment().catch(()=>{});};if(!savedName",
    "watchdog new game",
)
rep(
    "logInfo('存檔已載入');}}player.hp=clamp(player.hp,0,player.maxHp);renderAllPanels();updateStatusBar();updateButtons();switchTab('log');if(!player.shopItems||player.shopItems.length===0||Date.now()>=player.shopRefreshTime){refreshShop();}startPlaytimeCounter();ensureChatLazyInit();applyPendingOverloadPayment().catch(()=>{});}btnAtkMain.addEventListener",
    "logInfo('存檔已載入');}}player.hp=clamp(player.hp,0,player.maxHp);renderAllPanels();updateStatusBar();updateButtons();switchTab('log');if(!player.shopItems||player.shopItems.length===0||Date.now()>=player.shopRefreshTime){refreshShop();}startPlaytimeCounter();sealPlayerState();startAntiCheatWatchdog();ensureChatLazyInit();initVersionWatch();applyPendingOverloadPayment().catch(()=>{});}btnAtkMain.addEventListener",
    "watchdog loaded save",
)

# throttleSave: audit before scheduling save in combat path - actually saveGame already audits

# bug catalog
rep(
    "const LOCAL_KNOWN_BUG_FIXES={'level-rollback':'2.17.6','cloud-sync-fail':'2.17.1','xp-bar-stale':'2.6.6','leaderboard-stale':'2.8.6'};",
    "const LOCAL_KNOWN_BUG_FIXES={'level-rollback':'2.17.6','cloud-sync-fail':'2.17.1','xp-bar-stale':'2.6.6','leaderboard-stale':'2.8.6','runtime-tamper':'2.17.9','stat-inflation':'2.17.9','invalid-equipment':'2.17.9'};",
    "bug fixes",
)

INDEX.write_text(text, encoding="utf-8")
print("OK: patched index.html -> v2.17.9 anti-cheat")
