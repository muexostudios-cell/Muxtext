import fs from 'fs';

const path = '/workspace/index.html';
let h = fs.readFileSync(path, 'utf8');

function syntaxOk(buf = h) {
  const start = buf.indexOf('<script>') + 8;
  const end = buf.lastIndexOf('</script>');
  try {
    new Function(buf.slice(start, end));
    return true;
  } catch (e) {
    console.error('SYNTAX:', e.message);
    const m = String(e.message).match(/position (\d+)/);
    if (m) {
      const js = buf.slice(start, end);
      const pos = +m[1];
      console.error(js.slice(Math.max(0, pos - 100), pos + 100));
    }
    return false;
  }
}

function rep(oldStr, newStr, label) {
  if (!h.includes(oldStr)) throw new Error('missing: ' + label);
  h = h.replace(oldStr, newStr);
  if (!syntaxOk()) throw new Error('syntax broke at: ' + label);
  console.log('OK', label);
}

const css = `
#combat-dock{display:flex;flex-direction:column;flex-shrink:0;border-top:1px solid #1a1a1a}
#combat-atk-bar{display:none;gap:.25rem;padding:.3rem .5rem .15rem;background:#000}
#combat-atk-bar.show{display:flex}
.combat-atk-btn{flex:1 1 0;min-width:0;min-height:2.6rem;padding:.35rem .25rem;background:#050505;color:#aaa;border:1px solid #222;font-family:inherit;font-size:.52rem;line-height:1.2;letter-spacing:.02rem;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:.2rem;position:relative;overflow:visible;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
.combat-atk-btn .weapon-btn-label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:100%}
.combat-atk-btn:disabled{opacity:.25;pointer-events:none}
.combat-atk-btn.ready{color:var(--accent);border-color:var(--accent)}
.combat-atk-btn.rarity-legendary{border-color:var(--legendary);color:var(--legendary)}
.combat-atk-btn.rarity-hidden{border-color:var(--hidden);color:var(--hidden)}
.combat-atk-btn.rarity-legendary.ready,.combat-atk-btn.rarity-hidden.ready{color:var(--accent);border-color:var(--accent)}
#combat-dock .combat-item-bar{margin:0;padding:.25rem .5rem .1rem;gap:.25rem;justify-content:stretch}
#combat-dock .combat-item-bar.show{display:flex}
#combat-dock .combat-slot-btn{flex:1 1 0;width:auto;min-width:0;min-height:46px}
#game-main.combat-layout #map-container,#game-main.combat-layout #quick-btns{display:none!important}
#game-main.combat-layout #battle-screen{order:2;flex-shrink:0}
#game-main.combat-layout #log-container{order:3;flex:1;min-height:0;display:block!important;overflow-y:auto;border-bottom:1px solid #1a1a1a}
#game-main.combat-layout #equip-panel.show,#game-main.combat-layout #inventory-panel.show,#game-main.combat-layout #craft-panel.show,#game-main.combat-layout #profile-panel.show{order:3;flex:1;min-height:0;overflow-y:auto}
#game-main.combat-layout #combat-dock{order:4}
#game-main.combat-layout #tab-bar{order:5;border-top:1px solid #1a1a1a}
#game-main.combat-layout #action-bar{order:6;border-top:1px solid #1a1a1a}
#game-main.combat-layout #player-xp-strip{order:1}
#game-main.combat-layout #status-bar{order:1}
#log-container .log-line.heal-msg{color:var(--heal)}
#log-container .log-line.dmg-msg{color:var(--dmg)}
#log-container .log-line.shield-msg{color:var(--shield)}
#log-container .log-line.death-msg{color:var(--hp);font-weight:700}
#log-container .log-line.lvlup-msg{color:var(--xp);font-weight:700}
#log-container .log-line.info-msg{color:#fff}
`;

rep('</style>', css + '</style>', 'css');
rep(
  '#btn-atk-main,#btn-atk-off{display:none}#btn-atk-main.show,#btn-atk-off.show{display:block}',
  '',
  'old atk css'
);
rep(
  '<div id="combat-item-bar" class="combat-item-bar"><button type="button" class="combat-slot-btn" data-slot="0" id="combat-slot-0"></button><button type="button" class="combat-slot-btn" data-slot="1" id="combat-slot-1"></button><button type="button" class="combat-slot-btn" data-slot="2" id="combat-slot-2"></button></div><div class="battle-msg" id="battle-msg">> 準備...</div><div id="loot-area">-- 戰利品 --</div></div>',
  '</div>',
  'html battle-screen'
);
rep(
  '<div id="tab-bar"><button class="tab-btn active" data-tab="log" id="tab-log">日誌</button>',
  '<div id="combat-dock"><div id="combat-item-bar" class="combat-item-bar"><button type="button" class="combat-slot-btn" data-slot="0" id="combat-slot-0"></button><button type="button" class="combat-slot-btn" data-slot="1" id="combat-slot-1"></button><button type="button" class="combat-slot-btn" data-slot="2" id="combat-slot-2"></button></div><div id="combat-atk-bar"><button type="button" id="btn-atk-main" class="combat-atk-btn" disabled></button><button type="button" id="btn-atk-off" class="combat-atk-btn" disabled></button></div></div><div id="tab-bar"><button class="tab-btn active" data-tab="log" id="tab-log">日誌</button>',
  'html combat-dock'
);
rep(
  '<div id="action-bar"><button id="btn-atk-main" disabled>[主手攻擊]</button><button id="btn-atk-off" disabled>[副手攻擊]</button><button id="btn-escape"',
  '<div id="action-bar"><button id="btn-escape"',
  'html action-bar'
);
rep(",battleMsg=document.getElementById('battle-msg'),lootArea=document.getElementById('loot-area')", '', 'vars');

const weaponHelpers = `function getWeaponAttackBtnHtml(eq){if(!eq)return'<span class="weapon-btn-label">'+getUnarmedWeaponName()+'</span>';const c=RARITY_COLORS[eq.rarity]||'#fff';const up=eq.upgradeLv?' +'+eq.upgradeLv:'';return getEquipPixelIconHtml(eq,20)+'<span class="weapon-btn-label" style="color:'+c+'">'+getEquipDisplayName(eq.name)+up+'</span>';}function updateWeaponAttackButtons(){if(!btnAtkMain||!btnAtkOff)return;const m=player.equipment.mainhand,o=player.equipment.offhand;btnAtkMain.innerHTML=getWeaponAttackBtnHtml(m);btnAtkOff.innerHTML=getWeaponAttackBtnHtml(o);btnAtkMain.className='combat-atk-btn'+(m?' rarity-'+m.rarity:'');btnAtkOff.className='combat-atk-btn'+(o?' rarity-'+o.rarity:'');}function setAtkBtnStyle(active){btnAtkMain.classList.toggle('ready',!!active);btnAtkOff.classList.toggle('ready',!!active);}`;

rep(
  "function setAtkBtnStyle(active){if(active){btnAtkMain.style.color='var(--accent)';btnAtkMain.style.borderColor='var(--accent)';btnAtkOff.style.color='var(--accent)';btnAtkOff.style.borderColor='var(--accent)';}else{btnAtkMain.style.color='#666';btnAtkMain.style.borderColor='#333';btnAtkOff.style.color='#666';btnAtkOff.style.borderColor='#333';}}",
  weaponHelpers,
  'weapon helpers'
);

rep(
  "const hideAtkBtns=()=>{btnAtkMain.classList.remove('show');btnAtkOff.classList.remove('show');};",
  "const atkBar=document.getElementById('combat-atk-bar');const hideAtkBtns=()=>{if(atkBar)atkBar.classList.remove('show');};",
  'updateButtons atkBar'
);
rep(
  "btnAtkMain.classList.toggle('show',showAtk);btnAtkOff.classList.toggle('show',showAtk);const canAttack=showAtk&&!gameOver&&!isProcessingQueue&&Date.now()>=playerAttackCooldownUntil;btnAtkMain.disabled=!canAttack;btnAtkOff.disabled=!canAttack;setAtkBtnStyle(canAttack);btnEscape.classList.add('show');",
  "const canAttack=showAtk&&!gameOver&&!isProcessingQueue&&Date.now()>=playerAttackCooldownUntil;btnAtkMain.disabled=!canAttack;btnAtkOff.disabled=!canAttack;setAtkBtnStyle(canAttack);updateWeaponAttackButtons();if(atkBar)atkBar.classList.toggle('show',showAtk);btnEscape.classList.toggle('show',showAtk);",
  'updateButtons'
);
rep('function tryEscape(){if(!inDungeon)return;', 'function tryEscape(){if(!inDungeon||!inCombat||!currentEnemy)return;', 'tryEscape');

rep(
  "function setLogVisible(show){const log=document.getElementById('log-container');if(!log)return;if(isDesktopLayout()){log.style.display='block';return;}log.style.display=show?'block':'none';}",
  "function updateCombatLayout(){const main=document.getElementById('game-main');if(!main)return;const on=!!(inCombat&&currentEnemy&&!isDesktopLayout());main.classList.toggle('combat-layout',on);if(on)setLogVisible(currentTab==='log');}function setLogVisible(show){const log=document.getElementById('log-container');if(!log)return;if(isDesktopLayout()){log.style.display='block';return;}if(inCombat&&!isDesktopLayout()){log.style.display=currentTab==='log'?'block':'none';return;}log.style.display=show?'block':'none';}",
  'combat layout'
);

const showBattleOld = "function showBattleScreen(show){if(show){battleScreen.classList.add('active');document.getElementById('map-container').style.display='none';setLogVisible(isDesktopLayout());}else{battleScreen.classList.remove('active');document.getElementById('map-container').style.display='flex';setLogVisible(isDesktopLayout()||currentTab==='log');lootArea.textContent=t('lootArea');}updateCombatItemBarVisibility();}";
const showBattleNew = "function showBattleScreen(show){if(show){battleScreen.classList.add('active');document.getElementById('map-container').style.display='none';if(!isDesktopLayout()){currentTab='log';document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));const tb=document.getElementById('tab-log');if(tb)tb.classList.add('active');equipPanel.classList.remove('show');inventoryPanel.classList.remove('show');craftPanel.classList.remove('show');profilePanel.classList.remove('show');}setLogVisible(true);}else{battleScreen.classList.remove('active');document.getElementById('map-container').style.display='flex';setLogVisible(isDesktopLayout()||currentTab==='log');}updateCombatLayout();updateCombatItemBarVisibility();}";
rep(showBattleOld, showBattleNew, 'showBattleScreen');

rep('if(show)renderCombatItemBar();}', 'if(show){renderCombatItemBar();updateWeaponAttackButtons();}}', 'combat bar vis');

rep(
  "function setBattleMsg(msg,cls=''){battleMsg.textContent='> '+msg;battleMsg.className='battle-msg '+cls;}",
  "function logCombat(msg,cls=''){if(!msg)return;log(msg,cls||'dmg-msg');}function setBattleMsg(msg,cls=''){logCombat(msg,cls);}",
  'logCombat'
);

rep('setBattleMsg(msg);logInfo(msg);', 'logCombat(msg);', 'dedupe1');
rep("setBattleMsg(`${currentEnemy.name} 未命中`,'shield-msg');logInfo(`${currentEnemy.name} 未命中`);", "logCombat(`${currentEnemy.name} 未命中`,'shield-msg');", 'dedupe2');
rep("setBattleMsg(`[${weaponName}] > ${currentEnemy.name} 閃避`,'shield-msg');logInfo(`${currentEnemy.name} 閃避了攻擊`);", "logCombat(`[${weaponName}] > ${currentEnemy.name} 閃避`,'shield-msg');logInfo(`${currentEnemy.name} 閃避了攻擊`);", 'dedupe3');
rep("setBattleMsg(`${currentEnemy.name} 被擊敗`,wasBoss?'boss-msg':'heal-msg');logInfo(t('msgEnemyDefeated',currentEnemy.name));", "logCombat(`${currentEnemy.name} 被擊敗`,wasBoss?'boss-msg':'heal-msg');logInfo(t('msgEnemyDefeated',currentEnemy.name));", 'dedupe4');
rep("logInfo('觸發避免死亡');setBattleMsg('避免死亡!','heal-msg');", "logCombat('避免死亡!','heal-msg');logInfo('觸發避免死亡');", 'dedupe5');
rep("setBattleMsg('你死了','death-msg');logInfo('你死了！');", "logCombat('你死了','death-msg');logInfo('你死了！');", 'dedupe6');
rep("logInfo(msg);setBattleMsg(msg,'heal-msg');", "logCombat(msg,'heal-msg');", 'dedupe7');

rep(
  "setBattleMsg(`遭遇: ${enemy.name}${initNote}${player.shield>0?' [護盾:'+player.shield+']':''}`,enemy.isBoss?'boss-msg':(player.shield>0?'shield-msg':'info-msg'));updateButtons();",
  "logCombat(`遭遇: ${enemy.name}${initNote}${player.shield>0?' [護盾:'+player.shield+']':''}`,enemy.isBoss?'boss-msg':(player.shield>0?'shield-msg':'info-msg'));updateButtons();updateCombatLayout();",
  'enterCombat'
);
rep('showBattleScreen(false);renderCombatItemBar();updateButtons();', 'showBattleScreen(false);renderCombatItemBar();updateButtons();updateCombatLayout();', 'exitCombat');

rep('player.gold+=totalGold;lootArea.innerHTML=`金幣: +${totalGold}`;', "player.gold+=totalGold;logCombat(`金幣: +${totalGold}`,'info-msg');", 'loot gold');
rep('player.xp+=_xpGain;lootArea.innerHTML+=` | 經驗: +${_xpGain}`;', "player.xp+=_xpGain;logCombat(`經驗: +${_xpGain}`,'info-msg');", 'loot xp');
rep('player.xp+=_clearBonus;lootArea.innerHTML+=` | 通關: +${_clearBonus}`;', "player.xp+=_clearBonus;logCombat(`通關: +${_clearBonus}`,'info-msg');", 'loot clear');
rep('logInfo(`掉落: ${equipToString(eq,false)}`);lootArea.innerHTML+=`<br>戰利品: ${equipToString(eq,true)}`;', 'logInfo(`掉落: ${equipToString(eq,false)}`);logCombat(`戰利品: ${equipToString(eq,true)}`,\'info-msg\');', 'loot equip');
rep('lootArea.innerHTML+=`<br>戰利品: ${equipToString(eq,true)} (自動回收)`;', 'logCombat(`戰利品: ${equipToString(eq,true)} (自動回收)`,\'info-msg\');', 'loot recycle');

while (h.includes("addItem('hellTicket',1);lootArea.innerHTML+='<br># 地獄門禁卡';")) {
  h = h.replace("addItem('hellTicket',1);lootArea.innerHTML+='<br># 地獄門禁卡';", "addItem('hellTicket',1);logCombat('# 地獄門禁卡','info-msg');");
}
if (!syntaxOk()) throw new Error('syntax after hell ticket');

rep("if(lootArea)lootArea.innerHTML+='<br>'+getItemIcon(id)+' '+formatItemName(id);else logItemLoot(id);", 'logItemLoot(id);', 'stones');
rep("else if(addItem(id,1)&&lootArea)lootArea.innerHTML+='<br>'+getItemIcon(id)+' '+getItemName(id);", 'else if(addItem(id,1))logItemLoot(id);', 'bag stones');
rep("const line=getItemIcon(stoneId)+' '+formatItemName(stoneId)+qtyLabel;if(lootArea)lootArea.innerHTML+='<br>'+line;logInfo(t('msgLootItem',formatItemName(stoneId)+qtyLabel));", "logInfo(t('msgLootItem',formatItemName(stoneId)+qtyLabel));", 'boss stones');
h = h.split('if(lootArea)lootArea.innerHTML+=`<br><span style="color:var(--item-red)">! ${getItemName(\'encryptedWeaponCrate\')}</span>`;').join('');

h = h.split('tryDropUpgradeStones(lootArea)').join('tryDropUpgradeStones()');
h = h.split('tryDropBagSpaceStones(lootArea)').join('tryDropBagSpaceStones()');
h = h.split('grantBossUpgradeStoneReward(lootArea)').join('grantBossUpgradeStoneReward()');
h = h.split('tryDropEncryptedWeaponCrate(wasBoss,lootArea)').join('tryDropEncryptedWeaponCrate(wasBoss)');
if (!syntaxOk()) throw new Error('syntax after loot cleanup');

rep(
  "document.getElementById('btn-atk-main').textContent=t('btnMainAtk');document.getElementById('btn-atk-off').textContent=t('btnOffAtk');",
  "if(typeof updateWeaponAttackButtons==='function')updateWeaponAttackButtons();",
  'applyLanguage'
);
if (h.includes("document.getElementById('loot-area').textContent=t('lootArea');")) {
  h = h.replace("document.getElementById('loot-area').textContent=t('lootArea');", '');
}
if (h.includes("setLogVisible(tab==='log');if(tab==='equip'){")) {
  h = h.replace("setLogVisible(tab==='log');if(tab==='equip'){", "setLogVisible(tab==='log');updateCombatLayout();if(tab==='equip'){");
}

rep("GAME_VERSION='2.24.34'", "GAME_VERSION='2.24.36'", 'version');
rep(
  "logBalanceV22434:'[修復 v2.24.34]",
  "logBalanceV22436:'[優化 v2.24.36] 戰鬥介面改版：傷害/戰利品改日誌顯示；底部武器攻擊列與快捷欄佈局。',logBalanceV22435:'[優化 v2.24.35] 逃脫按鈕僅在戰鬥中顯示。',logBalanceV22434:'[修復 v2.24.34]",
  'changelog'
);
rep(
  "VERSION_HISTORY=[{version:'2.24.34'",
  "VERSION_HISTORY=[{version:'2.24.36',date:'2026-06-09',summary:{zh:'v2.24.36 戰鬥介面改版與日誌化。',en:'v2.24.36 combat UI overhaul and log-based combat feed.'}},{version:'2.24.35',date:'2026-06-09',summary:{zh:'v2.24.35 逃脫按鈕僅戰鬥中顯示。',en:'v2.24.35 escape button only in combat.'}},{version:'2.24.34'",
  'history'
);

// equipItem refresh
if (h.includes('syncPlayerSeal();renderEquipPanel();updateStatusBar();')) {
  h = h.replace('syncPlayerSeal();renderEquipPanel();updateStatusBar();', 'syncPlayerSeal();renderEquipPanel();updateStatusBar();if(inCombat&&typeof updateWeaponAttackButtons===\'function\')updateWeaponAttackButtons();');
}
if (h.includes('syncPlayerSeal();renderEquipPanel();updateStatusBar();throttleSave();}function unequipItem')) {
  h = h.replace('syncPlayerSeal();renderEquipPanel();updateStatusBar();throttleSave();}function unequipItem', 'syncPlayerSeal();renderEquipPanel();updateStatusBar();if(inCombat&&typeof updateWeaponAttackButtons===\'function\')updateWeaponAttackButtons();throttleSave();}function unequipItem');
}

if (!syntaxOk()) throw new Error('final syntax');
fs.writeFileSync(path, h);
console.log('DONE lootArea refs:', (h.match(/lootArea/g) || []).length);
