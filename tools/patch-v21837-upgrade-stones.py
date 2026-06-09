#!/usr/bin/env python3
"""Add rare/epic/hidden upgrade stones, +10 rare/epic enhance, tiered drops."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def main():
    s = INDEX.read_text(encoding="utf-8")

    # Version
    s = s.replace("GAME_VERSION='2.18.36'", "GAME_VERSION='2.18.37'")
    s = s.replace(
        "GAME_VERSION_HISTORY=[{version:'2.18.35'",
        "GAME_VERSION_HISTORY=[{version:'2.18.37',date:'2026-06-09',summary:{zh:'v2.18.37 新增稀有／史詩／隱藏升級石；稀有與史詩裝備可強化至 +10，掉落與數值依稀有度平衡。',en:'v2.18.37 rare/epic/hidden upgrade stones; rare & epic gear +10 enhance with rarity-balanced drops and stats.'}},{version:'2.18.35'",
    )
    s = s.replace(
        'logBalanceV2195:"[功能 v2.18.36]',
        'logBalanceV2196:"[功能 v2.18.37] 新增稀有／史詩／隱藏升級石（顏色對應裝備稀有度）；稀有與史詩裝備可強化至 +10，掉落率與強化數值依稀有度平衡。",logBalanceV2195:"[功能 v2.18.36]',
    )

    # LANG zh
    s = s.replace(
        'upgradeStone:"史詩升級石",hellTicket:',
        'upgradeStoneRare:"稀有升級石",upgradeStoneRareDesc:"用於強化稀有裝備至 +10。",upgradeStone:"史詩升級石",upgradeStoneDesc:"用於強化史詩與傳說裝備至 +10。",upgradeStoneHidden:"隱藏升級石",upgradeStoneHiddenDesc:"用於強化隱藏裝備至 +10。",hellTicket:',
    )
    s = s.replace(
        'upgradeFailMsg:"強化失敗！史詩升級石已消耗。"',
        'upgradeFailMsg:"強化失敗！{0} 已消耗。",upgradeMaxMsg:"已達強化上限 +{0}",upgradeNeedStone:"{0} 不足！需要 {1} 顆",upgradeConfirm:"強化 +{0}\\n需求: {1} {2}\\n成功率: {3}%"',
    )

    # LANG en
    s = s.replace(
        'upgradeStone:"UPGRADE_STONE",hellTicket:',
        'upgradeStoneRare:"RARE UPGRADE STONE",upgradeStoneRareDesc:"Enhance rare gear up to +10.",upgradeStone:"EPIC UPGRADE STONE",upgradeStoneDesc:"Enhance epic & legendary gear up to +10.",upgradeStoneHidden:"HIDDEN UPGRADE STONE",upgradeStoneHiddenDesc:"Enhance hidden gear up to +10.",hellTicket:',
    )
    s = s.replace(
        'upgradeFailMsg:"Enhancement failed! Upgrade stone consumed."',
        'upgradeFailMsg:"Enhancement failed! {0} consumed.",upgradeMaxMsg:"Max enhancement +{0}",upgradeNeedStone:"Not enough {0}! Need {1}",upgradeConfirm:"Enhance +{0}\\nCost: {1} {2}\\nSuccess: {3}%"',
    )

    # CSS border colors for upgrade stones
    s = s.replace(
        ".equip-slot.item-herb{border-left-color:var(--heal)}",
        ".equip-slot.item-herb{border-left-color:var(--heal)}.equip-slot.item-stone-rare{border-left-color:var(--rare)}.equip-slot.item-stone-epic{border-left-color:var(--epic)}.equip-slot.item-stone-hidden{border-left-color:var(--hidden)}",
    )

    # ITEMS
    s = s.replace(
        "upgradeStone:{type:'material'},hellTicket:",
        "upgradeStoneRare:{type:'material',upgradeRarity:'rare'},upgradeStone:{type:'material',upgradeRarity:'epic'},upgradeStoneHidden:{type:'material',upgradeRarity:'hidden'},hellTicket:",
    )

    # Display order
    s = s.replace(
        "ITEM_DISPLAY_ORDER=['herb_low','herb_mid','herb_high','upgradeStone','hellTicket'",
        "ITEM_DISPLAY_ORDER=['herb_low','herb_mid','herb_high','upgradeStoneRare','upgradeStone','upgradeStoneHidden','hellTicket'",
    )

    # Upgrade config + helpers (before getUpgradeStoneDropRate)
    upgrade_block = (
        "const UPGRADE_MAX_LV=10;const UPGRADE_STONE_BY_RARITY={rare:'upgradeStoneRare',epic:'upgradeStone',legendary:'upgradeStone',hidden:'upgradeStoneHidden'};"
        "const UPGRADE_SCALE={rare:0.48,epic:0.72,legendary:1,hidden:1.12};"
        "const UPGRADE_TARGET_RM={rare:1.45,epic:2.2,legendary:3.5};"
        "function getUpgradeStoneIdForEquip(rarity){return UPGRADE_STONE_BY_RARITY[rarity]||null;}"
        "function canEquipUpgrade(rarity){return !!getUpgradeStoneIdForEquip(rarity);}"
        "function getUpgradeStoneCost(targetLv,rarity){const mult={rare:1,epic:1,legendary:1,hidden:1.25};return Math.max(1,Math.ceil(targetLv*(mult[rarity]||1)));}"
        "function getUpgradeSuccessRate(targetLv,rarity){if(targetLv<=6)return 100;if(targetLv<=8)return rarity==='rare'?85:(rarity==='hidden'?80:100);if(targetLv===9)return rarity==='hidden'?45:(rarity==='rare'?70:50);return rarity==='hidden'?35:(rarity==='rare'?55:50);}"
    )
    s = s.replace("function getUpgradeStoneDropRate()", upgrade_block + "function getUpgradeStoneDropRate()")

    # Drop rates
    old_drop = (
        "function getUpgradeStoneDropRate(){if(!currentDungeon)return 0.00002;const tier=currentDungeon.tier;const floorBonus=currentDungeon.floorLevel*0.000001;let base=0.00002;if(tier==='hard')base+=0.00001;if(tier==='hell')base+=0.00003;return Math.min(0.0001,base+floorBonus);}"
    )
    new_drop = (
        "function getUpgradeStoneDropRate(){return getUpgradeStoneDropRates().epic;}"
        "function getUpgradeStoneDropRates(){if(!currentDungeon)return {rare:0,epic:0,hidden:0};const tier=currentDungeon.tier;const fl=Math.max(1,currentDungeon.floorLevel);const floorMult=1+fl*0.00002;const dropBoost=getDungeonModMult('dropMult');let rare=0.00006,epic=0.00002,hidden=0.0000015;if(tier==='hard'){rare+=0.00003;epic+=0.000012;hidden+=0.0000008;}if(tier==='hell'){rare+=0.00005;epic+=0.000025;hidden+=0.000004;}return {rare:Math.min(0.00025,rare*floorMult*dropBoost),epic:Math.min(0.00012,epic*floorMult*dropBoost),hidden:Math.min(0.00002,hidden*floorMult*dropBoost)};}"
        "function tryDropUpgradeStones(lootArea){const rates=getUpgradeStoneDropRates();const table=[['upgradeStoneHidden',rates.hidden],['upgradeStone',rates.epic],['upgradeStoneRare',rates.rare]];for(const [id,rate] of table){if(rate>0&&Math.random()<rate){addItem(id,1);if(lootArea)lootArea.innerHTML+='<br>'+getItemIcon(id)+' '+formatItemName(id);else logItemLoot(id);}}}"
    )
    if old_drop not in s:
        raise SystemExit("getUpgradeStoneDropRate block not found")
    s = s.replace(old_drop, new_drop)

    # Kill loot
    s = s.replace(
        "if(Math.random()<getUpgradeStoneDropRate()){addItem('upgradeStone',1);lootArea.innerHTML+='<br>* 史詩升級石';}",
        "tryDropUpgradeStones(lootArea);",
    )

    # Cache cell
    s = s.replace(
        "}else if(roll<0.55){addItem('upgradeStone',1);logItemLoot('upgradeStone');}",
        "}else if(roll<0.55){const sr=Math.random();if(sr<0.55){addItem('upgradeStoneRare',1);logItemLoot('upgradeStoneRare');}else if(sr<0.88){addItem('upgradeStone',1);logItemLoot('upgradeStone');}else{addItem('upgradeStoneHidden',1);logItemLoot('upgradeStoneHidden');}}",
    )

    # computeUpgradeTargetBase - add rare
    s = s.replace(
        "if(eq.rarity==='hidden')return Math.floor(slotDef.baseValue*5+targetLv*1.5);const rm={epic:2.2,legendary:3.5};return Math.floor(slotDef.baseValue*(rm[eq.rarity]||2.2)+targetLv*0.5);",
        "if(eq.rarity==='hidden')return Math.floor(slotDef.baseValue*5+targetLv*1.5);if(eq.rarity==='rare')return Math.floor(slotDef.baseValue*UPGRADE_TARGET_RM.rare+Math.min(280,targetLv)*0.38);const rm=UPGRADE_TARGET_RM;return Math.floor(slotDef.baseValue*(rm[eq.rarity]||2.2)+targetLv*0.5);",
    )

    # applyEquipUpgradeStats scale
    s = s.replace(
        "const scale={epic:0.72,legendary:1,hidden:1.12}[eq.rarity]||0;",
        "const scale=UPGRADE_SCALE[eq.rarity]||0;",
    )

    # getItemColor
    s = s.replace(
        "if(itemId==='renameCard')return 'var(--shop-blue)';const item=ITEMS[itemId];",
        "if(itemId==='renameCard')return 'var(--shop-blue)';if(itemId==='upgradeStoneRare')return 'var(--rare)';if(itemId==='upgradeStone')return 'var(--epic)';if(itemId==='upgradeStoneHidden')return 'var(--hidden)';const item=ITEMS[itemId];",
    )

    # getItemName
    s = s.replace(
        "upgradeStone:'upgradeStone',hellTicket:",
        "upgradeStoneRare:'upgradeStoneRare',upgradeStone:'upgradeStone',upgradeStoneHidden:'upgradeStoneHidden',hellTicket:",
    )

    # getItemIcon - distinct icons
    s = s.replace(
        "upgradeStone:'*',hellTicket:",
        "upgradeStoneRare:'*',upgradeStone:'*',upgradeStoneHidden:'*',hellTicket:",
    )

    # getItemDesc
    s = s.replace(
        "const descs={herb_low:'herbLowDesc'",
        "const descs={upgradeStoneRare:'upgradeStoneRareDesc',upgradeStone:'upgradeStoneDesc',upgradeStoneHidden:'upgradeStoneHiddenDesc',herb_low:'herbLowDesc'",
    )

    # getItemTypeClass
    s = s.replace(
        "if(itemId==='renameCard')return 'item-rename';const item=ITEMS[itemId];",
        "if(itemId==='renameCard')return 'item-rename';if(itemId==='upgradeStoneRare')return 'item-stone-rare';if(itemId==='upgradeStone')return 'item-stone-epic';if(itemId==='upgradeStoneHidden')return 'item-stone-hidden';const item=ITEMS[itemId];",
    )

    # showEquipAction upgrade block
    old_upgrade_btn = (
        "if(eq.rarity==='epic'||eq.rarity==='legendary'||eq.rarity==='hidden'){const upgradeBtn=document.createElement('button');upgradeBtn.className='btn-upgrade';upgradeBtn.textContent=t('upgradeBtn');upgradeBtn.addEventListener('click',()=>{const targetLv=(eq.upgradeLv||0)+1;if(targetLv>10){alert('已達強化上限 +10');return;}const cost=targetLv;const successRate=targetLv<=8?100:50;if(getItemQty('upgradeStone')<cost){alert('史詩升級石不足！需要 '+cost+' 顆');return;}if(confirm(`強化 +${targetLv}\\n需求: ${cost} 史詩升級石\\n成功率: ${successRate}%`)){removeItem('upgradeStone',cost);const roll=Math.random()*100;if(roll<successRate){eq.upgradeLv=targetLv;upgradeEquipmentStats(eq);logInfo(t('upgradeSuccessMsg',getEquipDisplayName(eq.name),targetLv));}else{logInfo(t('upgradeFailMsg'));}recalcPlayerStats();renderAllPanels();updateStatusBar();throttleSave();equipActionDetail.innerHTML=getEquipDetailHtml(eq);}});equipActionBtns.appendChild(upgradeBtn);}"
    )
    new_upgrade_btn = (
        "if(canEquipUpgrade(eq.rarity)){const upgradeBtn=document.createElement('button');upgradeBtn.className='btn-upgrade';upgradeBtn.textContent=t('upgradeBtn');upgradeBtn.addEventListener('click',()=>{const targetLv=(eq.upgradeLv||0)+1;if(targetLv>UPGRADE_MAX_LV){alert(t('upgradeMaxMsg',UPGRADE_MAX_LV));return;}const stoneId=getUpgradeStoneIdForEquip(eq.rarity);const cost=getUpgradeStoneCost(targetLv,eq.rarity);const successRate=getUpgradeSuccessRate(targetLv,eq.rarity);const stoneName=getItemName(stoneId);if(getItemQty(stoneId)<cost){alert(t('upgradeNeedStone',stoneName,cost));return;}if(confirm(t('upgradeConfirm',targetLv,cost,stoneName,successRate))){removeItem(stoneId,cost);const roll=Math.random()*100;if(roll<successRate){eq.upgradeLv=targetLv;upgradeEquipmentStats(eq);logInfo(t('upgradeSuccessMsg',getEquipDisplayName(eq.name),targetLv));}else{logInfo(t('upgradeFailMsg',stoneName));}recalcPlayerStats();renderAllPanels();updateStatusBar();throttleSave();equipActionDetail.innerHTML=getEquipDetailHtml(eq);}});equipActionBtns.appendChild(upgradeBtn);}"
    )
    if old_upgrade_btn not in s:
        raise SystemExit("showEquipAction upgrade block not found")
    s = s.replace(old_upgrade_btn, new_upgrade_btn)

    INDEX.write_text(s, encoding="utf-8")
    print("Patched", INDEX)


if __name__ == "__main__":
    main()
