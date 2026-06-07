#!/usr/bin/env python3
"""Restore overload chip shop; remove decoder from Arasaka; add rename card."""
from pathlib import Path

path = Path('/workspace/index.html')
c = path.read_text(encoding='utf-8')

replacements = [
    # Shop menu tab
    (
        '<button type="button" id="shop-tab-arasaka">荒坂貨幣補給站</button></div>',
        '<button type="button" id="shop-tab-arasaka">荒坂貨幣補給站</button><button type="button" id="shop-tab-chips">超載晶片商店</button></div>',
    ),
    # Arasaka panel: drop decoder slot; add chip shop panel
    (
        '<div id="shop-arasaka-panel" style="display:none"><div id="shop-arasaka-recharge"><h4 id="shop-arasaka-recharge-title">充值超載晶片</h4><div id="shop-arasaka-packages"></div></div><div id="shop-arasaka-items"></div><button type="button" id="btn-shop-back-arasaka" class="shop-back-btn">返回</button></div><button id="btn-close-shop">關閉</button>',
        '<div id="shop-arasaka-panel" style="display:none"><div id="shop-arasaka-recharge"><h4 id="shop-arasaka-recharge-title">充值超載晶片</h4><div id="shop-arasaka-packages"></div></div><button type="button" id="btn-shop-back-arasaka" class="shop-back-btn">返回</button></div><div id="shop-chips-panel" style="display:none"><h4 id="shop-chips-items-title" style="font-size:.55rem;color:var(--chip);margin-bottom:.35rem;">晶片道具</h4><div id="shop-chips-items"></div><button type="button" id="btn-shop-back-chips" class="shop-back-btn">返回</button></div><button id="btn-close-shop">關閉</button>',
    ),
    # Chip shop CSS
    (
        '#shop-arasaka-recharge{margin-bottom:.6rem;padding:.4rem;border:1px solid #333}',
        '#shop-chips-panel{font-size:.55rem}#shop-chips-items .shop-item-price{color:var(--chip)}#shop-arasaka-recharge{margin-bottom:.6rem;padding:.4rem;border:1px solid #333}',
    ),
    # Version
    (
        "GAME_VERSION='2.4'",
        "GAME_VERSION='2.5'",
    ),
    (
        "GAME_VERSION_HISTORY=[{version:'2.4'",
        "GAME_VERSION_HISTORY=[{version:'2.5',date:'2025-06-07',summary:{zh:'超載晶片商店恢復：破解器與玩家改名卡；荒坂站移除金幣破解器。',en:'Overload chip shop restored with decoder and rename card; removed gold decoder from Arasaka.'}},{version:'2.4'",
    ),
    (
        'SAVE_VERSION=25',
        'SAVE_VERSION=26',
    ),
    # LANG zh
    (
        'overloadShopDecoder:"高級武器箱破解器"',
        (
            'overloadShopDecoder:"高級武器箱破解器",overloadShopRenameCard:"玩家改名卡",renameCard:"玩家改名卡",'
            'renameCardDesc:"使用後可更改玩家代號，每次成功改名後需等待三天才能再次使用",'
            'renameCardUseConfirm:"使用玩家改名卡將消耗一張卡片並開啟改名視窗。<br><br>成功改名後將進入 <b>三天</b> 冷卻，期間無法再次使用改名卡。<br><br>確定要使用嗎？",'
            'renameCardCooldown:"改名卡冷卻中，剩餘 {0}",renameCardCooldownDays:"{0} 天 {1} 小時",'
            'renameCardCooldownHours:"{0} 小時 {1} 分鐘",renameCardCooldownMins:"{0} 分鐘",'
            'renameCardRenameTitle:"更改玩家代號",renameCardRenameDesc:"輸入新的代號（最多12個字符）",'
            'renameCardRenameConfirm:"確認改名",'
            'renameCardUsedReminder:"改名成功！<br><br>玩家改名卡已進入 <b>三天</b> 冷卻，期間無法再次使用改名卡。"'
        ),
    ),
    # LANG en
    (
        'overloadShopDecoder:"WEAPON CRATE DECODER"',
        (
            'overloadShopDecoder:"WEAPON CRATE DECODER",overloadShopRenameCard:"PLAYER RENAME CARD",'
            'renameCard:"PLAYER RENAME CARD",'
            'renameCardDesc:"Change your player name. After each successful rename, a 3-day cooldown applies before you can use another card.",'
            'renameCardUseConfirm:"Using a rename card will consume one card and open the rename window.<br><br>After a successful rename, a <b>3-day</b> cooldown applies before you can use another card.<br><br>Continue?",'
            'renameCardCooldown:"Rename card on cooldown. Remaining: {0}",renameCardCooldownDays:"{0}d {1}h",'
            'renameCardCooldownHours:"{0}h {1}m",renameCardCooldownMins:"{0}m",'
            'renameCardRenameTitle:"CHANGE PLAYER NAME",renameCardRenameDesc:"Enter a new name (max 12 characters)",'
            'renameCardRenameConfirm:"CONFIRM RENAME",'
            'renameCardUsedReminder:"Rename successful!<br><br>Rename card is on a <b>3-day</b> cooldown before you can use another card."'
        ),
    ),
    # applyLanguage shop chips
    (
        "const _sta=document.getElementById('shop-tab-arasaka');if(_sta)_sta.textContent=t('shopTabArasaka');",
        "const _sta=document.getElementById('shop-tab-arasaka');if(_sta)_sta.textContent=t('shopTabArasaka');const _stc=document.getElementById('shop-tab-chips');if(_stc)_stc.textContent=t('shopTabOverload');const _sci=document.getElementById('shop-chips-items-title');if(_sci)_sci.textContent=t('overloadShopItemsTitle');const _sbc=document.getElementById('btn-shop-back-chips');if(_sbc)_sbc.textContent=t('shopBack');",
    ),
    # Shop listeners
    (
        "document.getElementById('shop-tab-arasaka').addEventListener('click',()=>switchShopTab('arasaka'));",
        "document.getElementById('shop-tab-arasaka').addEventListener('click',()=>switchShopTab('arasaka'));document.getElementById('shop-tab-chips').addEventListener('click',()=>switchShopTab('chips'));document.getElementById('btn-shop-back-chips').addEventListener('click',showShopMenu);",
    ),
    # ITEMS + default player
    (
        "weaponCrateDecoder:{type:'material'}};",
        "weaponCrateDecoder:{type:'material'},renameCard:{type:'rename'}};",
    ),
    (
        "isPermanentlyDead:false};}",
        "isPermanentlyDead:false,renameCardCooldownUntil:0};}",
    ),
    # migrateSave v26
    (
        "function migrateSave(data){if(data.version<25)",
        "function migrateSave(data){if(data.version<26){if(data.player.renameCardCooldownUntil===undefined)data.player.renameCardCooldownUntil=0;data.version=26;}if(data.version<25)",
    ),
    # Remove Arasaka decoder price
    (
        ',ARASAKA_DECODER_PRICE=80000',
        '',
    ),
    (
        'function getArasakaDecoderPrice(){return ARASAKA_DECODER_PRICE;}',
        '',
    ),
    # Chip shop items constant (before selectedRechargePkg)
    (
        'let selectedRechargePkg=null;',
        "const OVERLOAD_CHIP_SHOP_ITEMS=[{itemId:'weaponCrateDecoder',qty:1,chips:300,labelKey:'overloadShopDecoder'},{itemId:'renameCard',qty:1,chips:60,labelKey:'overloadShopRenameCard'}];let selectedRechargePkg=null;",
    ),
    # renderArasakaShop: recharge only
    (
        'function renderArasakaShop(){const pkgEl=document.getElementById(\'shop-arasaka-packages\');if(pkgEl){pkgEl.innerHTML=\'\';OVERLOAD_CHIP_PACKAGES.forEach(pkg=>{const btn=document.createElement(\'button\');btn.type=\'button\';btn.className=\'chip-package-btn\';btn.innerHTML=\'<span>\'+t(\'overloadBuyChips\',pkg.chips,pkg.priceLabel)+\'</span><span>\'+t(\'overloadRechargeBtn\')+\'</span>\';btn.addEventListener(\'click\',()=>openRechargeOverlay(pkg.id));pkgEl.appendChild(btn);});}const el=document.getElementById(\'shop-arasaka-items\');if(!el)return;const price=getArasakaDecoderPrice();el.innerHTML=`<div class="shop-item"><div class="shop-item-info">${itemToString(\'weaponCrateDecoder\').replace(/x\\d+/,\'\')}<div style="font-size:0.5rem;color:#888;margin-top:0.2rem;">${t(\'weaponCrateDecoderDesc\')}</div></div><span class="shop-item-price">${t(\'arasakaDecoderPrice\',price)}</span><button id="btn-buy-decoder">${t(\'shopBuy\')}</button></div>`;const btn=document.getElementById(\'btn-buy-decoder\');if(btn){btn.disabled=player.gold<price;btn.addEventListener(\'click\',()=>{const p=getArasakaDecoderPrice();if(player.gold<p){logInfo(t(\'shopNeedGold\'));return;}if(!addItem(\'weaponCrateDecoder\',1))return;player.gold-=p;logInfo(t(\'shopBuySuccess\',getItemName(\'weaponCrateDecoder\')));renderArasakaShop();renderAllPanels();updateStatusBar();throttleSave();});}}',
        "function renderArasakaShop(){const pkgEl=document.getElementById('shop-arasaka-packages');if(!pkgEl)return;pkgEl.innerHTML='';OVERLOAD_CHIP_PACKAGES.forEach(pkg=>{const btn=document.createElement('button');btn.type='button';btn.className='chip-package-btn';btn.innerHTML='<span>'+t('overloadBuyChips',pkg.chips,pkg.priceLabel)+'</span><span>'+t('overloadRechargeBtn')+'</span>';btn.addEventListener('click',()=>openRechargeOverlay(pkg.id));pkgEl.appendChild(btn);});}function renderOverloadChipShop(){const itemsEl=document.getElementById('shop-chips-items');if(!itemsEl)return;itemsEl.innerHTML='';OVERLOAD_CHIP_SHOP_ITEMS.forEach(entry=>{const div=document.createElement('div');div.className='shop-item';const label=t(entry.labelKey);div.innerHTML='<div class=\"shop-item-info\">'+label+'<div style=\"font-size:0.5rem;color:#888;margin-top:0.2rem;\">'+itemToString(entry.itemId).replace(/x\\d+/,'')+' x'+entry.qty+'</div></div><span class=\"shop-item-price\">'+t('overloadChipCost',entry.chips)+'</span>';const btn=document.createElement('button');btn.textContent=t('shopBuy');btn.disabled=(player.overloadChips||0)<entry.chips;btn.addEventListener('click',()=>{if((player.overloadChips||0)<entry.chips){logInfo(t('overloadNeedChips'));return;}if(!addItem(entry.itemId,entry.qty))return;player.overloadChips-=entry.chips;logInfo(t('overloadBuySuccess',label));renderOverloadChipShop();updateStatusBar();throttleSave();});div.appendChild(btn);itemsEl.appendChild(div);});}",
    ),
    # showShopMenu + switchShopTab
    (
        "function showShopMenu(){currentShopView='menu';const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');if(menu)menu.style.display='flex';if(equipPanel)equipPanel.style.display='none';if(arasakaPanel)arasakaPanel.style.display='none';}",
        "function showShopMenu(){currentShopView='menu';const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');const chipsPanel=document.getElementById('shop-chips-panel');if(menu)menu.style.display='flex';if(equipPanel)equipPanel.style.display='none';if(arasakaPanel)arasakaPanel.style.display='none';if(chipsPanel)chipsPanel.style.display='none';}",
    ),
    (
        "function switchShopTab(tab){currentShopView=tab;const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');if(menu)menu.style.display='none';if(equipPanel)equipPanel.style.display=tab==='equip'?'block':'none';if(arasakaPanel)arasakaPanel.style.display=tab==='arasaka'?'block':'none';if(tab==='equip'){if(!player.shopItems||player.shopItems.length===0)refreshShop();else renderShop();}if(tab==='arasaka')renderArasakaShop();}",
        "function switchShopTab(tab){currentShopView=tab;const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');const chipsPanel=document.getElementById('shop-chips-panel');if(menu)menu.style.display='none';if(equipPanel)equipPanel.style.display=tab==='equip'?'block':'none';if(arasakaPanel)arasakaPanel.style.display=tab==='arasaka'?'block':'none';if(chipsPanel)chipsPanel.style.display=tab==='chips'?'block':'none';if(tab==='equip'){if(!player.shopItems||player.shopItems.length===0)refreshShop();else renderShop();}if(tab==='arasaka')renderArasakaShop();if(tab==='chips')renderOverloadChipShop();}",
    ),
    # Item helpers
    (
        "weaponCrateDecoder:'weaponCrateDecoder'};return t(names[itemId]||itemId);}",
        "weaponCrateDecoder:'weaponCrateDecoder',renameCard:'renameCard'};return t(names[itemId]||itemId);}",
    ),
    (
        "weaponCrateDecoder:'%'};return icons[itemId]||'?';}",
        "weaponCrateDecoder:'%',renameCard:'~'};return icons[itemId]||'?';}",
    ),
    (
        "weaponCrateDecoder:'weaponCrateDecoderDesc'};return descs[itemId]?t(descs[itemId]):'';}",
        "weaponCrateDecoder:'weaponCrateDecoderDesc',renameCard:'renameCardDesc'};return descs[itemId]?t(descs[itemId]):'';}",
    ),
    (
        "'encryptedWeaponCrate','weaponCrateDecoder'];",
        "'encryptedWeaponCrate','weaponCrateDecoder','renameCard'];",
    ),
    # Rename card use flow (after promptNewPlayerName)
    (
        "document.addEventListener('keydown',handleEsc);}",
        "document.addEventListener('keydown',handleEsc);}const RENAME_CARD_COOLDOWN_MS=3*24*60*60*1000;function getRenameCardCooldownRemaining(){const until=player.renameCardCooldownUntil||0;return Math.max(0,until-Date.now());}function formatRenameCardCooldown(ms){const totalSec=Math.ceil(ms/1000);const days=Math.floor(totalSec/86400);const hours=Math.floor((totalSec%86400)/3600);const mins=Math.floor((totalSec%3600)/60);if(days>0)return t('renameCardCooldownDays',days,hours);if(hours>0)return t('renameCardCooldownHours',hours,mins);return t('renameCardCooldownMins',mins);}function promptPlayerRename(onSuccess,onCancel){const overlay=document.getElementById('name-input-overlay');const box=overlay.querySelector('h3');const descEl=document.getElementById('name-input-desc');const input=document.getElementById('name-input-field');const confirmBtn=document.getElementById('name-input-confirm');const errorSpan=document.getElementById('name-input-error');const hintEl=document.getElementById('name-input-hint');const orig={title:box.textContent,desc:descEl.innerHTML,confirm:confirmBtn.textContent,hint:hintEl.style.display};box.textContent=t('renameCardRenameTitle');descEl.innerHTML=t('renameCardRenameDesc');confirmBtn.textContent=t('renameCardRenameConfirm');hintEl.style.display='none';overlay.style.display='flex';input.value=playerCustomName||'';input.classList.remove('error');errorSpan.classList.remove('show');input.focus();input.select();const restore=()=>{box.textContent=orig.title;descEl.innerHTML=orig.desc;confirmBtn.textContent=orig.confirm;hintEl.style.display=orig.hint;};const cleanup=()=>{confirmBtn.removeEventListener('click',handleConfirm);input.removeEventListener('keydown',handleKey);document.removeEventListener('keydown',handleEsc);};const finish=(fn)=>{overlay.style.display='none';cleanup();restore();if(fn)fn();};const handleConfirm=()=>{const raw=input.value.trim();if(raw==''){input.classList.add('error');errorSpan.classList.add('show');input.focus();setTimeout(()=>{input.classList.remove('error');},300);return;}finish(()=>onSuccess(raw.substring(0,12)));};const handleKey=(e)=>{if(e.key==='Enter'){e.preventDefault();handleConfirm();}};const handleEsc=(e)=>{if(e.key==='Escape'){e.preventDefault();finish(onCancel);}};confirmBtn.addEventListener('click',handleConfirm);input.addEventListener('keydown',handleKey);document.addEventListener('keydown',handleEsc);}function useRenameCard(){if(getItemQty('renameCard')<=0)return;const remain=getRenameCardCooldownRemaining();if(remain>0){showAlert(t('renameCardCooldown',formatRenameCardCooldown(remain)));return;}showConfirm(t('renameCardUseConfirm'),()=>{promptPlayerRename((name)=>{if(!removeItem('renameCard',1))return;player.renameCardCooldownUntil=Date.now()+RENAME_CARD_COOLDOWN_MS;savePlayerName(name);renderAllPanels();updateStatusBar();throttleSave();showAlert(t('renameCardUsedReminder'));});});}",
    ),
    # showItemAction rename button
    (
        "equipActionBtns.appendChild(dec2);}}const closeBtn=document.createElement('button');",
        "equipActionBtns.appendChild(dec2);}}if(item&&item.type==='rename'&&getItemQty(itemId)>0){const useRenameBtn=document.createElement('button');useRenameBtn.className='btn-equip';useRenameBtn.textContent=t('itemUseBtn');useRenameBtn.addEventListener('click',()=>{equipActionOverlay.style.display='none';useRenameCard();});equipActionBtns.appendChild(useRenameBtn);}const closeBtn=document.createElement('button');",
    ),
    # addItemLongPress tap
    (
        "else if(item&&item.type==='crate')decryptWeaponCrate(false);});",
        "else if(item&&item.type==='crate')decryptWeaponCrate(false);else if(item&&item.type==='rename')useRenameCard();});",
    ),
]

for i, (old, new) in enumerate(replacements):
    if old not in c:
        raise SystemExit(f'MISSING patch {i}: {old[:120]}...')
    c = c.replace(old, new, 1)

checks = [
    'shop-tab-chips', 'shop-chips-panel', 'renderOverloadChipShop',
    'OVERLOAD_CHIP_SHOP_ITEMS', 'renameCard', 'useRenameCard',
    'getArasakaDecoderPrice', 'shop-arasaka-items',
]
for pat in checks:
    count = c.count(pat)
    if pat == 'getArasakaDecoderPrice' or pat == 'shop-arasaka-items':
        if count > 0:
            print(f'warning: should remove {pat}, found {count}')
    elif count == 0:
        raise SystemExit(f'MISSING after patch: {pat}')

path.write_text(c, encoding='utf-8')
print('Applied chip shop + rename card patches')
