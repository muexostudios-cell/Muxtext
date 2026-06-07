#!/usr/bin/env python3
"""Shop theme colors + item color coding for decoder/crate/rename card."""
from pathlib import Path

path = Path('/workspace/index.html')
c = path.read_text(encoding='utf-8')

replacements = [
    # CSS variables
    (
        '--chip:#00e5ff}',
        '--chip:#00e5ff;--item-red:#ff4444;--shop-blue:#4488ff}',
    ),
    # Shop panel themes
    (
        '#shop-arasaka-panel{text-align:center;padding:2rem .5rem;color:#666;font-size:.6rem}#shop-chips-panel{font-size:.55rem}#shop-chips-items .shop-item-price{color:var(--chip)}#shop-arasaka-recharge{margin-bottom:.6rem;padding:.4rem;border:1px solid #333}#shop-arasaka-recharge h4{margin-bottom:.35rem;color:var(--chip);font-size:.55rem}#shop-arasaka-packages{display:flex;flex-direction:column;gap:.25rem;margin-bottom:.4rem}.chip-package-btn{width:100%;padding:.4rem;background:0 0;border:1px solid #333;color:#aaa;font-family:inherit;font-size:.55rem;cursor:pointer;text-align:left;display:flex;justify-content:space-between;align-items:center}.chip-package-btn:active{border-color:var(--chip);color:var(--chip)}',
        '#shop-tab-arasaka{color:var(--gold);border-color:#554400}#shop-tab-chips{color:var(--shop-blue);border-color:#224466}#shop-arasaka-panel{text-align:center;padding:2rem .5rem;color:var(--gold);font-size:.6rem}#shop-arasaka-recharge{margin-bottom:.6rem;padding:.4rem;border:1px solid var(--gold)}#shop-arasaka-recharge h4{margin-bottom:.35rem;color:var(--gold);font-size:.55rem}#shop-arasaka-packages{display:flex;flex-direction:column;gap:.25rem;margin-bottom:.4rem}#shop-arasaka-panel .chip-package-btn{width:100%;padding:.4rem;background:0 0;border:1px solid #554400;color:var(--gold);font-family:inherit;font-size:.55rem;cursor:pointer;text-align:left;display:flex;justify-content:space-between;align-items:center}#shop-arasaka-panel .chip-package-btn:active{border-color:var(--gold);color:#fff;background:#221a00}#shop-arasaka-panel .shop-back-btn{border-color:var(--gold);color:var(--gold)}#shop-chips-panel{font-size:.55rem;color:var(--shop-blue)}#shop-chips-items-title{color:var(--shop-blue)!important}#shop-chips-items .shop-item-price{color:var(--shop-blue)}#shop-chips-panel .shop-item{border-color:#1a2a44}#shop-chips-panel .shop-item button{border-color:#224466;color:var(--shop-blue)}#shop-chips-panel .shop-item button:active{border-color:var(--shop-blue);color:#fff;background:#001a33}#shop-chips-panel .shop-back-btn{border-color:var(--shop-blue);color:var(--shop-blue)}.chip-package-btn{width:100%;padding:.4rem;background:0 0;border:1px solid #333;color:#aaa;font-family:inherit;font-size:.55rem;cursor:pointer;text-align:left;display:flex;justify-content:space-between;align-items:center}.chip-package-btn:active{border-color:var(--chip);color:var(--chip)}',
    ),
    # Inventory item slot colors
    (
        '.equip-slot.item-crate{border-left-color:#ff4444}',
        '.equip-slot.item-crate{border-left-color:var(--item-red);color:var(--item-red)}.equip-slot.item-decoder{border-left-color:var(--item-red);color:var(--item-red)}.equip-slot.item-rename{border-left-color:var(--shop-blue);color:var(--shop-blue)}',
    ),
    # Item color helpers
    (
        'function getItemName(itemId){',
        "function getItemColor(itemId){if(itemId==='encryptedWeaponCrate'||itemId==='weaponCrateDecoder')return 'var(--item-red)';if(itemId==='renameCard')return 'var(--shop-blue)';const item=ITEMS[itemId];if(item&&item.type==='herb')return '#fff';return '#fff';}function formatItemName(itemId){return `<span style=\"color:${getItemColor(itemId)}\">${getItemName(itemId)}</span>`;}function logItemLoot(itemId){logInfo(t('msgLootItem',formatItemName(itemId)));}function getItemName(itemId){",
    ),
    (
        "function getItemTypeClass(itemId){const item=ITEMS[itemId];if(!item)return 'item-material';if(item.type==='crate')return 'item-crate';return item.type==='herb'?'item-herb':'item-material';}",
        "function getItemTypeClass(itemId){if(itemId==='weaponCrateDecoder')return 'item-decoder';if(itemId==='renameCard')return 'item-rename';const item=ITEMS[itemId];if(!item)return 'item-material';if(item.type==='crate')return 'item-crate';return item.type==='herb'?'item-herb':'item-material';}",
    ),
    (
        "function itemToString(itemId){const item=ITEMS[itemId];const nameColor=item&&item.type==='crate'?'#ff4444':item&&item.type==='herb'?'#fff':'#fff';return `<b style=\"color:${nameColor}\">${getItemIcon(itemId)} ${getItemName(itemId)}</b> <span style=\"color:#666;\">x${getItemQty(itemId)}</span>`;}",
        "function itemToString(itemId){const nameColor=getItemColor(itemId);return `<b style=\"color:${nameColor}\">${getItemIcon(itemId)} ${getItemName(itemId)}</b> <span style=\"color:#666;\">x${getItemQty(itemId)}</span>`;}",
    ),
    # Encrypted crate drop log
    (
        "logInfo(t('msgLootItem',getItemName('encryptedWeaponCrate')));if(lootArea)lootArea.innerHTML+=`<br><span style=\"color:#ff4444\">! ${getItemName('encryptedWeaponCrate')}</span>`;",
        "logItemLoot('encryptedWeaponCrate');if(lootArea)lootArea.innerHTML+=`<br><span style=\"color:var(--item-red)\">! ${getItemName('encryptedWeaponCrate')}</span>`;",
    ),
    # Chip shop item labels
    (
        "div.innerHTML='<div class=\"shop-item-info\">'+label+'<div style=\"font-size:0.5rem;color:#888;margin-top:0.2rem;\">'+itemToString(entry.itemId).replace(/x\\d+/,'')+' x'+entry.qty+'</div></div><span class=\"shop-item-price\">'+t('overloadChipCost',entry.chips)+'</span>';",
        "const itemColor=getItemColor(entry.itemId);div.innerHTML='<div class=\"shop-item-info\"><div style=\"color:'+itemColor+'\">'+label+'</div><div style=\"font-size:0.5rem;color:#888;margin-top:0.2rem;\">'+itemToString(entry.itemId).replace(/x\\d+/,'')+' x'+entry.qty+'</div></div><span class=\"shop-item-price\">'+t('overloadChipCost',entry.chips)+'</span>';",
    ),
    # Drone loot material list
    (
        'html+=`<div style="margin:0.12rem 0;color:#aaa;">${getDroneMaterialName(id)} x${summary.materials[id]}</div>`;',
        'html+=`<div style="margin:0.12rem 0;">${formatItemName(id)} <span style="color:#666;">x${summary.materials[id]}</span></div>`;',
    ),
    # Item detail overlay
    (
        "function getItemDetailHtml(itemId){const desc=getItemDesc(itemId);const item=ITEMS[itemId];const itemColor=item&&item.type==='crate'?'#ff4444':item&&item.type==='herb'?'var(--heal)':'#fff';let html=`<div style=\"color:${itemColor};font-size:0.65rem;margin-bottom:0.3rem;\">${getItemName(itemId)}</div>`;",
        "function getItemDetailHtml(itemId){const desc=getItemDesc(itemId);const itemColor=getItemColor(itemId);let html=`<div style=\"color:${itemColor};font-size:0.65rem;margin-bottom:0.3rem;\">${getItemName(itemId)}</div>`;",
    ),
    # Version
    (
        "GAME_VERSION='2.5'",
        "GAME_VERSION='2.5.1'",
    ),
    (
        "GAME_VERSION_HISTORY=[{version:'2.5'",
        "GAME_VERSION_HISTORY=[{version:'2.5.1',date:'2025-06-07',summary:{zh:'商店與道具配色：荒坂站金色、晶片店藍色；破解器/武器箱紅色、改名卡藍色。',en:'Shop and item colors: Arasaka gold, chip shop blue; decoder/crate red, rename card blue.'}},{version:'2.5'",
    ),
]

for i, (old, new) in enumerate(replacements):
    if old not in c:
        raise SystemExit(f'MISSING patch {i}: {old[:100]}...')
    c = c.replace(old, new, 1)

for pat in ['getItemColor', 'item-decoder', 'item-rename', '--shop-blue', '#shop-tab-arasaka{color']:
    if pat not in c:
        raise SystemExit(f'MISSING after patch: {pat}')

path.write_text(c, encoding='utf-8')
print('Applied shop/item color patches')
