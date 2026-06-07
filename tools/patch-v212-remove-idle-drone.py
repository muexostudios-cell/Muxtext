#!/usr/bin/env python3
"""Remove idle (挂机) system and all drone battle features (v2.12.0)."""
import re
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:240]}")
    s = s.replace(old, new, 1)


def remove_fn(js: str, name: str) -> str:
    pat = rf"(?:async )?function {re.escape(name)}\([^)]*\)\{{"
    while True:
        m = re.search(pat, js)
        if not m:
            return js
        i = m.end() - 1
        depth = 0
        while i < len(js):
            if js[i] == "{":
                depth += 1
            elif js[i] == "}":
                depth -= 1
                if depth == 0:
                    js = js[: m.start()] + js[i + 1 :]
                    break
            i += 1
    return js


# --- HTML ---
rep('<button class="quick-btn" id="btn-craft-idle">> 掛機系統</button>', "", "btn-craft-idle")
rep(
    '<div id="drone-dungeon-overlay"><div id="drone-dungeon-box"><h3 style="color:#fff;margin-bottom:.5rem">無人機模式</h3><p style="margin-bottom:.8rem">是否為本地城啟用無人機自動戰鬥？</p><p style="color:#aaa;font-size:.5rem;margin-bottom:.8rem">> 啟用後玩家無法操作<br>> 無人機自動完成地城<br>> 掉落物與玩家戰鬥相同<br>> 經驗值和金幣自動獲得<br>> 完成後顯示所有戰利品<br>> 無人機損壞後手動完成地城可自動修復</p><div style="display:flex;gap:.5rem"><button id="drone-dungeon-yes" style="flex:1;padding:.5rem;background:0 0;border:1px solid #fff;color:#fff;cursor:pointer;font-family:inherit">啟用無人機</button><button id="drone-dungeon-no" style="flex:1;padding:.5rem;background:0 0;border:1px solid #555;color:#555;cursor:pointer;font-family:inherit">手動戰鬥</button></div><button id="drone-dungeon-cancel" style="width:100%;margin-top:.5rem;padding:.3rem;background:0 0;border:1px solid #333;color:#666;cursor:pointer;font-family:inherit">返回</button></div></div>\n',
    "",
    "drone-dungeon-overlay",
)
rep(
    '<div id="drone-result-overlay"><div id="drone-result-box"><h3 style="color:#fff;text-align:center;margin-bottom:.5rem;border-bottom:1px solid #333;padding-bottom:.3rem">無人機完成地城！</h3><div id="drone-result-content"></div><div style="display:flex;gap:.5rem;margin-top:.8rem"><button id="drone-result-claim" style="flex:1;padding:.5rem;background:0 0;border:1px solid #fff;color:#fff;cursor:pointer;font-family:inherit">放入背包</button><button id="drone-result-discard" style="flex:1;padding:.5rem;background:0 0;border:1px solid #333;color:#666;cursor:pointer;font-family:inherit">丟棄所有物品</button></div></div></div>\n',
    "",
    "drone-result-overlay",
)

start = s.find('<div id="craft-idle-panel">')
if start < 0:
    raise SystemExit("craft-idle-panel not found")
depth = 0
i = start
while i < len(s):
    if s[i : i + 4] == "<div":
        depth += 1
        i = s.find(">", i) + 1
    elif s[i : i + 6] == "</div>":
        depth -= 1
        if depth == 0:
            s = s[:start] + s[i + 6 :]
            break
        i += 6
    else:
        i += 1

rep(
    '<div class="profile-stat"><span id="profile-craft-idle-label">合成台掛機等級:</span> <span id="profile-craft-idle-level">1</span></div><div class="profile-stat"><span id="profile-drone-idle-label">無人機掛機等級:</span> <span id="profile-drone-idle-level">1</span></div>',
    "",
    "profile idle stats",
)

# --- CSS chunks ---
for chunk in [
    "#craft-idle-panel,#craft-idle-panel.show",
    "#craft-idle-panel{",
    "#craft-idle-progress{",
    ".time-btn-grid{",
    ".time-btn{",
    ".time-btn.active{",
    "#drone-dungeon-overlay{",
    "#drone-dungeon-box{",
    "#drone-result-overlay{",
    "#drone-result-box{",
    "#confirm-btns button.confirm-drone{",
    "#drone-status{",
    ".cell.drone-pos{",
    ".cell.drone-locked{",
    ".battle-msg.drone-msg{",
]:
    idx = s.find(chunk)
    if idx >= 0:
        end = s.find("}", idx) + 1
        s = s[:idx] + s[end:]

# --- JS ---
m = re.search(r"<script>(.*?)</script>", s, re.DOTALL)
if not m:
    raise SystemExit("script not found")
js = m.group(1)

# Idle block
idle_start = js.find("const IDLE_TIME_OPTIONS")
idle_end = js.find("function getIdleConflictMessage")
if idle_start >= 0 and idle_end >= 0:
    idle_end = js.find("}", idle_end) + 1
    js = js[:idle_start] + js[idle_end:]

for fn in [
    "startDroneAI",
    "droneSeekEnemy",
    "handleDroneBagFull",
    "isDroneBagFull",
    "grantDroneCompanionKillRewards",
    "retrieveDroneItems",
    "addToDroneBag",
    "showDroneFullConfirm",
    "canOfferDroneAutoBattle",
    "updateDroneDungeonTabLocks",
    "applyDroneDungeonPanelLock",
    "startDroneAutoDungeon",
    "killDroneEnemy",
    "finishDroneDungeon",
    "showDroneDungeonResult",
    "summarizeDroneDungeonLoot",
    "renderDroneDungeonLootHtml",
    "getDroneMaterialName",
    "clampCraftStationLevel",
    "updateCraftIdleDisplay",
    "clampDroneIdleLevel",
    "updateDroneIdleDisplay",
]:
    js = remove_fn(js, fn)

js = js.replace(
    "function getCraftMaxLevel(){return Math.max(1,player.level||1);}",
    "function getCraftMaxLevel(){return Math.max(1,player.level||1);}function clampCraftStationLevel(){const maxLv=getCraftMaxLevel();if(!player.craftLevel||player.craftLevel<1)player.craftLevel=1;if(player.craftLevel>maxLv)player.craftLevel=maxLv;}",
)

# Version
js = js.replace("GAME_VERSION='2.11.0'", "GAME_VERSION='2.12.0'")
js = js.replace(
    "GAME_VERSION_HISTORY=[{version:'2.11.0'",
    "GAME_VERSION_HISTORY=[{version:'2.12.0',date:'2026-06-07',summary:{zh:'v2.12 移除掛機系統與無人機戰鬥（含自動地城與伴侶戰鬥）。',en:'v2.12 removed idle system and all drone battle features.'}},{version:'2.11.0'",
)
js = js.replace("SAVE_VERSION=39", "SAVE_VERSION=41")
js = js.replace(
    'logBalanceV211:"[平衡 v2.11] 崩壞懲罰加重；詞綴強化；每日詛咒地城（入場顯示、通關額外減崩壞）。",',
    'logBalanceV212:"[更新 v2.12] 已移除掛機系統與無人機戰鬥功能。",logBalanceV211:"[平衡 v2.11] 崩壞懲罰加重；詞綴強化；每日詛咒地城（入場顯示、通關額外減崩壞）。",',
)
js = js.replace(
    'logBalanceV211:"[Balance v2.11] Stronger decay penalty; harsher modifiers; daily cursed dungeon with clear bonus.",',
    'logBalanceV212:"[Update v2.12] Idle system and drone battle features removed.",logBalanceV211:"[Balance v2.11] Stronger decay penalty; harsher modifiers; daily cursed dungeon with clear bonus.",',
)

# Globals
js = js.replace(
    "let pendingDungeonStart=null,droneDungeonActive=false,autoHerbWarnState={},droneDungeonItems=[];",
    "let autoHerbWarnState={};",
)
js = js.replace("let droneSeekInterval=null,droneAttackInterval=null,", "")
for const in [
    "DRONE_AUTO_GOLD_MULT",
    "DRONE_AUTO_XP_MULT",
    "DRONE_AUTO_EQUIP_DROP_MULT",
    "DRONE_COMPANION_GOLD_MULT",
    "DRONE_COMPANION_XP_MULT",
    "DRONE_COMPANION_EQUIP_CHANCE",
    "DRONE_COMPANION_BOSS_EQUIP_CHANCE",
    "DRONE_TARGET_LOCK_DELAY_MS",
    "DRONE_IDLE_UNLOCK_HARD",
    "DRONE_IDLE_UNLOCK_HELL",
    "DRONE_IDLE_XP_RATE",
]:
    js = re.sub(rf",?{const}=[^,;]+", "", js)

js = js.replace(
    "inDungeon,bossDefeated,bossLeaveAvailable,droneDungeonActive,droneDungeonItems,lockedEquipment",
    "inDungeon,bossDefeated,bossLeaveAvailable,lockedEquipment",
)

# startDungeon
js = js.replace(
    "if(canOfferDroneAutoBattle(tier)){pendingDungeonStart={tierLevel,tier};document.getElementById('drone-dungeon-overlay').style.display='flex';return;}enterDungeonWithAutoHerbCheck(tierLevel,tier,false);",
    "enterDungeonWithAutoHerbCheck(tierLevel,tier);",
)

# Replace startDungeonInternal + remove drone overlay listeners (before signature-wide replace)
_si = js.find("function startDungeonInternal(tierLevel,tier,useDrone)")
_dr = js.find("const DRONE_DUNGEON_ALLOWED_TABS=", _si)
if _si < 0 or _dr < 0:
    raise SystemExit(f"startDungeonInternal markers not found si={_si} dr={_dr}")
_old_internal = js[_si : _dr + len("const DRONE_DUNGEON_ALLOWED_TABS=['log','craft','profile'];")]
new_internal = (
    "function startDungeonInternal(tierLevel,tier){if(tier==='hell')removeItem('hellTicket',1);clearAllTimers();inCombat=false;currentEnemy=null;gameOver=false;attackQueue=[];isProcessingQueue=false;playerAttackCooldownUntil=0;generateDungeon(tierLevel,tier);trackDungeonRunStart(tierLevel,tier);const entryDecay=getDungeonModFlat('decayOnEntry');if(entryDecay>0){player.memoryDecay=Math.min(100,parseFloat(((player.memoryDecay||0)+entryDecay).toFixed(1)));logInfo(t('logCurseEntry',entryDecay));}recalcPlayerStats();const hpStart=getDungeonModMult('playerHpStart');player.hp=hpStart<1?Math.floor(player.maxHp*hpStart):player.maxHp;player.shield=player.maxShield;player.drone.active=false;const tierName=currentLang==='zh'?{normal:'普通',hard:'困難',hell:'地獄'}[tier]:tier.toUpperCase();logEl.innerHTML='';logInfo(t('msgEnterDungeon',tierName,currentDungeon.floorLevel,currentDungeon.floorLevel+2,monstersRemaining));logDungeonRunVariety();logInfo('擊殺BOSS即可解鎖出口');battleScreen.classList.remove('active');document.getElementById('map-container').style.display='flex';setLogVisible(true);quickBtns.classList.add('hidden');renderMap();updateDungeonRunBanner();updateStatusBar();updateButtons();throttleSave();}"
)
js = js.replace(_old_internal, new_internal)

# enterDungeonWithAutoHerbCheck
js = js.replace("function enterDungeonWithAutoHerbCheck(tierLevel,tier,useDrone){", "function enterDungeonWithAutoHerbCheck(tierLevel,tier){")
js = js.replace("if(useDrone||!getAutoHerbSettings().enabled){startDungeonInternal(tierLevel,tier,useDrone);return;}", "if(!getAutoHerbSettings().enabled){startDungeonInternal(tierLevel,tier);return;}")
js = js.replace("startDungeonInternal(tierLevel,tier,useDrone)", "startDungeonInternal(tierLevel,tier)")

# Remove DRONE_* const groups after startDungeonInternal rewrite
js = re.sub(r"const DRONE_DUNGEON_ALLOWED_TABS=\[[^\]]+\];", "", js)
js = re.sub(r"const DRONE_LOOT_MATERIAL_ORDER=\[[^\]]+\],DRONE_LOOT_RARITY_ORDER=\[[^\]]+\],DRONE_LOOT_EQUIP_TYPE_ORDER=\[[^\]]+\];", "", js)

# drone result listeners
js = js.replace(
    "document.getElementById('drone-result-claim').addEventListener('click',()=>{document.getElementById('drone-result-overlay').style.display='none';const items=droneDungeonItems.slice();droneDungeonItems=[];items.forEach(item=>{if(item.type==='equip')addToEquipInventory(item.data);else if(item.type==='material')addItem(item.id,item.qty);else if(item.type==='gold')player.gold+=item.qty;else if(item.type==='xp')addXp(item.qty);});renderAllPanels();updateStatusBar();logInfo(t('dronePutInBag'));throttleSave();});document.getElementById('drone-result-discard').addEventListener('click',()=>{document.getElementById('drone-result-overlay').style.display='none';droneDungeonItems=[];logInfo('已丟棄無人機戰利品');throttleSave();});",
    "",
)

# Guards and UI
js = js.replace("||droneDungeonActive", "")
js = js.replace("droneDungeonActive||", "")
js = js.replace("&&droneDungeonActive", "")
js = js.replace("droneDungeonActive&&", "")
js = js.replace("if(isDesktopLayout()&&tab==='log'&&!droneDungeonActive)tab='equip';", "if(isDesktopLayout()&&tab==='log')tab='equip';")
js = js.replace("if(droneDungeonActive&&!DRONE_DUNGEON_ALLOWED_TABS.includes(tab)&&tab!=='chat')return;", "")
js = js.replace("if(droneDungeonActive)updateDroneDungeonTabLocks();", "")
js = js.replace("craftIdlePanel.classList.remove('show');", "")
js = js.replace("craftIdlePanel.classList.add('show');", "")
js = js.replace("else if(currentTab==='log'||currentTab==='craftIdle'||!", "else if(currentTab==='log'||!")
js = re.sub(r"if\(tab==='craftIdle'\)\{[^}]+\}", "", js)
js = js.replace(",droneLocked:false", "")

js = js.replace(
    "function clearDroneTimers(){if(droneSeekInterval){clearInterval(droneSeekInterval);droneSeekInterval=null;}if(droneAttackInterval){clearInterval(droneAttackInterval);droneAttackInterval=null;}}",
    "function clearDroneTimers(){}",
)
js = js.replace("if(player.drone){droneStatus.style.display='';", "if(false&&player.drone){droneStatus.style.display='';")
js = js.replace("droneDungeonActive=false;droneDungeonItems=[];", "")
js = js.replace("updateCraftIdleDisplay();updateDroneIdleDisplay();", "")
js = js.replace("clampCraftStationLevel();clampDroneIdleLevel();", "clampCraftStationLevel();")
js = js.replace("craftIdlePanel=document.getElementById('craft-idle-panel'),", "")
js = js.replace(",craftIdlePanel", "")

# Listeners
js = re.sub(
    r"document\.getElementById\('btn-craft-idle'\)\.addEventListener\('click',\(\)=>\{[^}]+\}\);",
    "",
    js,
)
for bid in [
    "btn-start-craft-idle",
    "btn-claim-craft-idle",
    "btn-cancel-craft-idle",
    "btn-start-drone-idle",
    "btn-claim-drone-idle",
    "btn-cancel-drone-idle",
    "btn-start-gold-gacha",
    "btn-claim-gold-gacha",
    "btn-cancel-gold-gacha",
]:
    js = re.sub(
        "document\\.getElementById\\('" + bid + "'\\)\\.addEventListener\\('click',[^;]+\\);",
        "",
        js,
    )

js = re.sub(r"startDroneAI\(\);?", "", js)
js = re.sub(r"grantDroneCompanionKillRewards\([^)]*\);?", "", js)
js = re.sub(r"if\(droneDungeonActive\)\{[^}]+\}", "", js)

# applyLanguage idle refs
for el in [
    "craft-idle-title",
    "craft-idle-desc",
    "drone-idle-title",
    "drone-idle-desc",
    "gold-gacha-title",
    "gold-gacha-desc",
    "profile-craft-idle-label",
    "profile-drone-idle-label",
    "btn-craft-idle",
]:
    js = re.sub(rf"const _\w+=document\.getElementById\('{el}'\);[^;]+;", "", js)

# profile render idle levels
js = re.sub(
    r"document\.getElementById\('profile-craft-idle-level'\)\.textContent=[^;]+;",
    "",
    js,
)
js = re.sub(
    r"document\.getElementById\('profile-drone-idle-level'\)\.textContent=[^;]+;",
    "",
    js,
)

# initGame drone resume
js = re.sub(
    r"if\(droneDungeonActive&&inDungeon\)\{applyDroneDungeonPanelLock\(\);startDroneAutoDungeon\(\);\}",
    "",
    js,
)

# migrate
js = js.replace(
    "function migrateSave(data){if(data.version<39){data._balanceV211Notice=true;data.version=39;}",
    "function migrateSave(data){if(data.version<41){data._balanceV212Notice=true;data.version=41;}if(data.version<39){data._balanceV211Notice=true;data.version=39;}",
)
js = js.replace(
    "const _balanceV211Notice=!!data._balanceV211Notice;delete data._balanceV211Notice;",
    "const _balanceV211Notice=!!data._balanceV211Notice;delete data._balanceV211Notice;const _balanceV212Notice=!!data._balanceV212Notice;delete data._balanceV212Notice;",
)
js = js.replace(
    "if(_balanceV211Notice)logInfo(t('logBalanceV211'));leaderboardTrackedLevel=-1;",
    "if(_balanceV211Notice)logInfo(t('logBalanceV211'));if(_balanceV212Notice)logInfo(t('logBalanceV212'));leaderboardTrackedLevel=-1;",
)

# loadGame stale drone dungeon
js = js.replace("droneDungeonActive=!!data.droneDungeonActive;", "")
js = js.replace("droneDungeonItems=Array.isArray(data.droneDungeonItems)?data.droneDungeonItems:[];", "")

s = s[: m.start(1)] + js + s[m.end(1) :]
path.write_text(s)
print("v2.12.0 remove idle/drone patch OK")
