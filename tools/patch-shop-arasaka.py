#!/usr/bin/env python3
"""Move chip recharge to Arasaka shop; remove overload chip shop tab/items."""
from pathlib import Path

path = Path('/workspace/index.html')
c = path.read_text(encoding='utf-8')

replacements = [
    (
        '<button type="button" id="shop-tab-arasaka">荒坂貨幣補給站</button><button type="button" id="shop-tab-chips">超載晶片商店</button>',
        '<button type="button" id="shop-tab-arasaka">荒坂貨幣補給站</button>',
    ),
    (
        '<div id="shop-arasaka-panel" style="display:none"><div id="shop-arasaka-items"></div><button type="button" id="btn-shop-back-arasaka" class="shop-back-btn">返回</button></div><div id="shop-chips-panel" style="display:none"><div id="shop-chips-recharge"><h4 id="shop-chips-recharge-title">充值超載晶片</h4><div id="shop-chips-packages"></div></div><h4 id="shop-chips-items-title" style="font-size:.55rem;color:var(--chip);margin-bottom:.35rem;">晶片道具</h4><div id="shop-chips-items"></div><button type="button" id="btn-shop-back-chips" class="shop-back-btn">返回</button></div>',
        '<div id="shop-arasaka-panel" style="display:none"><div id="shop-arasaka-recharge"><h4 id="shop-arasaka-recharge-title">充值超載晶片</h4><div id="shop-arasaka-packages"></div></div><button type="button" id="btn-shop-back-arasaka" class="shop-back-btn">返回</button></div>',
    ),
    (
        '#shop-chips-panel{font-size:.55rem}#shop-chips-recharge{margin-bottom:.6rem;padding:.4rem;border:1px solid #333}#shop-chips-recharge h4{margin-bottom:.35rem;color:var(--chip);font-size:.55rem}#shop-chips-packages{display:flex;flex-direction:column;gap:.25rem;margin-bottom:.4rem}.chip-package-btn{width:100%;padding:.4rem;background:0 0;border:1px solid #333;color:#aaa;font-family:inherit;font-size:.55rem;cursor:pointer;text-align:left;display:flex;justify-content:space-between;align-items:center}.chip-package-btn:active{border-color:var(--chip);color:var(--chip)}#shop-chips-items .shop-item-price{color:var(--chip)}',
        '#shop-arasaka-recharge{margin-bottom:.6rem;padding:.4rem;border:1px solid #333}#shop-arasaka-recharge h4{margin-bottom:.35rem;color:var(--chip);font-size:.55rem}#shop-arasaka-packages{display:flex;flex-direction:column;gap:.25rem;margin-bottom:.4rem}.chip-package-btn{width:100%;padding:.4rem;background:0 0;border:1px solid #333;color:#aaa;font-family:inherit;font-size:.55rem;cursor:pointer;text-align:left;display:flex;justify-content:space-between;align-items:center}.chip-package-btn:active{border-color:var(--chip);color:var(--chip)}',
    ),
    (
        "const _scr=document.getElementById('shop-chips-recharge-title');if(_scr)_scr.textContent=t('overloadShopRechargeTitle');const _sci=document.getElementById('shop-chips-items-title');if(_sci)_sci.textContent=t('overloadShopItemsTitle');",
        "const _scr=document.getElementById('shop-arasaka-recharge-title');if(_scr)_scr.textContent=t('overloadShopRechargeTitle');",
    ),
    (
        "const _stc=document.getElementById('shop-tab-chips');if(_stc)_stc.textContent=t('shopTabOverload');",
        '',
    ),
    (
        "document.getElementById('shop-tab-chips').addEventListener('click',()=>switchShopTab('chips'));document.getElementById('btn-shop-back-chips').addEventListener('click',showShopMenu);",
        '',
    ),
    (
        "const _sbc=document.getElementById('btn-shop-back-chips');if(_sbc)_sbc.textContent=t('shopBack');",
        '',
    ),
    (
        "const OVERLOAD_CHIP_SHOP_ITEMS=[{itemId:'weaponCrateDecoder',qty:1,chips:300,labelKey:'overloadShopDecoder'}];",
        '',
    ),
    (
        "function renderArasakaShop(){const el=document.getElementById('shop-arasaka-items');if(!el)return;const price=getArasakaDecoderPrice();el.innerHTML=`<div class=\"shop-item\"><div class=\"shop-item-info\">${itemToString('weaponCrateDecoder').replace(/x\\d+/,'')}<div style=\"font-size:0.5rem;color:#888;margin-top:0.2rem;\">${t('weaponCrateDecoderDesc')}</div></div><span class=\"shop-item-price\">${t('arasakaDecoderPrice',price)}</span><button id=\"btn-buy-decoder\">${t('shopBuy')}</button></div>`;const btn=document.getElementById('btn-buy-decoder');if(btn){btn.disabled=player.gold<price;btn.addEventListener('click',()=>{const p=getArasakaDecoderPrice();if(player.gold<p){logInfo(t('shopNeedGold'));return;}if(!addItem('weaponCrateDecoder',1))return;player.gold-=p;logInfo(t('shopBuySuccess',getItemName('weaponCrateDecoder')));renderArasakaShop();renderAllPanels();updateStatusBar();throttleSave();});}}",
        "function renderArasakaShop(){const pkgEl=document.getElementById('shop-arasaka-packages');if(!pkgEl)return;pkgEl.innerHTML='';OVERLOAD_CHIP_PACKAGES.forEach(pkg=>{const btn=document.createElement('button');btn.type='button';btn.className='chip-package-btn';btn.innerHTML='<span>'+t('overloadBuyChips',pkg.chips,pkg.priceLabel)+'</span><span>'+t('overloadRechargeBtn')+'</span>';btn.addEventListener('click',()=>openRechargeOverlay(pkg.id));pkgEl.appendChild(btn);});}",
    ),
    (
        "function renderOverloadChipShop(){const pkgEl=document.getElementById('shop-chips-packages');if(pkgEl){pkgEl.innerHTML='';OVERLOAD_CHIP_PACKAGES.forEach(pkg=>{const btn=document.createElement('button');btn.type='button';btn.className='chip-package-btn';btn.innerHTML='<span>'+t('overloadBuyChips',pkg.chips,pkg.priceLabel)+'</span><span>'+t('overloadRechargeBtn')+'</span>';btn.addEventListener('click',()=>openRechargeOverlay(pkg.id));pkgEl.appendChild(btn);});}const itemsEl=document.getElementById('shop-chips-items');if(!itemsEl)return;itemsEl.innerHTML='';OVERLOAD_CHIP_SHOP_ITEMS.forEach(entry=>{const div=document.createElement('div');div.className='shop-item';const label=t(entry.labelKey);div.innerHTML='<div class=\"shop-item-info\">'+label+'<div style=\"font-size:0.5rem;color:#888;margin-top:0.2rem;\">'+itemToString(entry.itemId).replace(/x\\d+/,'')+' x'+entry.qty+'</div></div><span class=\"shop-item-price\">'+t('overloadChipCost',entry.chips)+'</span>';const btn=document.createElement('button');btn.textContent=t('shopBuy');btn.disabled=(player.overloadChips||0)<entry.chips;btn.addEventListener('click',()=>{if((player.overloadChips||0)<entry.chips){logInfo(t('overloadNeedChips'));return;}if(!addItem(entry.itemId,entry.qty))return;player.overloadChips-=entry.chips;logInfo(t('overloadBuySuccess',label));renderOverloadChipShop();updateStatusBar();throttleSave();});div.appendChild(btn);itemsEl.appendChild(div);});}",
        '',
    ),
    (
        "function showShopMenu(){currentShopView='menu';const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');const chipsPanel=document.getElementById('shop-chips-panel');if(menu)menu.style.display='flex';if(equipPanel)equipPanel.style.display='none';if(arasakaPanel)arasakaPanel.style.display='none';if(chipsPanel)chipsPanel.style.display='none';}",
        "function showShopMenu(){currentShopView='menu';const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');if(menu)menu.style.display='flex';if(equipPanel)equipPanel.style.display='none';if(arasakaPanel)arasakaPanel.style.display='none';}",
    ),
    (
        "function switchShopTab(tab){currentShopView=tab;const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');const chipsPanel=document.getElementById('shop-chips-panel');if(menu)menu.style.display='none';if(equipPanel)equipPanel.style.display=tab==='equip'?'block':'none';if(arasakaPanel)arasakaPanel.style.display=tab==='arasaka'?'block':'none';if(chipsPanel)chipsPanel.style.display=tab==='chips'?'block':'none';if(tab==='equip'){if(!player.shopItems||player.shopItems.length===0)refreshShop();else renderShop();}if(tab==='arasaka')renderArasakaShop();if(tab==='chips')renderOverloadChipShop();}",
        "function switchShopTab(tab){currentShopView=tab;const menu=document.getElementById('shop-menu-panel');const equipPanel=document.getElementById('shop-equip-panel');const arasakaPanel=document.getElementById('shop-arasaka-panel');if(menu)menu.style.display='none';if(equipPanel)equipPanel.style.display=tab==='equip'?'block':'none';if(arasakaPanel)arasakaPanel.style.display=tab==='arasaka'?'block':'none';if(tab==='equip'){if(!player.shopItems||player.shopItems.length===0)refreshShop();else renderShop();}if(tab==='arasaka')renderArasakaShop();}",
    ),
    (
        'renderOverloadChipShop()',
        'renderArasakaShop()',
        True,
    ),
    (
        ',ARASAKA_DECODER_PRICE=80000',
        '',
    ),
    (
        'function getArasakaDecoderPrice(){return ARASAKA_DECODER_PRICE;}',
        '',
    ),
]

for i, item in enumerate(replacements):
    replace_all = False
    if len(item) == 3:
        old, new, replace_all = item
    else:
        old, new = item
    if old and old not in c:
        raise SystemExit(f'MISSING patch {i}: {old[:100]}...')
    if old:
        c = c.replace(old, new, c.count(old) if replace_all else 1)

leftovers = ['shop-chips', 'renderOverloadChipShop', 'OVERLOAD_CHIP_SHOP_ITEMS', 'shop-tab-chips']
for pat in leftovers:
    if pat in c:
        print(f'warning: leftover {pat} x{c.count(pat)}')

path.write_text(c, encoding='utf-8')
print('Applied shop arasaka patches')
