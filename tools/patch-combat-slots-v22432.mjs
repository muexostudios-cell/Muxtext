import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

// --- CSS: replace auto-herb panel styles ---
const cssOld = '.auto-herb-panel{margin-top:.5rem;padding:.4rem .45rem;border:1px solid #1a1a1a;background:#050505;font-size:.48rem;line-height:1.5}.auto-herb-toggle{display:flex;align-items:center;gap:.35rem;color:var(--heal);margin-bottom:.35rem;cursor:pointer}.auto-herb-toggle input{accent-color:var(--heal)}.auto-herb-row{display:flex;align-items:center;gap:.3rem;margin-top:.25rem;flex-wrap:wrap}.auto-herb-row>span{color:#666;min-width:2rem}.auto-herb-btns{display:flex;gap:.2rem;flex-wrap:wrap}.auto-herb-btn{background:#050505;border:1px solid #222;color:#888;padding:.15rem .35rem;font-family:inherit;font-size:.45rem;cursor:pointer}.auto-herb-btn.active{border-color:var(--heal);color:var(--heal)}.auto-herb-btn:disabled{opacity:.35;cursor:not-allowed}';
const cssNew = '.combat-item-bar{display:none;gap:.3rem;margin:.35rem 0 .2rem;justify-content:center;flex-wrap:wrap}.combat-item-bar.show{display:flex}#action-bar.combat-active{flex-wrap:wrap}.combat-slot-btn{width:54px;min-height:54px;border:1px solid #222;background:#050505;padding:.2rem;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-family:inherit;font-size:.42rem;color:#666;cursor:pointer;position:relative;touch-action:manipulation}.combat-slot-btn.equipped{border-color:var(--herb);color:var(--herb)}.combat-slot-btn.auto-on::after{content:"";position:absolute;top:3px;right:3px;width:5px;height:5px;background:var(--heal);box-shadow:0 0 4px var(--heal)}.combat-slot-btn .combat-slot-icon{pointer-events:none}.combat-slot-btn .combat-slot-qty{font-size:.38rem;color:#888}.combat-slot-btn.equipped .combat-slot-qty{color:var(--heal)}.combat-slot-btn .combat-slot-label{font-size:.36rem;color:#555;line-height:1.1;text-align:center}.combat-slot-btn.equipped .combat-slot-label{color:#aaa}#combat-slot-overlay{position:fixed;inset:0;background:rgba(0,0,0,.82);display:none;align-items:center;justify-content:center;z-index:12000;padding:1rem}#combat-slot-box{background:#050505;border:1px solid #222;padding:.75rem;max-width:320px;width:100%;font-size:.55rem}#combat-slot-title{color:var(--heal);margin-bottom:.45rem;font-size:.65rem}#combat-slot-body{color:#aaa;line-height:1.5;margin-bottom:.5rem}#combat-slot-btns{display:flex;flex-wrap:wrap;gap:.35rem}#combat-slot-btns button{background:#050505;border:1px solid #333;color:#fff;padding:.35rem .5rem;font-family:inherit;font-size:.5rem;cursor:pointer}#combat-slot-btns button.primary{border-color:var(--heal);color:var(--heal)}.combat-auto-range{width:100%;margin:.45rem 0;accent-color:var(--heal)}.combat-auto-stat{color:#ccc;font-size:.5rem;margin-top:.2rem}';
if (!html.includes(cssOld)) throw new Error('auto-herb CSS not found');
html = html.replace(cssOld, cssNew);

// --- HTML: remove auto-herb panel, add combat bar + overlay ---
const herbPanelHtml = '<div id="auto-herb-panel" class="auto-herb-panel"><label class="auto-herb-toggle"><input type="checkbox" id="auto-herb-enabled"><span id="auto-herb-label">自動草藥</span></label><div class="auto-herb-row"><span id="auto-herb-threshold-label">低於</span><div class="auto-herb-btns" id="auto-herb-threshold-btns"><button type="button" class="auto-herb-btn" data-threshold="15">15%</button><button type="button" class="auto-herb-btn" data-threshold="30">30%</button><button type="button" class="auto-herb-btn" data-threshold="50">50%</button></div></div><div class="auto-herb-row"><span id="auto-herb-herb-label">草藥</span><div class="auto-herb-btns" id="auto-herb-herb-btns"><button type="button" class="auto-herb-btn" data-herb="herb_low">+低</button><button type="button" class="auto-herb-btn" data-herb="herb_mid">+中</button><button type="button" class="auto-herb-btn" data-herb="herb_high">+高</button></div></div></div>';
if (!html.includes(herbPanelHtml)) throw new Error('auto-herb-panel HTML not found');
html = html.replace(herbPanelHtml, '');

const actionBarAnchor = '<div id="action-bar">';
if (!html.includes(actionBarAnchor)) throw new Error('action-bar not found');
html = html.replace(actionBarAnchor, '<div id="combat-item-bar" class="combat-item-bar"><button type="button" class="combat-slot-btn" data-slot="0" id="combat-slot-0"></button><button type="button" class="combat-slot-btn" data-slot="1" id="combat-slot-1"></button><button type="button" class="combat-slot-btn" data-slot="2" id="combat-slot-2"></button></div>' + actionBarAnchor);

const overlayAnchor = '<div id="equip-action-overlay">';
if (!html.includes(overlayAnchor)) throw new Error('equip-action-overlay not found');
html = html.replace(overlayAnchor, '<div id="combat-slot-overlay"><div id="combat-slot-box"><h3 id="combat-slot-title"></h3><div id="combat-slot-body"></div><div id="combat-slot-btns"></div></div></div>' + overlayAnchor);

// --- settings: remove autoHerb ---
html = html.replace(
  "const settings={uiScale:UI_SCALE_DEFAULT,textSize:TEXT_SIZE_DEFAULT,autoHerb:{enabled:false,threshold:30,herbId:'herb_low'}};",
  'const settings={uiScale:UI_SCALE_DEFAULT,textSize:TEXT_SIZE_DEFAULT};'
);

// --- loadSettings: strip autoHerb ---
html = html.replace(
  /if\(s\.autoHerb\)\{const th=\[15,30,50\]\.includes\(s\.autoHerb\.threshold\)\?s\.autoHerb\.threshold:30;const herb=\['herb_low','herb_mid','herb_high'\]\.includes\(s\.autoHerb\.herbId\)\?s\.autoHerb\.herbId:'herb_low';settings\.autoHerb=\{enabled:!!s\.autoHerb\.enabled,threshold:th,herbId:herb\};\}else settings\.autoHerb=\{enabled:false,threshold:30,herbId:'herb_low'\};/,
  ''
);

// --- getDefaultPlayer: combatSlots ---
html = html.replace(
  "items:{herb_low:3},craftLevel:1",
  "items:{herb_low:3},combatSlots:[{herbId:null,autoEnabled:false,threshold:30},{herbId:null,autoEnabled:false,threshold:30},{herbId:null,autoEnabled:false,threshold:30}],craftLevel:1"
);

// --- remove autoHerbWarnState ---
html = html.replace('let autoHerbWarnState={};', '');

// --- applyPlayerDefaults: ensureCombatSlots ---
html = html.replace(
  'ensureItemInvState();return p;}',
  'ensureItemInvState();ensureCombatSlots(p);return p;}'
);

// --- loadGame migration ---
html = html.replace(
  'if(data.autoHerbSettings)settings.autoHerb={...settings.autoHerb,...data.autoHerbSettings};player=data.player;',
  'if(data.autoHerbSettings){data._legacyAutoHerbSettings=data.autoHerbSettings;delete data.autoHerbSettings;}player=data.player;'
);
html = html.replace(
  'player=applyPlayerDefaults(player);reconcilePlayerXpProgress',
  'player=applyPlayerDefaults(player);migrateLegacyAutoHerbSettings(data._legacyAutoHerbSettings);reconcilePlayerXpProgress'
);

// --- saveGame: drop autoHerbSettings if present ---
html = html.replace(/,autoHerbSettings:settings\.autoHerb/g, '');

// --- startDungeon ---
html = html.replace('enterDungeonWithAutoHerbCheck(tierLevel,tier);', 'startDungeonInternal(tierLevel,tier);');

// --- tryAutoUseHerb calls ---
html = html.replaceAll('tryAutoUseHerb()', 'tryAutoUseCombatItems()');

// --- init ---
html = html.replace('initAutoHerbPanel();', 'initCombatItemBar();');

// --- applyLanguage ---
html = html.replace('applyAutoHerbLanguage();', 'renderCombatItemBar();');

// --- updateButtons: show combat bar ---
const updateButtonsOld = "btnEscape.classList.add('show');if(shouldShowLeaveButton())btnLeave.classList.add('show');else btnLeave.classList.remove('show');}";
const updateButtonsNew = "btnEscape.classList.add('show');if(shouldShowLeaveButton())btnLeave.classList.add('show');else btnLeave.classList.remove('show');const cbar=document.getElementById('combat-item-bar');const abar=document.getElementById('action-bar');if(cbar)cbar.classList.toggle('show',showAtk);if(abar)abar.classList.toggle('combat-active',showAtk);renderCombatItemBar();}";
if (!html.includes(updateButtonsOld)) throw new Error('updateButtons tail not found');
html = html.replace(updateButtonsOld, updateButtonsNew);

// --- remove updateAutoHerbPanelVisibility calls ---
html = html.replaceAll('updateAutoHerbPanelVisibility();', 'renderCombatItemBar();');

// --- replace entire auto herb module ---
const moduleStart = 'const AUTO_HERB_THRESHOLDS=[15,30,50];';
const moduleEnd = 'function useHerb(itemId,opts={})';
const si = html.indexOf(moduleStart);
const ei = html.indexOf(moduleEnd);
if (si < 0 || ei < 0 || ei <= si) throw new Error('auto herb module bounds not found');

const combatModule = `const COMBAT_ITEM_IDS=['herb_low','herb_mid','herb_high'];const COMBAT_SLOT_COUNT=3;function defaultCombatSlot(){return{herbId:null,autoEnabled:false,threshold:30};}function ensureCombatSlots(p){const target=p||player;if(!target)return;if(!Array.isArray(target.combatSlots))target.combatSlots=[defaultCombatSlot(),defaultCombatSlot(),defaultCombatSlot()];while(target.combatSlots.length<COMBAT_SLOT_COUNT)target.combatSlots.push(defaultCombatSlot());target.combatSlots=target.combatSlots.slice(0,COMBAT_SLOT_COUNT).map(s=>({herbId:COMBAT_ITEM_IDS.includes(s&&s.herbId)?s.herbId:null,autoEnabled:!!(s&&s.herbId&&s.autoEnabled),threshold:clamp(parseInt(s&&s.threshold,10)||30,5,95)}));}function migrateLegacyAutoHerbSettings(legacy){if(!legacy||!legacy.enabled)return;ensureCombatSlots(player);const slot=player.combatSlots[0];if(slot.herbId)return;const herb=COMBAT_ITEM_IDS.includes(legacy.herbId)?legacy.herbId:'herb_low';slot.herbId=herb;slot.autoEnabled=true;slot.threshold=[15,30,50].includes(legacy.threshold)?legacy.threshold:30;}function getPlayerHpPercent(){if(!player||!player.maxHp)return 0;return Math.max(0,Math.min(100,Math.round((player.hp/player.maxHp)*100)));}function closeCombatSlotOverlay(){const ov=document.getElementById('combat-slot-overlay');if(ov)ov.style.display='none';}function openCombatSlotOverlay(title,bodyHtml,btns){const ov=document.getElementById('combat-slot-overlay'),ti=document.getElementById('combat-slot-title'),bd=document.getElementById('combat-slot-body'),bs=document.getElementById('combat-slot-btns');if(!ov||!ti||!bd||!bs)return;ti.textContent=title||'';bd.innerHTML=bodyHtml||'';bs.innerHTML='';(btns||[]).forEach(b=>{const btn=document.createElement('button');if(b.primary)btn.className='primary';btn.textContent=b.label;btn.addEventListener('click',()=>{if(b.action)b.action();});bs.appendChild(btn);});ov.style.display='flex';}function equipCombatSlot(slotIndex,herbId){ensureCombatSlots();const slot=player.combatSlots[slotIndex];if(!slot)return;if(!herbId){slot.herbId=null;slot.autoEnabled=false;closeCombatSlotOverlay();renderCombatItemBar();throttleSave();return;}if(!COMBAT_ITEM_IDS.includes(herbId))return;if(getItemQty(herbId)<1){showAlert(t('combatSlotNoItem',getItemName(herbId)));return;}for(let i=0;i<COMBAT_SLOT_COUNT;i++){if(i!==slotIndex&&player.combatSlots[i].herbId===herbId)player.combatSlots[i].herbId=null;}slot.herbId=herbId;closeCombatSlotOverlay();renderCombatItemBar();throttleSave();}function showCombatSlotPicker(slotIndex){ensureCombatSlots();const slot=player.combatSlots[slotIndex];const btns=[];COMBAT_ITEM_IDS.forEach(id=>{const qty=getItemQty(id);btns.push({label:getItemName(id)+' x'+qty,primary:slot.herbId===id,action:()=>{if(qty<1)showAlert(t('combatSlotNoItem',getItemName(id)));else equipCombatSlot(slotIndex,id);}});});if(slot.herbId)btns.push({label:t('combatSlotUnequip'),action:()=>equipCombatSlot(slotIndex,null)});btns.push({label:t('btnClose'),action:closeCombatSlotOverlay});openCombatSlotOverlay(t('combatSlotEquipTitle'),t('combatSlotEquipHint'),btns);}function showCombatAutoThreshold(slotIndex){ensureCombatSlots();const slot=player.combatSlots[slotIndex];if(!slot||!slot.herbId)return;const body='<div>'+t('combatAutoThresholdLabel')+'</div><input type="range" class="combat-auto-range" id="combat-auto-range" min="5" max="95" step="1" value="'+slot.threshold+'"><div class="combat-auto-stat" id="combat-auto-threshold-text"></div><div class="combat-auto-stat" id="combat-auto-current-hp"></div>';openCombatSlotOverlay(t('combatAutoThresholdTitle'),body,[{label:t('confirmNo'),action:closeCombatSlotOverlay},{label:t('combatAutoConfirm'),primary:true,action:()=>{const el=document.getElementById('combat-auto-range');slot.threshold=clamp(parseInt(el&&el.value,10)||30,5,95);slot.autoEnabled=true;closeCombatSlotOverlay();renderCombatItemBar();throttleSave();logInfo(t('combatAutoEnabled',getItemName(slot.herbId),slot.threshold));}}]);const range=document.getElementById('combat-auto-range');const thEl=document.getElementById('combat-auto-threshold-text');const hpEl=document.getElementById('combat-auto-current-hp');const sync=()=>{const v=range?parseInt(range.value,10):slot.threshold;if(thEl)thEl.textContent=t('combatAutoThresholdValue',v);if(hpEl)hpEl.textContent=t('combatAutoCurrentHp',getPlayerHpPercent());};if(range){range.addEventListener('input',sync);sync();}}function promptCombatAutoEnable(slotIndex){ensureCombatSlots();const slot=player.combatSlots[slotIndex];if(!slot||!slot.herbId)return;showConfirm(t('combatAutoEnablePrompt',getItemName(slot.herbId)),()=>showCombatAutoThreshold(slotIndex));}function bindCombatSlotButton(btn){if(!btn||btn.dataset.bound)return;btn.dataset.bound='1';const slotIndex=parseInt(btn.dataset.slot,10);let longPressTimer=null,isLongPress=false,startPos={x:0,y:0};const clearLP=()=>{if(longPressTimer){clearTimeout(longPressTimer);longPressTimer=null;}};btn.addEventListener('pointerdown',e=>{e.preventDefault();isLongPress=false;startPos={x:e.clientX,y:e.clientY};clearLP();longPressTimer=setTimeout(()=>{isLongPress=true;ensureCombatSlots();const slot=player.combatSlots[slotIndex];if(slot&&slot.herbId)promptCombatAutoEnable(slotIndex);else showCombatSlotPicker(slotIndex);},500);});btn.addEventListener('pointermove',e=>{if(Math.abs(e.clientX-startPos.x)>10||Math.abs(e.clientY-startPos.y)>10)clearLP();});btn.addEventListener('pointerup',()=>{clearLP();if(isLongPress)return;ensureCombatSlots();const slot=player.combatSlots[slotIndex];if(slot&&slot.herbId)useHerb(slot.herbId);else showCombatSlotPicker(slotIndex);});btn.addEventListener('pointerleave',clearLP);btn.addEventListener('pointercancel',clearLP);}function renderCombatItemBar(){ensureCombatSlots();for(let i=0;i<COMBAT_SLOT_COUNT;i++){const btn=document.getElementById('combat-slot-'+i);if(!btn)continue;const slot=player.combatSlots[i];btn.classList.toggle('equipped',!!slot.herbId);btn.classList.toggle('auto-on',!!(slot.herbId&&slot.autoEnabled));if(slot.herbId){const qty=getItemQty(slot.herbId);btn.innerHTML=getItemPixelIconHtml(slot.herbId,28)+'<span class="combat-slot-qty">x'+qty+'</span><span class="combat-slot-label">'+getItemName(slot.herbId)+(slot.autoEnabled?' · '+slot.threshold+'%':'')+'</span>';btn.title=getItemName(slot.herbId);}else{btn.innerHTML='<span class="combat-slot-label">'+t('combatSlotEmpty')+'</span>';btn.title=t('combatSlotEmpty');}}}function initCombatItemBar(){for(let i=0;i<COMBAT_SLOT_COUNT;i++){const btn=document.getElementById('combat-slot-'+i);bindCombatSlotButton(btn);}const ov=document.getElementById('combat-slot-overlay');if(ov&&!ov.dataset.bound){ov.dataset.bound='1';ov.addEventListener('click',e=>{if(e.target===ov)closeCombatSlotOverlay();});}renderCombatItemBar();}function tryAutoUseCombatItems(){if(!inCombat||gameOver||player.isPermanentlyDead)return;ensureCombatSlots();if(player.hp>=player.maxHp)return;const pct=getPlayerHpPercent();let safety=8;for(let i=0;i<COMBAT_SLOT_COUNT&&safety>0;i++){const slot=player.combatSlots[i];if(!slot||!slot.herbId||!slot.autoEnabled)continue;if(pct>slot.threshold)continue;if(getItemQty(slot.herbId)<1){slot.autoEnabled=false;logInfo(t('combatAutoDepleted',getItemName(slot.herbId)));continue;}if(!useHerb(slot.herbId,{auto:true}))continue;safety--;if(player.hp>=player.maxHp)break;}renderCombatItemBar();}`;

html = html.slice(0, si) + combatModule + html.slice(ei);

// --- useHerb: update auto checkAutoHerbLowStock ---
html = html.replace('checkAutoHerbLowStock(itemId);', '');

// --- LANG zh ---
html = html.replace(
  'autoHerbLabel:"自動草藥"',
  'combatSlotEmpty:"戰鬥物品",combatSlotEquipTitle:"裝備戰鬥物品",combatSlotEquipHint:"選擇回復針劑裝備至快捷欄；點擊使用、長按設定自動使用。",combatSlotUnequip:"卸下",combatSlotNoItem:"背包沒有 {0}",combatAutoEnablePrompt:"是否啟用 <b>{0}</b> 自動使用？",combatAutoThresholdTitle:"自動使用設定",combatAutoThresholdLabel:"當生命值低於以下百分比時自動使用：",combatAutoThresholdValue:"設定值：{0}%",combatAutoCurrentHp:"目前生命值：{0}%",combatAutoConfirm:"確認啟用",combatAutoEnabled:"已啟用 {0} 自動使用（HP ≤ {1}%）",combatAutoDepleted:"{0} 已用完，該欄位自動使用已關閉",autoHerbLabel:"自動草藥"'
);

// --- LANG en (find en autoHerbLabel) ---
html = html.replace(
  'autoHerbLabel:"Auto herb"',
  'combatSlotEmpty:"Combat item",combatSlotEquipTitle:"Equip combat item",combatSlotEquipHint:"Choose a recovery syringe; tap to use, long-press for auto-use.",combatSlotUnequip:"Unequip",combatSlotNoItem:"No {0} in bag",combatAutoEnablePrompt:"Enable auto-use for <b>{0}</b>?",combatAutoThresholdTitle:"Auto-use settings",combatAutoThresholdLabel:"Auto-use when HP falls below:",combatAutoThresholdValue:"Threshold: {0}%",combatAutoCurrentHp:"Current HP: {0}%",combatAutoConfirm:"Confirm",combatAutoEnabled:"Auto-use enabled for {0} (HP ≤ {1}%)",combatAutoDepleted:"{0} depleted; auto-use disabled for this slot",autoHerbLabel:"Auto herb"'
);

// --- version ---
html = html.replace(/GAME_VERSION='2\.24\.31'/, "GAME_VERSION='2.24.32'");
html = html.replace(
  "logBalanceV22431:'[功能 v2.24.31] 裝備碎片改為像素斷劍圖示；傳說與隱藏裝備碎片加入粒子光效。',logBalanceV22430:",
  "logBalanceV22432:'[功能 v2.24.32] 移除舊自動草藥；地城戰鬥新增三格戰鬥物品快捷欄（針劑裝備/使用/長按自動回血設定）。',logBalanceV22431:'[功能 v2.24.31] 裝備碎片改為像素斷劍圖示；傳說與隱藏裝備碎片加入粒子光效。',logBalanceV22430:"
);
html = html.replace(
  "logBalanceV22431:'[Feature v2.24.31] Equip fragments as broken-sword pixels; legendary/hidden fragment particles.',logBalanceV22430:",
  "logBalanceV22432:'[Feature v2.24.32] Combat item quick slots replace auto-herb; equip syringes with long-press auto-heal threshold.',logBalanceV22431:'[Feature v2.24.31] Equip fragments as broken-sword pixels; legendary/hidden fragment particles.',logBalanceV22430:"
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.31'",
  "GAME_VERSION_HISTORY=[{version:'2.24.32',date:'2026-06-09',summary:{zh:'v2.24.32 戰鬥三格快捷欄取代自動草藥。',en:'v2.24.32 combat quick slots replace auto-herb.'}},{version:'2.24.31'"
);

fs.writeFileSync(path, html);
console.log('Patched index.html for v2.24.32 combat slots');
