#!/usr/bin/env python3
"""Apply v2.11.1 optional curse + weekend double curse + hell decay gate."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:240]}")
    s = s.replace(old, new, 1)


rep("GAME_VERSION='2.11.0'", "GAME_VERSION='2.11.1'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.11.0'",
    "GAME_VERSION_HISTORY=[{version:'2.11.1',date:'2026-06-07',summary:{zh:'v2.11.1 詛咒可選挑戰、週末雙詛咒、崩壞 70% 以上禁止進地獄。',en:'v2.11.1 optional curse challenge, weekend double curse, hell blocked at 70%+ decay.'}},{version:'2.11.0'",
    "hist",
)
rep("SAVE_VERSION=39", "SAVE_VERSION=40", "save")

rep(
    "MEMORY_DECAY_CURSE_CLEAR_BONUS=2,ESCAPE_DECAY_SUCCESS=1.2",
    "MEMORY_DECAY_CURSE_CLEAR_BONUS=2,MEMORY_DECAY_HELL_BLOCK=70,ESCAPE_DECAY_SUCCESS=1.2",
    "hell block const",
)

# i18n zh
rep(
    'dailyCursePreview:"今日詛咒地城: {0}",curseBleed:"裂血"',
    'dailyCursePreview:"今日詛咒: {0}",weekendDoubleCurse:"週末雙詛咒: {0} + {1}",curseOptInLabel:"☠ 接受詛咒挑戰",curseOptInHint:"勾選後套用今日詛咒；週末再加第二道。通關額外減崩壞。",hellDecayBlocked:"崩壞 {0}% 以上禁止進入地獄（目前 {1}%）",logBalanceV2111:"[平衡 v2.11.1] 詛咒改為可選挑戰；週末雙詛咒；崩壞 70% 以上禁止進地獄。",curseBleed:"裂血"',
    "i18n zh",
)
# i18n en
rep(
    'dailyCursePreview:"Today\'s cursed dungeon: {0}",curseBleed:"Bleed"',
    'dailyCursePreview:"Today\'s curse: {0}",weekendDoubleCurse:"Weekend double curse: {0} + {1}",curseOptInLabel:"☠ Accept curse challenge",curseOptInHint:"Applies today\'s curse; weekends add a second. Clear bonus decay relief.",hellDecayBlocked:"Hell blocked at {0}%+ decay (current {1}%)",logBalanceV2111:"[Balance v2.11.1] Optional curse challenge; weekend double curse; hell blocked at 70%+ decay.",curseBleed:"Bleed"',
    "i18n en",
)

rep(
    "function getDailyCurse(){const key=new Date().toDateString();let h=0;for(let i=0;i<key.length;i++)h=((h<<5)-h)+key.charCodeAt(i)|0;return{...DAILY_CURSES[Math.abs(h)%DAILY_CURSES.length]};}function getDailyCurseLabel(){return t(getDailyCurse().labelKey);}function rollDungeonModifiers(tier){const n=tier==='hell'?3:tier==='hard'?2:1;const rolled=shuffleArray(DUNGEON_MODIFIERS).slice(0,n);rolled.push(getDailyCurse());return rolled;}",
    "function isWeekend(){const d=new Date().getDay();return d===0||d===6;}function getDailyCurse(){const key=new Date().toDateString();let h=0;for(let i=0;i<key.length;i++)h=((h<<5)-h)+key.charCodeAt(i)|0;return{...DAILY_CURSES[Math.abs(h)%DAILY_CURSES.length]};}function getSecondDailyCurse(primary){const key=new Date().toDateString()+'_2';let h=0;for(let i=0;i<key.length;i++)h=((h<<5)-h)+key.charCodeAt(i)|0;let idx=Math.abs(h)%DAILY_CURSES.length;if(DAILY_CURSES[idx].id===primary.id)idx=(idx+1)%DAILY_CURSES.length;return{...DAILY_CURSES[idx]};}function getDailyCurseLabel(){return t(getDailyCurse().labelKey);}function getDailyCursePreviewLabels(){const primary=getDailyCurse();if(isWeekend()){const second=getSecondDailyCurse(primary);return t('weekendDoubleCurse',t(primary.labelKey),t(second.labelKey));}return t('dailyCursePreview',t(primary.labelKey));}function isHellBlockedByDecay(){return(player.memoryDecay||0)>=MEMORY_DECAY_HELL_BLOCK;}function rollDungeonModifiers(tier,acceptCurse){const n=tier==='hell'?3:tier==='hard'?2:1;const rolled=shuffleArray(DUNGEON_MODIFIERS).slice(0,n);if(acceptCurse){const primary=getDailyCurse();rolled.push(primary);if(isWeekend())rolled.push(getSecondDailyCurse(primary));}return rolled;}",
    "curse funcs",
)

rep(
    "function hasActiveDailyCurse(){return!!(currentDungeon&&currentDungeon.modifiers&&currentDungeon.modifiers.some(m=>m.isCurse));}",
    "function hasActiveDailyCurse(){return!!(currentDungeon&&currentDungeon.curseAccepted&&currentDungeon.modifiers&&currentDungeon.modifiers.some(m=>m.isCurse));}",
    "has curse",
)

rep(
    "function formatDungeonModifierList(){if(!currentDungeon||!currentDungeon.modifiers||!currentDungeon.modifiers.length)return'';const curse=currentDungeon.modifiers.find(m=>m.isCurse);const rest=currentDungeon.modifiers.filter(m=>!m.isCurse).map(m=>t(m.labelKey)).join(' · ');const cursePart=curse?t('dailyCurseTag',t(curse.labelKey)):'';return cursePart?(rest?cursePart+' · '+rest:cursePart):rest;}",
    "function formatDungeonModifierList(){if(!currentDungeon||!currentDungeon.modifiers||!currentDungeon.modifiers.length)return'';const curses=currentDungeon.modifiers.filter(m=>m.isCurse);const rest=currentDungeon.modifiers.filter(m=>!m.isCurse).map(m=>t(m.labelKey)).join(' · ');const cursePart=curses.length?curses.map(c=>t('dailyCurseTag',t(c.labelKey))).join(' · '):'';return cursePart?(rest?cursePart+' · '+rest:cursePart):rest;}",
    "format mods",
)

rep(
    "function generateDungeon(tierLevel,tier){const layout=pick(DUNGEON_LAYOUTS),modifiers=rollDungeonModifiers(tier);currentDungeon={tierLevel,tier,floorLevel:tierLevel*TIERS_PER_LEVEL-2,layout,modifiers};",
    "function generateDungeon(tierLevel,tier,acceptCurse){const layout=pick(DUNGEON_LAYOUTS),modifiers=rollDungeonModifiers(tier,!!acceptCurse);currentDungeon={tierLevel,tier,floorLevel:tierLevel*TIERS_PER_LEVEL-2,layout,modifiers,curseAccepted:!!acceptCurse};",
    "generate",
)

rep(
    "function showDifficultySelection(tierLevel){const diffInfo=document.getElementById('difficulty-info');const diffList=document.getElementById('difficulty-list');const levelStart=tierLevel*TIERS_PER_LEVEL-2;const levelEnd=tierLevel*TIERS_PER_LEVEL;diffInfo.innerHTML=`<div style=\"color:var(--accent);\">已選擇地城等級: Lv.${levelStart} - ${levelEnd}</div><div style=\"color:#888;font-size:0.55rem;margin-top:0.35rem;\">${t('diffVarietyHint')}</div><div style=\"color:var(--decay);font-size:0.55rem;margin-top:0.3rem;\">${t('dailyCursePreview',getDailyCurseLabel())}</div>`;diffList.innerHTML='';const difficulties=[{tier:'normal',cssClass:'normal-diff',nameKey:'diffNormalName',descKey:'diffNormalDesc',mult:'x1.0',color:'#888'},{tier:'hard',cssClass:'hard-diff',nameKey:'diffHardName',descKey:'diffHardDesc',mult:'x1.8',color:'#fff'},{tier:'hell',cssClass:'hell-diff',nameKey:'diffHellName',descKey:'diffHellDesc',mult:'x3.0',color:'#ff4444',requiresTicket:true}];difficulties.forEach(diff=>{const btn=document.createElement('button');btn.className=`difficulty-btn ${diff.cssClass}`;btn.innerHTML=`<span class=\"diff-name\" style=\"color:${diff.color}\">${t(diff.nameKey)}</span><span class=\"diff-mult\">${diff.mult}</span><span class=\"diff-desc\">${t(diff.descKey)}</span>${diff.requiresTicket?`<span class=\"diff-desc\" style=\"color:#ff4444;\">${t('diffTicketReq',getItemQty('hellTicket'))}</span>`:''}`;btn.addEventListener('click',()=>{if(diff.requiresTicket&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡！');return;}difficultyOverlay.style.display='none';dungeonOverlay.style.display='none';startDungeon(tierLevel,diff.tier);});diffList.appendChild(btn);});difficultyOverlay.style.display='flex';",
    "function showDifficultySelection(tierLevel){const diffInfo=document.getElementById('difficulty-info');const diffList=document.getElementById('difficulty-list');const levelStart=tierLevel*TIERS_PER_LEVEL-2;const levelEnd=tierLevel*TIERS_PER_LEVEL;const decay=(player.memoryDecay||0);const hellBlocked=isHellBlockedByDecay();diffInfo.innerHTML=`<div style=\"color:var(--accent);\">已選擇地城等級: Lv.${levelStart} - ${levelEnd}</div><div style=\"color:#888;font-size:0.55rem;margin-top:0.35rem;\">${t('diffVarietyHint')}</div><label class=\"curse-opt-in\"><input type=\"checkbox\" id=\"curse-opt-in\"><span>${t('curseOptInLabel')}</span></label><div id=\"curse-preview\" style=\"color:var(--decay);font-size:0.55rem;margin-top:0.3rem;display:none;\">${getDailyCursePreviewLabels()}</div><div style=\"color:#666;font-size:0.5rem;margin-top:0.25rem;\">${t('curseOptInHint')}</div>${hellBlocked?`<div style=\"color:var(--decay);font-size:0.55rem;margin-top:0.3rem;\">${t('hellDecayBlocked',MEMORY_DECAY_HELL_BLOCK,decay.toFixed(1))}</div>`:''}`;const curseCb=document.getElementById('curse-opt-in');const cursePreview=document.getElementById('curse-preview');if(curseCb&&cursePreview)curseCb.addEventListener('change',()=>{cursePreview.style.display=curseCb.checked?'':'none';});diffList.innerHTML='';const difficulties=[{tier:'normal',cssClass:'normal-diff',nameKey:'diffNormalName',descKey:'diffNormalDesc',mult:'x1.0',color:'#888'},{tier:'hard',cssClass:'hard-diff',nameKey:'diffHardName',descKey:'diffHardDesc',mult:'x1.8',color:'#fff'},{tier:'hell',cssClass:'hell-diff',nameKey:'diffHellName',descKey:'diffHellDesc',mult:'x3.0',color:'#ff4444',requiresTicket:true}];difficulties.forEach(diff=>{const btn=document.createElement('button');const blocked=diff.tier==='hell'&&hellBlocked;btn.className=`difficulty-btn ${diff.cssClass}${blocked?' hell-blocked':''}`;btn.disabled=blocked;btn.innerHTML=`<span class=\"diff-name\" style=\"color:${diff.color}\">${t(diff.nameKey)}</span><span class=\"diff-mult\">${diff.mult}</span><span class=\"diff-desc\">${t(diff.descKey)}</span>${diff.requiresTicket?`<span class=\"diff-desc\" style=\"color:#ff4444;\">${t('diffTicketReq',getItemQty('hellTicket'))}</span>`:''}${blocked?`<span class=\"diff-desc\" style=\"color:var(--decay);\">${t('hellDecayBlocked',MEMORY_DECAY_HELL_BLOCK,decay.toFixed(1))}</span>`:''}`;btn.addEventListener('click',()=>{if(blocked){logInfo(t('hellDecayBlocked',MEMORY_DECAY_HELL_BLOCK,decay.toFixed(1)));return;}if(diff.requiresTicket&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡！');return;}const acceptCurse=!!document.getElementById('curse-opt-in')?.checked;difficultyOverlay.style.display='none';dungeonOverlay.style.display='none';startDungeon(tierLevel,diff.tier,acceptCurse);});diffList.appendChild(btn);});difficultyOverlay.style.display='flex';",
    "diff ui",
)

rep(
    "function startDungeon(tierLevel,tier){if(isVersionUpdateBlocking())return;if(player.isPermanentlyDead){logInfo('角色已永久死亡，無法進入地城');return;}if(tier==='hell'&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡');return;}const unlockedTier=getUnlockedDungeonTier();if(!isDungeonTierUnlocked(tierLevel)){logInfo(t('dungeonLockedMsg'));logInfo(t('dungeonMaxMsg',unlockedTier*TIERS_PER_LEVEL-2,unlockedTier*TIERS_PER_LEVEL));return;}if(!canEnterDungeonByPlayerLevel(tierLevel)){logInfo(t('dungeonLevelTooHighLog',getTierLevelStart(tierLevel),player.level||1,PLAYER_LEVEL_GAP));return;}if(canOfferDroneAutoBattle(tier)){pendingDungeonStart={tierLevel,tier};document.getElementById('drone-dungeon-overlay').style.display='flex';return;}enterDungeonWithAutoHerbCheck(tierLevel,tier,false);}",
    "function startDungeon(tierLevel,tier,acceptCurse){if(isVersionUpdateBlocking())return;if(player.isPermanentlyDead){logInfo('角色已永久死亡，無法進入地城');return;}if(tier==='hell'&&isHellBlockedByDecay()){logInfo(t('hellDecayBlocked',MEMORY_DECAY_HELL_BLOCK,(player.memoryDecay||0).toFixed(1)));return;}if(tier==='hell'&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡');return;}const unlockedTier=getUnlockedDungeonTier();if(!isDungeonTierUnlocked(tierLevel)){logInfo(t('dungeonLockedMsg'));logInfo(t('dungeonMaxMsg',unlockedTier*TIERS_PER_LEVEL-2,unlockedTier*TIERS_PER_LEVEL));return;}if(!canEnterDungeonByPlayerLevel(tierLevel)){logInfo(t('dungeonLevelTooHighLog',getTierLevelStart(tierLevel),player.level||1,PLAYER_LEVEL_GAP));return;}if(canOfferDroneAutoBattle(tier)){pendingDungeonStart={tierLevel,tier,acceptCurse:!!acceptCurse};document.getElementById('drone-dungeon-overlay').style.display='flex';return;}enterDungeonWithAutoHerbCheck(tierLevel,tier,false,!!acceptCurse);}",
    "start dungeon",
)

rep(
    "function enterDungeonWithAutoHerbCheck(tierLevel,tier,useDrone){if(useDrone||!getAutoHerbSettings().enabled){startDungeonInternal(tierLevel,tier,useDrone);return;}",
    "function enterDungeonWithAutoHerbCheck(tierLevel,tier,useDrone,acceptCurse){if(useDrone||!getAutoHerbSettings().enabled){startDungeonInternal(tierLevel,tier,useDrone,!!acceptCurse);return;}",
    "herb enter 1",
)
rep(
    "startDungeonInternal(tierLevel,tier,useDrone);};if(qty<1){showConfirm(t('autoHerbDungeonEmptyWarn',getItemName(herbId)),proceed);return;}if(qty<20){showConfirm(t('autoHerbDungeonLowWarn',getItemName(herbId),qty),proceed);return;}startDungeonInternal(tierLevel,tier,useDrone);}",
    "startDungeonInternal(tierLevel,tier,useDrone,!!acceptCurse);};if(qty<1){showConfirm(t('autoHerbDungeonEmptyWarn',getItemName(herbId)),proceed);return;}if(qty<20){showConfirm(t('autoHerbDungeonLowWarn',getItemName(herbId),qty),proceed);return;}startDungeonInternal(tierLevel,tier,useDrone,!!acceptCurse);}",
    "herb enter 2",
)

rep(
    "function startDungeonInternal(tierLevel,tier,useDrone){if(tier==='hell')removeItem('hellTicket',1);clearAllTimers();clearDroneTimers();inCombat=false;currentEnemy=null;gameOver=false;attackQueue=[];isProcessingQueue=false;playerAttackCooldownUntil=0;generateDungeon(tierLevel,tier);",
    "function startDungeonInternal(tierLevel,tier,useDrone,acceptCurse){if(tier==='hell')removeItem('hellTicket',1);clearAllTimers();clearDroneTimers();inCombat=false;currentEnemy=null;gameOver=false;attackQueue=[];isProcessingQueue=false;playerAttackCooldownUntil=0;generateDungeon(tierLevel,tier,!!acceptCurse);",
    "start internal",
)

rep(
    "startDungeonInternal(pendingDungeonStart.tierLevel,pendingDungeonStart.tier,true);pendingDungeonStart=null;}});document.getElementById('drone-dungeon-no').addEventListener('click',()=>{document.getElementById('drone-dungeon-overlay').style.display='none';if(pendingDungeonStart){logInfo('無人機進入休眠模式，請手動完成地城');player.drone.active=false;clearDroneTimers();enterDungeonWithAutoHerbCheck(pendingDungeonStart.tierLevel,pendingDungeonStart.tier,false);pendingDungeonStart=null;}});",
    "startDungeonInternal(pendingDungeonStart.tierLevel,pendingDungeonStart.tier,true,!!pendingDungeonStart.acceptCurse);pendingDungeonStart=null;}});document.getElementById('drone-dungeon-no').addEventListener('click',()=>{document.getElementById('drone-dungeon-overlay').style.display='none';if(pendingDungeonStart){logInfo('無人機進入休眠模式，請手動完成地城');player.drone.active=false;clearDroneTimers();enterDungeonWithAutoHerbCheck(pendingDungeonStart.tierLevel,pendingDungeonStart.tier,false,!!pendingDungeonStart.acceptCurse);pendingDungeonStart=null;}});",
    "drone handlers",
)

rep(
    ".hell-diff{border-left:3px solid #f46}",
    ".hell-diff{border-left:3px solid #f46}.curse-opt-in{display:flex;align-items:center;gap:0.35rem;margin-top:0.45rem;font-size:0.55rem;color:var(--decay);cursor:pointer}.curse-opt-in input{accent-color:var(--decay)}.difficulty-btn.hell-blocked{opacity:0.45;cursor:not-allowed;border-color:#333!important}",
    "css",
)

rep(
    "function migrateSave(data){if(data.version<39){data._balanceV211Notice=true;data.version=39;}",
    "function migrateSave(data){if(data.version<40){data._balanceV2111Notice=true;data.version=40;}if(data.version<39){data._balanceV211Notice=true;data.version=39;}",
    "migrate",
)
rep(
    "const _balanceV211Notice=!!data._balanceV211Notice;delete data._balanceV211Notice;",
    "const _balanceV211Notice=!!data._balanceV211Notice;delete data._balanceV211Notice;const _balanceV2111Notice=!!data._balanceV2111Notice;delete data._balanceV2111Notice;",
    "load var",
)
rep(
    "if(_balanceV211Notice)logInfo(t('logBalanceV211'));leaderboardTrackedLevel=-1;",
    "if(_balanceV211Notice)logInfo(t('logBalanceV211'));if(_balanceV2111Notice)logInfo(t('logBalanceV2111'));leaderboardTrackedLevel=-1;",
    "load log",
)

path.write_text(s)
print("v2.11.1 patch OK")
