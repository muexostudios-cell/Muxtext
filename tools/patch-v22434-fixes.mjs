import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

// --- 1. Move combat-item-bar into battle-screen ---
const combatBarHtml = '<div id="combat-item-bar" class="combat-item-bar"><button type="button" class="combat-slot-btn" data-slot="0" id="combat-slot-0"></button><button type="button" class="combat-slot-btn" data-slot="1" id="combat-slot-1"></button><button type="button" class="combat-slot-btn" data-slot="2" id="combat-slot-2"></button></div>';
if (!html.includes(combatBarHtml + '<div id="action-bar">')) throw new Error('combat bar before action-bar not found');
html = html.replace(combatBarHtml + '<div id="action-bar">', '<div id="action-bar">');
const battleAnchor = '</div></div><div class="battle-msg" id="battle-msg">';
if (!html.includes(battleAnchor)) throw new Error('battle-screen anchor not found');
html = html.replace(battleAnchor, '</div></div>' + combatBarHtml + '<div class="battle-msg" id="battle-msg">');

// --- 2. CSS: combat bar only in battle screen ---
html = html.replace(
  '.combat-item-bar{display:none;gap:.3rem;margin:.35rem 0 .2rem;justify-content:center;flex-wrap:wrap}',
  '.combat-item-bar{display:none;gap:.3rem;margin:.35rem 0 .15rem;justify-content:center;flex-wrap:wrap;width:100%}#battle-screen .combat-item-bar{margin-top:.25rem}'
);

// --- 3. syncPlayerSeal + ensurePlayerEquipment ---
const sealAnchor = 'function sealPlayerState(){if(typeof player!==\'undefined\'&&player&&!isDevAccount())_acSeal=computePlayerSeal(player);}';
if (!html.includes(sealAnchor)) throw new Error('sealPlayerState not found');
html = html.replace(
  sealAnchor,
  sealAnchor + 'function syncPlayerSeal(opts={}){let p;try{p=player;}catch(e){return;}if(!p)return;if(opts.recalc!==false){recalcPlayerStats();updateDroneStats();}sealPlayerState();}function ensurePlayerEquipment(p){const target=p||(typeof player!==\'undefined\'?player:null);if(!target)return;const def=getDefaultPlayer().equipment;if(!target.equipment||typeof target.equipment!==\'object\')target.equipment={...def};for(const slotDef of EQUIP_SLOTS){if(target.equipment[slotDef.slot]===undefined)target.equipment[slotDef.slot]=null;}}'
);

// --- 4. applyPlayerDefaults: ensure equipment ---
html = html.replace(
  'ensureItemInvState();ensureCombatSlots(p);return p;}',
  'ensureItemInvState();ensurePlayerEquipment(p);ensureCombatSlots(p);return p;}'
);

// --- 5. addItem/removeItem: sync seal after item count changes ---
html = html.replace(
  "player.items[itemId]=existing+qty;return true;}function removeItem(itemId,qty){if(getItemQty(itemId)>=qty){player.items[itemId]-=qty;if(player.items[itemId]<=0)delete player.items[itemId];return true;}return false;}",
  "player.items[itemId]=existing+qty;syncPlayerSeal({recalc:false});return true;}function removeItem(itemId,qty){if(getItemQty(itemId)>=qty){player.items[itemId]-=qty;if(player.items[itemId]<=0)delete player.items[itemId];syncPlayerSeal({recalc:false});return true;}return false;}"
);

// --- 6. validateAllEquipment: repair before delete ---
const valOld = 'function validateAllEquipment(){let ok=true;const fix=eq=>{if(eq&&!validateEquipmentItem(eq)){bugClientSignals.add(\'invalid_equipment\');ok=false;return null;}return eq;};';
const valNew = 'function sanitizeEquipmentItem(eq){if(!eq||!eq.type||!eq.rarity)return null;if(!eq.id)eq.id=\'eq_\'+Date.now().toString(36)+\'_\'+Math.random().toString(36).slice(2,8);if(!Array.isArray(eq.affixes))eq.affixes=[];if(!eq.level||eq.level<1)eq.level=1;for(const a of eq.affixes){if(!a||!a.stat)continue;const b=getEquipAffixValueBounds(eq,a.stat);if(Number.isFinite(a.value))a.value=clamp(a.value,b.min,b.max);}return eq;}function validateAllEquipment(){let ok=true;const fix=eq=>{if(!eq)return null;if(validateEquipmentItem(eq))return eq;const repaired=sanitizeEquipmentItem(eq);if(repaired&&validateEquipmentItem(repaired))return repaired;bugClientSignals.add(\'invalid_equipment\');ok=false;return null;};';
if (!html.includes(valOld)) throw new Error('validateAllEquipment not found');
html = html.replace(valOld, valNew);

// --- 7. useHerb: sync seal immediately ---
html = html.replace(
  'if(inCombat){updateBattleUI();updateStatusBar();renderInventoryPanel();}else{updateBattleUI();updateStatusBar();renderAllPanels();}throttleSave();return true;}function getHerbDesc',
  'syncPlayerSeal();if(inCombat){updateBattleUI();updateStatusBar();renderInventoryPanel();}else{updateBattleUI();updateStatusBar();renderAllPanels();}throttleSave();return true;}function getHerbDesc'
);

// --- 8. equipItem / unequipItem: sync seal ---
html = html.replace(
  'logInfo(t(\'msgEquipped\',equipToString(eq,false)));renderAllPanels();updateStatusBar();throttleSave();}function unequipItem',
  'logInfo(t(\'msgEquipped\',equipToString(eq,false)));syncPlayerSeal();renderAllPanels();updateStatusBar();throttleSave();}function unequipItem'
);
html = html.replace(
  'logInfo(t(\'msgUnequipped\',equipToString(eq,false)));renderAllPanels();updateStatusBar();throttleSave();}',
  'logInfo(t(\'msgUnequipped\',equipToString(eq,false)));syncPlayerSeal();renderAllPanels();updateStatusBar();throttleSave();}'
);

// --- 9. combat bar visibility helpers ---
const renderCombatAnchor = 'function renderCombatItemBar(){let p;try{p=player;}catch(e){return;}';
const visibilityFns = 'function shouldShowCombatItemBar(){if(player&&player.isPermanentlyDead)return false;return !!(inDungeon&&inCombat&&currentEnemy&&!gameOver&&battleScreen&&battleScreen.classList.contains(\'active\'));}function updateCombatItemBarVisibility(){const cbar=document.getElementById(\'combat-item-bar\');const abar=document.getElementById(\'action-bar\');const show=shouldShowCombatItemBar();if(cbar)cbar.classList.toggle(\'show\',show);if(abar)abar.classList.toggle(\'combat-active\',show);if(show)renderCombatItemBar();}function renderCombatItemBar(){let p;try{p=player;}catch(e){return;}';
if (!html.includes(renderCombatAnchor)) throw new Error('renderCombatItemBar not found');
html = html.replace(renderCombatAnchor, visibilityFns);

// --- 10. updateButtons: use updateCombatItemBarVisibility, always hide on early exit ---
const ubOld = "setAtkBtnStyle(false);return;}if(gameOver){btnAtkMain.disabled=true;btnAtkOff.disabled=true;hideAtkBtns();btnEscape.classList.remove('show');btnLeave.classList.remove('show');btnRestart.classList.add('show');setAtkBtnStyle(false);return;}if(!inDungeon){btnAtkMain.disabled=true;btnAtkOff.disabled=true;hideAtkBtns();btnEscape.classList.remove('show');btnLeave.classList.remove('show');btnRestart.classList.remove('show');setAtkBtnStyle(false);return;}";
const ubNew = "setAtkBtnStyle(false);updateCombatItemBarVisibility();return;}if(gameOver){btnAtkMain.disabled=true;btnAtkOff.disabled=true;hideAtkBtns();btnEscape.classList.remove('show');btnLeave.classList.remove('show');btnRestart.classList.add('show');setAtkBtnStyle(false);updateCombatItemBarVisibility();return;}if(!inDungeon){btnAtkMain.disabled=true;btnAtkOff.disabled=true;hideAtkBtns();btnEscape.classList.remove('show');btnLeave.classList.remove('show');btnRestart.classList.remove('show');setAtkBtnStyle(false);updateCombatItemBarVisibility();return;}";
if (!html.includes(ubOld)) throw new Error('updateButtons early returns not found');
html = html.replace(ubOld, ubNew);
html = html.replace(
  "const cbar=document.getElementById('combat-item-bar');const abar=document.getElementById('action-bar');if(cbar)cbar.classList.toggle('show',showAtk);if(abar)abar.classList.toggle('combat-active',showAtk);renderCombatItemBar();}",
  'updateCombatItemBarVisibility();'
);

// --- 11. showBattleScreen: use visibility helper ---
html = html.replace('lootArea.textContent=t(\'lootArea\');}renderCombatItemBar();}', 'lootArea.textContent=t(\'lootArea\');}updateCombatItemBarVisibility();}');

// --- 12. applyLanguage: don't render combat bar on boot ---
html = html.replace('renderCombatItemBar();document.getElementById(\'materials-title\')', 'document.getElementById(\'materials-title\')');

// --- 13. dungeon entry lock + return bool ---
html = html.replace(
  'let dungeonShowCompleted=false,dungeonShowRecentClears=false,dungeonLoadMoreExtra=0,selectedTierLevel=null;',
  'let dungeonShowCompleted=false,dungeonShowRecentClears=false,dungeonLoadMoreExtra=0,selectedTierLevel=null,dungeonEntryBusy=false;'
);
const sdOld = "function startDungeon(tierLevel,tier){if(isVersionUpdateBlocking())return;if(player.isPermanentlyDead){logInfo('角色已永久死亡，無法進入地城');return;}if(tier==='hell'&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡');return;}const unlockedTier=getUnlockedDungeonTier();if(!isDungeonTierUnlocked(tierLevel)){logInfo(t('dungeonLockedMsg'));logInfo(t('dungeonMaxMsg',unlockedTier*TIERS_PER_LEVEL-2,unlockedTier*TIERS_PER_LEVEL));return;}if(!canEnterDungeonByPlayerLevel(tierLevel)){logInfo(t('dungeonLevelTooHighLog',getTierLevelStart(tierLevel),player.level||1,PLAYER_LEVEL_GAP));return;}startDungeonInternal(tierLevel,tier);}";
const sdNew = "function startDungeon(tierLevel,tier){if(dungeonEntryBusy||inDungeon){if(inDungeon)logInfo(t('dungeonAlreadyInside'));return false;}if(isVersionUpdateBlocking()){showAlert(t('versionUpdateBlocking'));return false;}if(player.isPermanentlyDead){logInfo('角色已永久死亡，無法進入地城');return false;}if(tier==='hell'&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡');return false;}const unlockedTier=getUnlockedDungeonTier();if(!isDungeonTierUnlocked(tierLevel)){logInfo(t('dungeonLockedMsg'));logInfo(t('dungeonMaxMsg',unlockedTier*TIERS_PER_LEVEL-2,unlockedTier*TIERS_PER_LEVEL));return false;}if(!canEnterDungeonByPlayerLevel(tierLevel)){logInfo(t('dungeonLevelTooHighLog',getTierLevelStart(tierLevel),player.level||1,PLAYER_LEVEL_GAP));return false;}dungeonEntryBusy=true;try{startDungeonInternal(tierLevel,tier);return true;}catch(e){console.error(e);logInfo(t('dungeonEnterFail'));return false;}finally{dungeonEntryBusy=false;}}";
if (!html.includes(sdOld)) throw new Error('startDungeon not found');
html = html.replace(sdOld, sdNew);

// --- 14. difficulty selection: close overlays only on success ---
html = html.replace(
  "btn.addEventListener('click',()=>{if(diff.requiresTicket&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡！');return;}difficultyOverlay.style.display='none';dungeonOverlay.style.display='none';startDungeon(tierLevel,diff.tier);});",
  "btn.addEventListener('click',()=>{if(diff.requiresTicket&&getItemQty('hellTicket')<1){logInfo('需要地獄門禁卡！');return;}if(!startDungeon(tierLevel,diff.tier))return;difficultyOverlay.style.display='none';dungeonOverlay.style.display='none';});"
);

// --- 15. LANG keys ---
html = html.replace(
  'logBalanceV22433:\'[修復 v2.24.33]',
  'logBalanceV22434:\'[修復 v2.24.34] 修復裝備異常丟失、戰鬥快捷欄僅顯示於地城戰鬥畫面、地下城進入偶發失敗。\',logBalanceV22433:\'[修復 v2.24.33]'
);
html = html.replace(
  'logBalanceV22433:\'[Fix v2.24.33]',
  'logBalanceV22434:\'[Fix v2.24.34] Fix equip loss, combat bar scope, dungeon entry reliability.\',logBalanceV22433:\'[Fix v2.24.33]'
);
html = html.replace(
  'versionUpdateMandatory:',
  'versionUpdateBlocking:"請先更新遊戲版本後再繼續",dungeonAlreadyInside:"已在地城中",dungeonEnterFail:"進入地城失敗，請再試一次",versionUpdateMandatory:'
);
html = html.replace(
  'versionUpdateMandatory:',
  'versionUpdateBlocking:"Update the game before continuing",dungeonAlreadyInside:"Already in a dungeon",dungeonEnterFail:"Failed to enter dungeon, please try again",versionUpdateMandatory:'
);
// fix double en replace - en block uses different structure
const enBlock = html.indexOf('en:{');
const enVersionMandatory = html.indexOf('versionUpdateMandatory:', enBlock);
if (enVersionMandatory > 0 && !html.slice(enBlock, enVersionMandatory).includes('versionUpdateBlocking:')) {
  html = html.slice(0, enVersionMandatory) + 'versionUpdateBlocking:"Update the game before continuing",dungeonAlreadyInside:"Already in a dungeon",dungeonEnterFail:"Failed to enter dungeon, please try again",' + html.slice(enVersionMandatory);
}

// --- 16. version bump ---
html = html.replace(/GAME_VERSION='2\.24\.33'/, "GAME_VERSION='2.24.34'");
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.33'",
  "GAME_VERSION_HISTORY=[{version:'2.24.34',date:'2026-06-09',summary:{zh:'v2.24.34 修復裝備丟失與戰鬥快捷欄顯示範圍。',en:'v2.24.34 fix equip loss and combat bar scope.'}},{version:'2.24.33'"
);

fs.writeFileSync(path, html);
console.log('Patched index.html for v2.24.34');
