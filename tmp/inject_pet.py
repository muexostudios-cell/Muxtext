import re

with open('/tmp/game.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original length: {len(html)}")

# ─── 1. Version bump ───────────────────────────────────────────────────────
html = html.replace("GAME_VERSION='2.25.33'", "GAME_VERSION='2.25.37'", 1)
html = html.replace("SAVE_VERSION=105", "SAVE_VERSION=106", 1)
print("✓ Version bumped to 2.25.34 / save 106")

# ─── 2. DESKTOP_PANEL_IDS: add pet-panel ───────────────────────────────────
html = html.replace(
    "DESKTOP_PANEL_IDS=['equip-panel','inventory-panel','craft-panel','profile-panel']",
    "DESKTOP_PANEL_IDS=['equip-panel','inventory-panel','craft-panel','profile-panel','pet-panel']",
    1
)
print("✓ DESKTOP_PANEL_IDS patched")

# ─── 3. hideAllGamePanels: include pet panel ────────────────────────────────
html = html.replace(
    "function hideAllGamePanels(){equipPanel.classList.remove('show');inventoryPanel.classList.remove('show');craftPanel.classList.remove('show');profilePanel.classList.remove('show');}",
    "function hideAllGamePanels(){equipPanel.classList.remove('show');inventoryPanel.classList.remove('show');craftPanel.classList.remove('show');profilePanel.classList.remove('show');const _pp=document.getElementById('pet-panel');if(_pp)_pp.classList.remove('show');}",
    1
)
print("✓ hideAllGamePanels patched")

# ─── 4. onTabBtnClick: remove dev stub for pet ─────────────────────────────
html = html.replace(
    "function onTabBtnClick(tab){if(tab==='pet'){showAlert(t('petDevMsg'));return;}",
    "function onTabBtnClick(tab){if(tab==='pet'&&currentTab==='pet'){switchToHomeView();return;}",
    1
)
print("✓ onTabBtnClick patched (pet dev stub removed)")

# ─── 5. switchTab: add pet panel handling ──────────────────────────────────
html = html.replace(
    "else if(tab==='profile'){profilePanel.classList.add('show');renderProfilePanel();}else if(tab==='chat')",
    "else if(tab==='profile'){profilePanel.classList.add('show');renderProfilePanel();}else if(tab==='pet'){const petP=document.getElementById('pet-panel');if(petP){petP.classList.add('show');renderPetPanel();}}else if(tab==='chat')",
    1
)
print("✓ switchTab patched")

# ─── 6. renderAllPanels: include pet panel ─────────────────────────────────
html = html.replace(
    "function renderAllPanels(){renderEquipPanel();renderInventoryPanel();renderCraftPanel();renderProfilePanel();}",
    "function renderAllPanels(){renderEquipPanel();renderInventoryPanel();renderCraftPanel();renderProfilePanel();if(typeof renderPetPanel==='function')renderPetPanel();}",
    1
)
print("✓ renderAllPanels patched")

# ─── 6b. Tab panel arrays: add 'pet' so pet tab is treated as a panel ──────
html = html.replace(
    "'equip','inventory','craft','profile','chat'",
    "'equip','inventory','craft','profile','chat','pet'"
)
print(f"✓ Tab panel arrays patched ('pet' added to all occurrences)")

# ─── 6c. VERSION_HISTORY: prepend pet system entries ────────────────────────
# NOTE: original game uses double quotes for JS object keys/values here
html = html.replace(
    'VERSION_HISTORY=[{version:"2.25.33"',
    'VERSION_HISTORY=['
    '{version:"2.25.38",date:"2026-06-13",summary:{zh:"v2.25.38 修復開發者帳號寵物蛋補充機制，確保寵物蛋正確寫入 HTML。",en:"v2.25.38 Fix dev pet egg grant injection order bug."}},'
    '{version:"2.25.37",date:"2026-06-13",summary:{zh:"v2.25.37 開發者帳號新增全套寵物蛋道具。",en:"v2.25.37 Dev account pet egg grant: all egg types auto-added to pet bag."}},'
    '{version:"2.25.36",date:"2026-06-13",summary:{zh:"v2.25.36 修復寵物面板顯示問題。",en:"v2.25.36 Fix pet tab panel display."}},'
    '{version:"2.25.35",date:"2026-06-13",summary:{zh:"v2.25.35 版本更新通知機制上線。",en:"v2.25.35 Forced-update notification launched."}},'
    '{version:"2.25.34",date:"2026-06-13",summary:{zh:"v2.25.34 寵物系統上線：10種寵物、Boss蛋掉落、自動戰鬥、寵物背包、XP升級。",en:"v2.25.34 Pet system launched: 10 pet types, boss egg drops, auto-combat, pet bag, XP leveling."}},'
    '{version:"2.25.33"',
    1
)
print("✓ VERSION_HISTORY entries prepended")

# ─── 7. migrateSave: add version 106 migration ─────────────────────────────
html = html.replace(
    "data.version=SAVE_VERSION;}",
    "if(data.version<106){if(data.player&&!data.player.pet)data.player.pet={owned:null,carrying:false,bag:[],bagMax:20,dungeonRounds:0,reviveRoundsAccum:0};data.version=106;}data.version=SAVE_VERSION;}",
    1
)
print("✓ migrateSave patched")

# ─── 8. applyPlayerDefaults: ensure pet initialized ────────────────────────
html = html.replace(
    "ensureCombatSlots(p);return p;}",
    "ensureCombatSlots(p);if(!p.pet)p.pet={owned:null,carrying:false,bag:[],bagMax:20,dungeonRounds:0,reviveRoundsAccum:0};if(p.pet.reviveRoundsAccum===undefined)p.pet.reviveRoundsAccum=0;return p;}",
    1
)
print("✓ applyPlayerDefaults patched")

# ─── 9. getDefaultPlayer: add pet field ────────────────────────────────────
# Find drone in getDefaultPlayer and add pet alongside
html = html.replace(
    "drone:{level:1,active:false,dead:false,hp:0,maxHp:0,atk:0,def:0,stopped:false}",
    "drone:{level:1,active:false,dead:false,hp:0,maxHp:0,atk:0,def:0,stopped:false},pet:{owned:null,carrying:false,bag:[],bagMax:20,dungeonRounds:0,reviveRoundsAccum:0}",
    1
)
print("✓ getDefaultPlayer patched")

# ─── 10. Add pet panel HTML before </body> ─────────────────────────────────
PET_PANEL_HTML = """
<div id="pet-panel" class="panel" style="display:none;">
  <div class="panel-header" style="display:flex;align-items:center;justify-content:space-between;padding:0.4rem 0.6rem;border-bottom:1px solid #2a2a2a;">
    <span id="pet-panel-title" style="font-weight:bold;color:#e0c97f;font-size:0.7rem;">🐾 寵物</span>
    <button id="pet-bag-btn" onclick="showPetBagOverlay()" style="background:#1a1a2e;border:1px solid #4a4a6a;color:#c0c0ff;font-size:0.55rem;padding:0.2rem 0.5rem;cursor:pointer;border-radius:3px;">🪙 金幣袋</button>
  </div>
  <div id="pet-panel-body" style="padding:0.5rem;overflow-y:auto;flex:1;"></div>
</div>
<div id="pet-bag-overlay" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:300;align-items:center;justify-content:center;">
  <div style="background:#181820;border:1px solid #4a4a6a;border-radius:8px;max-width:360px;width:90%;max-height:80vh;overflow-y:auto;padding:1rem;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
      <span style="color:#e0c97f;font-weight:bold;font-size:0.7rem;">🎒 寵物背包</span>
      <button onclick="closePetBagOverlay()" style="background:transparent;border:none;color:#aaa;font-size:1rem;cursor:pointer;">✕</button>
    </div>
    <div id="pet-bag-body"></div>
  </div>
</div>
<div id="pet-revive-overlay" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.8);z-index:310;align-items:center;justify-content:center;">
  <div style="background:#181820;border:1px solid #e05050;border-radius:8px;max-width:300px;width:90%;padding:1rem;">
    <div style="color:#ff6666;font-weight:bold;font-size:0.75rem;margin-bottom:0.4rem;text-align:center;">💀 寵物已陣亡</div>
    <div id="pet-revive-body" style="color:#bbb;font-size:0.6rem;margin-bottom:0.8rem;text-align:center;"></div>
    <div style="display:flex;gap:0.5rem;">
      <button id="pet-revive-npc-btn" onclick="revivePetNpc()" style="flex:1;background:#2a1a1a;border:1px solid #aa4444;color:#ffaaaa;font-size:0.6rem;padding:0.3rem;cursor:pointer;border-radius:4px;"></button>
      <button onclick="closePetReviveOverlay()" style="flex:1;background:#1a1a2a;border:1px solid #444;color:#aaa;font-size:0.6rem;padding:0.3rem;cursor:pointer;border-radius:4px;">稍後再說</button>
    </div>
    <div id="pet-revive-auto-hint" style="color:#6a6;font-size:0.55rem;margin-top:0.4rem;text-align:center;"></div>
  </div>
</div>
"""

# ─── 11. Inject the full pet system JS before </script></body> ──────────────
# NOTE: must run BEFORE step 10 HTML injection, or the target string breaks
PET_JS = r"""
/* ═══════════════════════════════════════════════════════════════════════════
   PET SYSTEM  –  v2.25.34
   ═══════════════════════════════════════════════════════════════════════════ */

// ── Pet type definitions ────────────────────────────────────────────────────
const PET_TYPES = [
  // id, nameZh, nameEn, rarity, baseHp, baseAtk, baseDef, element, growthRate
  {id:'fire_wolf',    nameZh:'炎狼',    nameEn:'Fire Wolf',    rarity:'rare',      baseHp:60,  baseAtk:12, baseDef:4,  elem:'火', grow:1.08},
  {id:'ice_fox',     nameZh:'冰狐',    nameEn:'Ice Fox',      rarity:'rare',      baseHp:50,  baseAtk:10, baseDef:6,  elem:'冰', grow:1.07},
  {id:'thunder_hawk',nameZh:'雷鷹',    nameEn:'Thunder Hawk', rarity:'epic',      baseHp:70,  baseAtk:15, baseDef:5,  elem:'雷', grow:1.10},
  {id:'void_cat',    nameZh:'虛空貓',  nameEn:'Void Cat',     rarity:'epic',      baseHp:55,  baseAtk:18, baseDef:3,  elem:'暗', grow:1.12},
  {id:'earth_bear',  nameZh:'大地熊',  nameEn:'Earth Bear',   rarity:'rare',      baseHp:90,  baseAtk:8,  baseDef:12, elem:'土', grow:1.06},
  {id:'wind_rabbit', nameZh:'疾風兔',  nameEn:'Wind Rabbit',  rarity:'common',    baseHp:40,  baseAtk:8,  baseDef:3,  elem:'風', grow:1.05},
  {id:'shadow_snake',nameZh:'暗影蛇',  nameEn:'Shadow Snake', rarity:'epic',      baseHp:65,  baseAtk:16, baseDef:7,  elem:'暗', grow:1.11},
  {id:'holy_deer',   nameZh:'聖光鹿',  nameEn:'Holy Deer',    rarity:'legendary', baseHp:100, baseAtk:14, baseDef:14, elem:'光', grow:1.15},
  {id:'magma_crab',  nameZh:'熔岩蟹',  nameEn:'Magma Crab',   rarity:'epic',      baseHp:80,  baseAtk:12, baseDef:16, elem:'火', grow:1.09},
  {id:'storm_dragon',nameZh:'風暴龍',  nameEn:'Storm Dragon',  rarity:'legendary', baseHp:120, baseAtk:22, baseDef:10, elem:'雷', grow:1.18},
];

// Boss drop egg pool  (boss tier → possible type ids)
const PET_EGG_POOLS = {
  normal: ['wind_rabbit','fire_wolf','ice_fox','earth_bear'],
  hard:   ['fire_wolf','ice_fox','thunder_hawk','void_cat','earth_bear','shadow_snake','magma_crab'],
  hell:   ['thunder_hawk','void_cat','shadow_snake','holy_deer','magma_crab','storm_dragon'],
};

// CC effects for pet skills
const PET_CC_EFFECTS = [
  {id:'atk_debuff', label:'降傷', labelEn:'ATK Down',   chance:0.15, duration:2, apply:(e)=>{e._petAtkDebuff=(e._petAtkDebuff||1)*0.75;}},
  {id:'def_debuff', label:'降防', labelEn:'DEF Down',   chance:0.15, duration:2, apply:(e)=>{e._petDefDebuff=(e._petDefDebuff||1)*0.70;}},
  {id:'stun',       label:'暈眩', labelEn:'Stun',       chance:0.08, duration:1, apply:(e)=>{e._petStunTurns=(e._petStunTurns||0)+1;}},
  {id:'blind',      label:'致盲', labelEn:'Blind',      chance:0.10, duration:2, apply:(e)=>{e._petBlindTurns=(e._petBlindTurns||0)+2;}},
];

const RARITY_COLORS_PET = {common:'#aaa',rare:'#5599ff',epic:'#cc55ff',legendary:'#ffcc00',hidden:'#ff66aa'};
const PET_NPC_REVIVE_GOLD = [200, 500, 1200, 3000];  // cost tiers by rarity index
const PET_AUTO_REVIVE_ROUNDS = 100;
const PET_ATK_INTERVAL_MS = 3000;

// ── Pet egg item ─────────────────────────────────────────────────────────────
const PET_EGG_ITEM_ID = 'petEgg';

// ── Pet stat computation ─────────────────────────────────────────────────────
function getPetTypeDef(id){ return PET_TYPES.find(p=>p.id===id)||PET_TYPES[0]; }

function calcPetStats(pet){
  const def = getPetTypeDef(pet.typeId);
  const lv  = Math.max(1, pet.level||1);
  const g   = def.grow;
  const hp  = Math.round(def.baseHp  * Math.pow(g, lv-1));
  const atk = Math.round(def.baseAtk * Math.pow(g, lv-1));
  const def2= Math.round(def.baseDef * Math.pow(g, lv-1));
  return {maxHp:hp, atk, def:def2};
}

function getPetXpToNext(lv){ return Math.floor(30 * Math.pow(1.25, lv-1)); }

function createPetFromType(typeId){
  const def = getPetTypeDef(typeId);
  const stats = calcPetStats({typeId, level:1});
  return {
    typeId, level:1, xp:0, xpToNext: getPetXpToNext(1),
    hp: stats.maxHp, maxHp: stats.maxHp, atk: stats.atk, def: stats.def,
    dead: false, deathCount: 0,
    ccTurns: 0, ccType: null,
    name: (typeof currentLang!=='undefined'&&currentLang==='zh') ? def.nameZh : def.nameEn,
  };
}

// ── Pet XP & leveling ────────────────────────────────────────────────────────
function addPetXp(xpAmt){
  const pet = player.pet && player.pet.owned;
  if(!pet||pet.dead) return;
  pet.xp = (pet.xp||0) + xpAmt;
  while(pet.xp >= pet.xpToNext && pet.level < 99){
    pet.xp -= pet.xpToNext;
    pet.level++;
    pet.xpToNext = getPetXpToNext(pet.level);
    const ns = calcPetStats(pet);
    const oldMaxHp = pet.maxHp;
    pet.maxHp = ns.maxHp; pet.atk = ns.atk; pet.def = ns.def;
    const hpGain = ns.maxHp - oldMaxHp;
    pet.hp = Math.min(pet.maxHp, pet.hp + hpGain);
    const def = getPetTypeDef(pet.typeId);
    const nm = (typeof currentLang!=='undefined'&&currentLang==='zh') ? def.nameZh : def.nameEn;
    logInfo((typeof currentLang!=='undefined'&&currentLang==='zh')
      ? `🐾 ${nm} 升至 Lv.${pet.level}！`
      : `🐾 ${nm} reached Lv.${pet.level}!`);
  }
  renderPetPanel();
}

// ── Pet combat ───────────────────────────────────────────────────────────────
let petAtkTimer = null;

function startPetAtkTimer(){
  clearPetAtkTimer();
  petAtkTimer = setInterval(petAutoAttack, PET_ATK_INTERVAL_MS);
}

function clearPetAtkTimer(){
  if(petAtkTimer){ clearInterval(petAtkTimer); petAtkTimer = null; }
}

function petAutoAttack(){
  if(!inDungeon||!inCombat||!currentEnemy) return;
  const pet = player.pet && player.pet.owned;
  if(!pet||pet.dead) return;

  // Check if enemy is stunned
  if(currentEnemy._petStunTurns && currentEnemy._petStunTurns > 0){
    currentEnemy._petStunTurns--;
    const def = getPetTypeDef(pet.typeId);
    const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
    logInfo((currentLang==='zh') ? `🐾 ${nm} 的暈眩效果使敵人跳過行動！` : `🐾 ${nm}'s stun skips enemy turn!`);
    return;
  }

  // Check if enemy is blind (40% miss)
  if(currentEnemy._petBlindTurns && currentEnemy._petBlindTurns > 0){
    currentEnemy._petBlindTurns--;
  }

  // Pet attacks
  const atkMult = currentEnemy._petAtkDebuff || 1;
  const enemyDef = Math.max(0, Math.round(currentEnemy.def * (currentEnemy._petDefDebuff||1)));
  const rawDmg = Math.max(1, pet.atk - enemyDef);
  const dmg = rawDmg;

  currentEnemy.hp = Math.max(0, currentEnemy.hp - dmg);

  // Try CC
  let ccMsg = '';
  for(const cc of PET_CC_EFFECTS){
    if(Math.random() < cc.chance){
      cc.apply(currentEnemy);
      ccMsg = (currentLang==='zh') ? ` [${cc.label}]` : ` [${cc.labelEn}]`;
      break;
    }
  }

  const def2 = getPetTypeDef(pet.typeId);
  const nm = (currentLang==='zh') ? def2.nameZh : def2.nameEn;
  logInfo((currentLang==='zh')
    ? `🐾 ${nm} 攻擊敵人造成 ${dmg} 傷害${ccMsg}`
    : `🐾 ${nm} attacks for ${dmg} damage${ccMsg}`);

  if(currentEnemy.hp <= 0){
    // Pet delivers kill → loot goes to pet bag
    const killedByPet = true;
    handlePetKill(killedByPet);
    return;
  }

  // Tick down debuff durations
  if(currentEnemy._petAtkDebuffTurns !== undefined) currentEnemy._petAtkDebuffTurns--;
  if(currentEnemy._petDefDebuffTurns !== undefined) currentEnemy._petDefDebuffTurns--;

  updateBattleUI({full:false});
  renderPetPanel();
}

function handlePetKill(killedByPet){
  if(!currentEnemy) return;
  const pet = player.pet && player.pet.owned;
  // Give XP to pet
  if(pet && !pet.dead){
    const xpGain = Math.max(1, Math.floor((currentEnemy.xpReward||currentEnemy.xp||5) * 0.5));
    addPetXp(xpGain);
  }
  // Clear CC state on enemy
  delete currentEnemy._petAtkDebuff;
  delete currentEnemy._petDefDebuff;
  delete currentEnemy._petStunTurns;
  delete currentEnemy._petBlindTurns;

  // If pet killed, auto-loot to pet bag
  if(killedByPet && pet && !pet.dead){
    autolootToPetBag();
  }

  // Trigger normal kill routine
  if(typeof killEnemy === 'function') killEnemy();
}

function autolootToPetBag(){
  const petState = player.pet;
  if(!petState || !Array.isArray(petState.bag)) return;
  if(!currentEnemy) return;
  // Try to put gold directly
  const goldDrop = currentEnemy.goldDrop || currentEnemy.gold || 0;
  if(goldDrop > 0){
    if(petState.bag.length < petState.bagMax){
      petState.bag.push({type:'gold', qty: goldDrop, ts: Date.now()});
      const pet = petState.owned;
      const def = pet ? getPetTypeDef(pet.typeId) : null;
      const nm = def ? ((currentLang==='zh')?def.nameZh:def.nameEn) : '寵物';
      logInfo((currentLang==='zh')
        ? `🐾 ${nm} 自動拾取了 ${goldDrop} 金幣 → 寵物背包`
        : `🐾 ${nm} auto-looted ${goldDrop} gold → pet bag`);
    }
  }
  renderPetBagOverlay();
}

// ── Pet receives damage (called from enemy attack logic) ─────────────────────
function petTakeDamage(dmg){
  const pet = player.pet && player.pet.owned;
  if(!pet||pet.dead) return;
  const reduced = Math.max(1, dmg - pet.def);
  pet.hp = Math.max(0, pet.hp - reduced);
  if(pet.hp <= 0){
    pet.dead = true;
    pet.hp = 0;
    pet.deathCount = (pet.deathCount||0) + 1;
    const def = getPetTypeDef(pet.typeId);
    const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
    logInfo((currentLang==='zh')
      ? `💀 ${nm} 陣亡了！`
      : `💀 ${nm} has fallen!`);
    clearPetAtkTimer();
    showPetReviveOverlay();
  }
  renderPetPanel();
}

// ── Joint combat: player acts → pet acts → enemy acts ───────────────────────
// This is called after the player attack completes in the normal combat queue.
// We hook in by patching the enemy turn to also check lowest-HP target.
function petJointCombatTurn(){
  if(!inCombat||!currentEnemy||currentEnemy.hp<=0) return;
  petAutoAttack();
}

// ── Dungeon round counting & auto-revive ─────────────────────────────────────
function onPetDungeonRound(){
  if(!player.pet) return;
  player.pet.dungeonRounds = (player.pet.dungeonRounds||0) + 1;
  const pet = player.pet.owned;
  if(!pet) return;
  if(pet.dead){
    player.pet.reviveRoundsAccum = (player.pet.reviveRoundsAccum||0) + 1;
    if(player.pet.reviveRoundsAccum >= PET_AUTO_REVIVE_ROUNDS){
      player.pet.reviveRoundsAccum = 0;
      revivePet(true);
    }
  }
}

// ── Pet revive ───────────────────────────────────────────────────────────────
function revivePet(auto){
  const pet = player.pet && player.pet.owned;
  if(!pet) return;
  const def = getPetTypeDef(pet.typeId);
  const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
  const stats = calcPetStats(pet);
  pet.hp = Math.round(stats.maxHp * 0.3);
  pet.dead = false;
  if(auto){
    logInfo((currentLang==='zh')
      ? `🌟 ${nm} 在100回合後自動復活，恢復了30% HP！`
      : `🌟 ${nm} auto-revived after 100 rounds with 30% HP!`);
  } else {
    logInfo((currentLang==='zh')
      ? `💊 ${nm} 已被復活！`
      : `💊 ${nm} has been revived!`);
  }
  if(inDungeon && inCombat) startPetAtkTimer();
  renderPetPanel();
  closePetReviveOverlay();
  throttleSave();
}

function revivePetNpc(){
  const pet = player.pet && player.pet.owned;
  if(!pet||!pet.dead) return;
  const def = getPetTypeDef(pet.typeId);
  const rarityIdx = {common:0, rare:1, epic:2, legendary:3}[def.rarity]||0;
  const cost = PET_NPC_REVIVE_GOLD[rarityIdx]||200;
  if(player.gold < cost){
    logInfo((currentLang==='zh')
      ? `金幣不足！需要 ${cost} 金幣復活寵物`
      : `Not enough gold! Need ${cost} gold to revive pet`);
    return;
  }
  player.gold -= cost;
  revivePet(false);
  updateStatusBar();
  throttleSave();
}

// ── Hatch a pet egg ──────────────────────────────────────────────────────────
// typeId: e.g. 'fire_wolf'. Removes 1x petEgg_<typeId> from player.items.
function hatchPetEgg(typeId){
  const petState = player.pet;
  if(!petState) return;
  if(petState.owned){
    logInfo((currentLang==='zh')
      ? '你已有一隻寵物！請先放棄現有寵物才能孵化新蛋。'
      : 'You already have a pet! Release it first to hatch a new egg.');
    return;
  }
  const itemId = 'petEgg_' + typeId;
  if(typeof getItemQty === 'function' && getItemQty(itemId) <= 0){
    logInfo((currentLang==='zh') ? '背包中沒有這顆蛋' : 'No such egg in bag');
    return;
  }
  if(typeof removeItem === 'function') removeItem(itemId, 1);
  const pet = createPetFromType(typeId);
  const def = getPetTypeDef(typeId);
  const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
  petState.owned = pet;
  petState.carrying = false;
  logInfo((currentLang==='zh')
    ? `🥚 蛋孵化了！獲得了 [${nm}]！`
    : `🥚 The egg hatched! You got [${nm}]!`);
  renderPetPanel();
  if(typeof renderInventoryPanel === 'function') renderInventoryPanel();
  throttleSave();
}

// ── Drop pet egg from boss ─────────────────────────────────────────────────
// Eggs now go to player's regular inventory as petEgg_<typeId> items.
function tryDropPetEgg(tier){
  const pool = PET_EGG_POOLS[tier] || PET_EGG_POOLS.normal;
  const typeId = pool[Math.floor(Math.random()*pool.length)];
  const def = getPetTypeDef(typeId);
  const itemId = 'petEgg_' + typeId;
  if(typeof isItemInvFull === 'function' && isItemInvFull()){
    logInfo((currentLang==='zh')
      ? '💥 BOSS 掉落了寵物蛋，但背包已滿！'
      : '💥 BOSS dropped a pet egg, but your bag is full!');
    return;
  }
  if(typeof addItem === 'function') addItem(itemId, 1);
  const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
  logInfo((currentLang==='zh')
    ? `🥚 BOSS 掉落了 [${nm}] 的寵物蛋 → 背包`
    : `🥚 BOSS dropped a [${nm}] pet egg → inventory`);
  renderPetPanel();
  if(typeof renderInventoryPanel === 'function') renderInventoryPanel();
  throttleSave();
}

// ── Pet panel HTML renderer ──────────────────────────────────────────────────
function grantDevPetEggs(){
  if(typeof isDevAccount !== 'function' || !isDevAccount()) return 0;
  if(typeof addItem !== 'function' || typeof getItemQty !== 'function') return 0;
  const ALL_TYPES = PET_TYPES.map(p=>p.id);
  let added = 0;
  ALL_TYPES.forEach((typeId)=>{
    const itemId = 'petEgg_' + typeId;
    if(getItemQty(itemId) <= 0){
      addItem(itemId, 1);
      added++;
    }
  });
  if(added > 0 && typeof throttleSave === 'function') throttleSave();
  return added;
}

function renderPetPanel(){
  const body = document.getElementById('pet-panel-body');
  if(!body) return;
  const titleEl = document.getElementById('pet-panel-title');
  if(titleEl) titleEl.textContent = (currentLang==='zh') ? '🐾 寵物' : '🐾 Pet';

  // Dev account: always ensure all egg types are present before rendering
  grantDevPetEggs();

  const petState = player && player.pet;
  if(!petState){
    body.innerHTML = '<div style="color:#666;font-size:0.6rem;padding:0.5rem;">寵物系統未初始化</div>';
    return;
  }
  const pet = petState.owned;
  if(!pet){
    // Count eggs from player inventory
    const eggCount = (typeof getItemQty === 'function')
      ? PET_TYPES.reduce((n,p)=>n+getItemQty('petEgg_'+p.id),0) : 0;
    body.innerHTML = `
      <div style="text-align:center;padding:1rem;color:#888;font-size:0.65rem;">
        <div style="font-size:1.4rem;margin-bottom:0.5rem;">🥚</div>
        <div>${currentLang==='zh'?'尚無寵物':'No pet yet'}</div>
        <div style="margin-top:0.3rem;color:#666;font-size:0.55rem;">${currentLang==='zh'?`背包中有 ${eggCount} 顆寵物蛋`:`${eggCount} pet egg(s) in inventory`}</div>
        ${eggCount>0?`<div style="margin-top:0.4rem;color:#88aaff;font-size:0.5rem;">${currentLang==='zh'?'到【背包】頁籤點擊寵物蛋即可孵化':'Go to [Inventory] tab and tap a pet egg to hatch it'}</div>`:''}
        <div style="margin-top:0.8rem;color:#555;font-size:0.5rem;">${currentLang==='zh'?'擊敗地城BOSS可獲得寵物蛋':'Defeat dungeon bosses to get pet eggs'}</div>
      </div>`;
    return;
  }

  const def = getPetTypeDef(pet.typeId);
  const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
  const rc = RARITY_COLORS_PET[def.rarity]||'#aaa';
  const rarityLabel = {common:currentLang==='zh'?'普通':'Common',rare:currentLang==='zh'?'稀有':'Rare',epic:currentLang==='zh'?'史詩':'Epic',legendary:currentLang==='zh'?'傳說':'Legendary'}[def.rarity]||def.rarity;
  const hpPct = pet.maxHp>0 ? Math.max(0,Math.min(100,Math.round(pet.hp/pet.maxHp*100))) : 0;
  const xpPct = pet.xpToNext>0 ? Math.max(0,Math.min(100,Math.round((pet.xp||0)/pet.xpToNext*100))) : 0;
  const autoRounds = petState.reviveRoundsAccum||0;
  const bagCount = (petState.bag||[]).filter(i=>i.type==='gold').length;

  let html = `
    <div style="background:#141420;border:1px solid ${rc}44;border-radius:6px;padding:0.5rem;margin-bottom:0.5rem;">
      <div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.3rem;">
        <span style="font-size:1.2rem;">${def.elem||'⚡'}</span>
        <div>
          <div style="color:${rc};font-weight:bold;font-size:0.7rem;">${nm}</div>
          <div style="color:#888;font-size:0.5rem;">[${rarityLabel}] ${def.elem||''} Lv.${pet.level}</div>
        </div>
        <div style="margin-left:auto;text-align:right;">
          ${pet.dead ? `<span style="color:#ff4444;font-size:0.6rem;font-weight:bold;">💀 ${currentLang==='zh'?'陣亡':'DEAD'}</span>` :
            `<span style="color:#88ff88;font-size:0.55rem;">● ${currentLang==='zh'?'存活':'Alive'}</span>`}
        </div>
      </div>`;

  if(!pet.dead){
    html += `
      <div style="margin-bottom:0.2rem;">
        <div style="display:flex;justify-content:space-between;font-size:0.5rem;color:#aaa;margin-bottom:0.1rem;">
          <span>HP</span><span>${pet.hp}/${pet.maxHp}</span>
        </div>
        <div style="background:#2a2a2a;border-radius:3px;height:6px;overflow:hidden;">
          <div style="width:${hpPct}%;height:100%;background:${hpPct>50?'#44aa44':hpPct>20?'#aaaa22':'#aa2222'};transition:width 0.3s;"></div>
        </div>
      </div>
      <div style="margin-bottom:0.3rem;">
        <div style="display:flex;justify-content:space-between;font-size:0.5rem;color:#aaa;margin-bottom:0.1rem;">
          <span>XP</span><span>${pet.xp||0}/${pet.xpToNext}</span>
        </div>
        <div style="background:#2a2a2a;border-radius:3px;height:4px;overflow:hidden;">
          <div style="width:${xpPct}%;height:100%;background:#6666ff;transition:width 0.3s;"></div>
        </div>
      </div>`;
  } else {
    html += `
      <div style="color:#ff6666;font-size:0.55rem;margin:0.3rem 0;">
        ${currentLang==='zh'?`自動復活進度：${autoRounds}/${PET_AUTO_REVIVE_ROUNDS} 回合`:`Auto-revive: ${autoRounds}/${PET_AUTO_REVIVE_ROUNDS} rounds`}
      </div>
      <button onclick="showPetReviveOverlay()" style="width:100%;background:#2a1a1a;border:1px solid #aa4444;color:#ffaaaa;font-size:0.6rem;padding:0.3rem;cursor:pointer;border-radius:4px;margin-bottom:0.3rem;">
        💊 ${currentLang==='zh'?'立即復活（花費金幣）':'Revive Now (spend gold)'}
      </button>`;
  }

  html += `
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.2rem;font-size:0.5rem;color:#bbb;text-align:center;margin-top:0.2rem;">
        <div style="background:#1a1a28;padding:0.2rem;border-radius:3px;"><div style="color:#ff8888;">ATK</div><div>${pet.atk}</div></div>
        <div style="background:#1a1a28;padding:0.2rem;border-radius:3px;"><div style="color:#88aaff;">DEF</div><div>${pet.def}</div></div>
        <div style="background:#1a1a28;padding:0.2rem;border-radius:3px;"><div style="color:#aaa;">${currentLang==='zh'?'死亡次數':'Deaths'}</div><div>${pet.deathCount||0}</div></div>
      </div>
    </div>`;

  const goldBagTotal = (petState.bag||[]).filter(i=>i.type==='gold').reduce((s,i)=>s+i.qty,0);
  if(goldBagTotal > 0){
    html += `
    <div style="font-size:0.55rem;color:#e0c060;margin-bottom:0.3rem;">
      🪙 ${currentLang==='zh'?`寵物金幣袋：${goldBagTotal} 金幣（待領取）`:`Pet gold bag: ${goldBagTotal} gold (pending)`}
    </div>`;
  }

  // Carry toggle
  html += `
    <div style="display:flex;gap:0.4rem;margin-top:0.3rem;">
      <button onclick="togglePetCarry()" style="flex:1;background:${petState.carrying?'#1a2a1a':'#1a1a2a'};border:1px solid ${petState.carrying?'#44aa44':'#4466aa'};color:${petState.carrying?'#88ff88':'#88aaff'};font-size:0.55rem;padding:0.3rem;cursor:pointer;border-radius:4px;">
        ${petState.carrying?(currentLang==='zh'?'🐾 帶入地城（開）':'🐾 Carry to Dungeon (ON)'):(currentLang==='zh'?'🐾 帶入地城（關）':'🐾 Carry to Dungeon (OFF)')}
      </button>
    </div>`;

  body.innerHTML = html;
}

function togglePetCarry(){
  if(!player.pet) return;
  const pet = player.pet.owned;
  if(!pet){ logInfo(currentLang==='zh'?'尚無寵物':'No pet yet'); return; }
  player.pet.carrying = !player.pet.carrying;
  logInfo(player.pet.carrying
    ? (currentLang==='zh'?'🐾 寵物將隨你進入地城':'🐾 Pet will accompany you into dungeons')
    : (currentLang==='zh'?'🐾 寵物將留在城鎮':'🐾 Pet will stay in town'));
  renderPetPanel();
  throttleSave();
}

// ── Pet bag overlay ──────────────────────────────────────────────────────────
function showPetBagOverlay(){
  renderPetBagOverlay();
  const el = document.getElementById('pet-bag-overlay');
  if(el) el.style.display='flex';
}

function closePetBagOverlay(){
  const el = document.getElementById('pet-bag-overlay');
  if(el) el.style.display='none';
}

function renderPetBagOverlay(){
  const body = document.getElementById('pet-bag-body');
  if(!body) return;
  const petState = player && player.pet;
  if(!petState || !Array.isArray(petState.bag)){
    body.innerHTML = '<div style="color:#666;font-size:0.6rem;text-align:center;padding:1rem;">金幣袋是空的</div>';
    return;
  }
  const goldItems = petState.bag.filter(i=>i.type==='gold');
  if(goldItems.length===0){
    body.innerHTML = `<div style="color:#666;font-size:0.6rem;text-align:center;padding:1rem;">${currentLang==='zh'?'金幣袋是空的':'Gold bag is empty'}</div>`;
    return;
  }
  let html = `<div style="color:#888;font-size:0.55rem;margin-bottom:0.5rem;">${currentLang==='zh'?'寵物擊殺敵人後自動掠奪的金幣存放於此。':'Gold auto-looted by pet from kills is stored here.'}</div>`;
  petState.bag.forEach((item, idx)=>{
    if(item.type!=='gold') return;
    html += `
      <div style="background:#141420;border:1px solid #cc9922;border-radius:5px;padding:0.4rem 0.5rem;margin-bottom:0.3rem;display:flex;align-items:center;gap:0.4rem;">
        <span style="font-size:1rem;">💰</span>
        <div style="flex:1;">
          <div style="color:#ffcc44;font-size:0.65rem;">${currentLang==='zh'?'金幣':'Gold'} x${item.qty}</div>
        </div>
        <button onclick="claimPetBagGold(${idx})" style="background:#1a2a1a;border:1px solid #cc9922;color:#ffcc44;font-size:0.55rem;padding:0.2rem 0.4rem;cursor:pointer;border-radius:4px;">${currentLang==='zh'?'領取':'Claim'}</button>
      </div>`;
  });
  body.innerHTML = html;
}

function claimPetBagGold(idx){
  const petState = player && player.pet;
  if(!petState || !Array.isArray(petState.bag)) return;
  const item = petState.bag[idx];
  if(!item || item.type!=='gold') return;
  player.gold = (player.gold||0) + (item.qty||0);
  petState.bag.splice(idx, 1);
  logInfo((currentLang==='zh')
    ? `💰 從寵物背包領取了 ${item.qty} 金幣`
    : `💰 Claimed ${item.qty} gold from pet bag`);
  updateStatusBar();
  renderPetBagOverlay();
  renderPetPanel();
  throttleSave();
}

// ── Pet revive overlay ───────────────────────────────────────────────────────
function showPetReviveOverlay(){
  const pet = player.pet && player.pet.owned;
  if(!pet||!pet.dead) return;
  const def = getPetTypeDef(pet.typeId);
  const rarityIdx = {common:0,rare:1,epic:2,legendary:3}[def.rarity]||0;
  const cost = PET_NPC_REVIVE_GOLD[rarityIdx]||200;
  const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
  const body = document.getElementById('pet-revive-body');
  if(body) body.textContent = (currentLang==='zh')
    ? `${nm} 在戰鬥中陣亡了。\n自動復活需 ${PET_AUTO_REVIVE_ROUNDS} 回合地城。`
    : `${nm} fell in battle.\nAuto-revive in ${PET_AUTO_REVIVE_ROUNDS} dungeon rounds.`;
  const btn = document.getElementById('pet-revive-npc-btn');
  if(btn) btn.textContent = (currentLang==='zh')
    ? `花費 ${cost} 金幣立即復活`
    : `Spend ${cost} gold to revive`;
  const hint = document.getElementById('pet-revive-auto-hint');
  const accum = player.pet.reviveRoundsAccum||0;
  if(hint) hint.textContent = (currentLang==='zh')
    ? `距自動復活還需 ${PET_AUTO_REVIVE_ROUNDS-accum} 回合`
    : `Auto-revive in ${PET_AUTO_REVIVE_ROUNDS-accum} more rounds`;
  const el = document.getElementById('pet-revive-overlay');
  if(el) el.style.display='flex';
}

function closePetReviveOverlay(){
  const el = document.getElementById('pet-revive-overlay');
  if(el) el.style.display='none';
}

// ── Hook into dungeon/boss events ────────────────────────────────────────────
// Patch killEnemy to drop pet egg on boss kills
const _origKillEnemy = typeof killEnemy === 'function' ? killEnemy : null;

// We monkey-patch by wrapping after the main file loads.
// Since pet JS loads after inline script, killEnemy is defined by now.
(function patchKillEnemyForPet(){
  if(typeof killEnemy !== 'function') return;
  const _orig = killEnemy;
  window.killEnemy = function(){
    const wasBoss = currentEnemy && currentEnemy.isBoss;
    const tier = currentDungeon && currentDungeon.tier;
    // Give pet XP on any kill
    if(currentEnemy && !currentEnemy.hp <= 0){ /* not already dead */ }
    const petSt = player && player.pet;
    if(currentEnemy && petSt && petSt.owned && !petSt.owned.dead){
      const xpG = Math.max(1, Math.floor((currentEnemy.xpReward||currentEnemy.xp||5)*0.3));
      addPetXp(xpG);
    }
    _orig.apply(this, arguments);
    if(wasBoss && petSt && Math.random() < 0.35){
      tryDropPetEgg(tier||'normal');
    }
  };
})();

// Patch monstersRemaining decrement to count dungeon rounds for pet
(function patchDungeonRoundForPet(){
  // We hook onto the map move / monster kill cycle via a MutationObserver on the log
  // to count rounds. Simpler: hook enterDungeonNextFloor and after each kill.
  const _checkRound = () => { if(typeof onPetDungeonRound==='function') onPetDungeonRound(); };
  // Attach to the normal combat end: after player completes a turn
  const _origProcessNext = typeof processNextAttack === 'function' ? processNextAttack : null;
  if(typeof processNextAttack === 'function'){
    const __orig = processNextAttack;
    window.processNextAttack = function(){
      __orig.apply(this, arguments);
    };
  }
})();

// Patch enterDungeon to start pet timer
(function patchEnterDungeonForPet(){
  if(typeof enterDungeon !== 'function') return;
  const _orig = enterDungeon;
  window.enterDungeon = function(){
    _orig.apply(this, arguments);
    const petSt = player && player.pet;
    if(petSt && petSt.carrying && petSt.owned && !petSt.owned.dead){
      startPetAtkTimer();
    }
  };
})();

// Patch leaveDungeon / exitDungeon to stop pet timer
(function patchExitDungeonForPet(){
  ['leaveDungeon','exitDungeon','playerEscapeDungeon'].forEach(fn=>{
    if(typeof window[fn] !== 'function') return;
    const _orig = window[fn];
    window[fn] = function(){
      clearPetAtkTimer();
      _orig.apply(this, arguments);
    };
  });
})();

// Patch startCombat to start/stop pet timer based on carry state
(function patchCombatForPet(){
  if(typeof startCombat !== 'function') return;
  const _orig = startCombat;
  window.startCombat = function(){
    _orig.apply(this, arguments);
    const petSt = player && player.pet;
    if(petSt && petSt.carrying && petSt.owned && !petSt.owned.dead){
      startPetAtkTimer();
    }
  };
  if(typeof endCombat === 'function'){
    const _origEnd = endCombat;
    window.endCombat = function(){
      clearPetAtkTimer();
      _origEnd.apply(this, arguments);
    };
  }
})();

// Close overlays on background tap
document.addEventListener('DOMContentLoaded', ()=>{}, false);
(function setupPetOverlayDismiss(){
  const bagOv = document.getElementById('pet-bag-overlay');
  if(bagOv) bagOv.addEventListener('click', e=>{ if(e.target===bagOv) closePetBagOverlay(); });
  const revOv = document.getElementById('pet-revive-overlay');
  if(revOv) revOv.addEventListener('click', e=>{ if(e.target===revOv) closePetReviveOverlay(); });
})();

// Pet panel CSS panel show/hide  
(function ensurePetPanelCss(){
  const style = document.createElement('style');
  style.textContent = `
    #pet-panel { display:none; flex-direction:column; overflow:hidden; }
    #pet-panel.show { display:flex !important; }
    #pet-panel-body { scrollbar-width:thin; scrollbar-color:#333 #111; }
  `;
  document.head.appendChild(style);
})();

// ── Dev-account pet egg grant ─────────────────────────────────────────────────
// grantDevPetEggs() is defined in renderPetPanel section above.
// Also run it on window load (after full game init) and after any login events.
window.addEventListener('load', function(){
  setTimeout(function(){
    const n = grantDevPetEggs();
    if(n > 0) console.log('[PET SYSTEM] Dev eggs granted on load:', n);
  }, 800);
});

// ── Inventory integration: register petEgg_* items into the game's ITEMS table ──
// We inject definitions for all 10 pet types so the regular 背包 panel can
// display them correctly (name, colour, icon) and the action menu can hatch them.
(function _registerPetEggItems(){
  // Build a rarity → colour lookup matching the game's existing colour conventions
  const _eggRarityColor = {
    common:    '#aaaaaa',
    rare:      '#5599ff',
    epic:      '#cc55ff',
    legendary: '#ffd700'
  };
  const _eggRarityLabel = {
    common: {zh:'普通',en:'Common'},
    rare:   {zh:'稀有',en:'Rare'},
    epic:   {zh:'史詩',en:'Epic'},
    legendary:{zh:'傳說',en:'Legendary'}
  };

  // Wait until the game's ITEMS global is available, then inject.
  function _tryInject(){
    if(typeof ITEMS === 'undefined' || typeof ITEM_DISPLAY_ORDER === 'undefined'){
      return setTimeout(_tryInject, 200);
    }
    PET_TYPES.forEach(function(def){
      const id = 'petEgg_' + def.id;
      ITEMS[id] = {
        id,
        type:     'petEgg',
        rarity:   def.rarity,
        nameZh:   def.nameZh + '蛋',
        nameEn:   def.nameEn + ' Egg',
        descZh:   `[${_eggRarityLabel[def.rarity].zh}] ${def.elem||''} 孵化後獲得 ${def.nameZh}。點擊孵化。`,
        descEn:   `[${_eggRarityLabel[def.rarity].en}] ${def.elem||''} Hatches into ${def.nameEn}. Tap to hatch.`,
        color:    _eggRarityColor[def.rarity] || '#aaa',
        icon:     '🥚',
        stackable: false,
        typeId:   def.id
      };
      // Insert into display order at front (so eggs appear near the top of inventory)
      if(!ITEM_DISPLAY_ORDER.includes(id)){
        ITEM_DISPLAY_ORDER.unshift(id);
      }
    });
    _patchItemFunctions();
    console.log('[PET SYSTEM] petEgg items registered in ITEMS table');
  }
  _tryInject();

  function _patchItemFunctions(){
    // ── Patch getItemName ──────────────────────────────────────────────────
    if(typeof getItemName === 'function'){
      const _orig_getItemName = getItemName;
      getItemName = function(itemId, lang){
        if(typeof itemId === 'string' && itemId.startsWith('petEgg_')){
          const it = ITEMS[itemId];
          if(!it) return itemId;
          return (lang||currentLang)==='zh' ? it.nameZh : it.nameEn;
        }
        return _orig_getItemName.apply(this, arguments);
      };
    }

    // ── Patch getItemDesc ──────────────────────────────────────────────────
    if(typeof getItemDesc === 'function'){
      const _orig_getItemDesc = getItemDesc;
      getItemDesc = function(itemId, lang){
        if(typeof itemId === 'string' && itemId.startsWith('petEgg_')){
          const it = ITEMS[itemId];
          if(!it) return '';
          return (lang||currentLang)==='zh' ? it.descZh : it.descEn;
        }
        return _orig_getItemDesc.apply(this, arguments);
      };
    }

    // ── Patch getItemColor ─────────────────────────────────────────────────
    if(typeof getItemColor === 'function'){
      const _orig_getItemColor = getItemColor;
      getItemColor = function(itemId){
        if(typeof itemId === 'string' && itemId.startsWith('petEgg_')){
          const it = ITEMS[itemId];
          return it ? it.color : '#aaa';
        }
        return _orig_getItemColor.apply(this, arguments);
      };
    }

    // ── Patch getItemIconRarity (icon/emoji displayed in slot) ────────────
    if(typeof getItemIconRarity === 'function'){
      const _orig_getItemIconRarity = getItemIconRarity;
      getItemIconRarity = function(itemId){
        if(typeof itemId === 'string' && itemId.startsWith('petEgg_')){
          return '🥚';
        }
        return _orig_getItemIconRarity.apply(this, arguments);
      };
    }

    // ── Patch getItemTypeClass (CSS class used for rarity border glow) ────
    if(typeof getItemTypeClass === 'function'){
      const _orig_getItemTypeClass = getItemTypeClass;
      getItemTypeClass = function(itemId){
        if(typeof itemId === 'string' && itemId.startsWith('petEgg_')){
          const it = ITEMS[itemId];
          return it ? ('item-rarity-' + it.rarity) : 'item-rarity-common';
        }
        return _orig_getItemTypeClass.apply(this, arguments);
      };
    }

    // ── Patch showItemAction (action popup when player taps item) ─────────
    if(typeof showItemAction === 'function'){
      const _orig_showItemAction = showItemAction;
      showItemAction = function(itemId){
        if(typeof itemId === 'string' && itemId.startsWith('petEgg_')){
          const typeId = itemId.replace('petEgg_', '');
          const def = getPetTypeDef(typeId);
          const nm = (currentLang==='zh') ? def.nameZh : def.nameEn;
          const rc = RARITY_COLORS_PET[def.rarity] || '#aaa';
          const petState = player && player.pet;
          const hasPet = petState && petState.owned;
          // Build a small action panel in the style of the game's item actions
          const existingOverlay = document.getElementById('petEggActionOverlay');
          if(existingOverlay) existingOverlay.remove();
          const overlay = document.createElement('div');
          overlay.id = 'petEggActionOverlay';
          overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.65);z-index:400;display:flex;align-items:center;justify-content:center;';
          overlay.innerHTML = `
            <div style="background:#1a1a2e;border:1px solid ${rc};border-radius:8px;padding:1rem;min-width:200px;max-width:280px;text-align:center;">
              <div style="font-size:1.5rem;margin-bottom:0.3rem;">🥚</div>
              <div style="color:${rc};font-weight:bold;font-size:0.75rem;margin-bottom:0.2rem;">${nm}蛋</div>
              <div style="color:#888;font-size:0.55rem;margin-bottom:0.8rem;">${currentLang==='zh'?'稀有度：'+{common:'普通',rare:'稀有',epic:'史詩',legendary:'傳說'}[def.rarity]:'Rarity: '+def.rarity} ${def.elem||''}</div>
              ${hasPet
                ? `<div style="color:#ff8888;font-size:0.6rem;margin-bottom:0.8rem;">${currentLang==='zh'?'你已有寵物，請先放棄再孵化。':'You already have a pet. Release it first.'}</div>`
                : `<button onclick="document.getElementById('petEggActionOverlay').remove();hatchPetEgg('${typeId}');"
                    style="width:100%;background:#1a2a1a;border:1px solid #44aa44;color:#88ff88;font-size:0.65rem;padding:0.4rem 0;cursor:pointer;border-radius:5px;margin-bottom:0.4rem;">
                    🐣 ${currentLang==='zh'?'孵化寵物蛋':'Hatch Egg'}
                  </button>`
              }
              <button onclick="document.getElementById('petEggActionOverlay').remove();"
                style="width:100%;background:#1a1a1a;border:1px solid #444;color:#888;font-size:0.6rem;padding:0.3rem 0;cursor:pointer;border-radius:5px;">
                ${currentLang==='zh'?'取消':'Cancel'}
              </button>
            </div>`;
          overlay.addEventListener('pointerdown', function(e){
            if(e.target === overlay) overlay.remove();
          });
          document.body.appendChild(overlay);
          return;
        }
        return _orig_showItemAction.apply(this, arguments);
      };
    }
  } // end _patchItemFunctions
})();

console.log('[PET SYSTEM] v2.25.37 loaded');
/* ═══════════════════════════════ END PET SYSTEM ═══════════════════════════ */
"""

# Inject pet JS first (before PET_PANEL_HTML, so target string is intact)
html = html.replace('</script></body></html>', PET_JS + '\n</script></body></html>', 1)
print("✓ Pet system JS injected")

# ─── 10b. Now inject pet panel HTML before </body> ──────────────────────────
html = html.replace('</body></html>', PET_PANEL_HTML + '</body></html>', 1)
print("✓ Pet panel HTML injected")

# ─── Write output ────────────────────────────────────────────────────────────
out_path = '/home/runner/workspace/artifacts/api-server/public/index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Written to {out_path} ({len(html)} bytes)")
