#!/usr/bin/env python3
"""v2.19.0 equipment affix & upgrade balance pass."""
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"

OLD_WEAPON_ARMOR = (
    "const WEAPON_AFFIXES=[{name:'CRIT%',stat:'critChance',min:18,max:23},{name:'CRIT_DMG',stat:'critDmg',min:20,max:30},{name:'GOLD+',stat:'goldBonus',min:5,max:30},{name:'CRIT%',stat:'critChance',min:22,max:28},{name:'CRIT_DMG',stat:'critDmg',min:25,max:35},{name:'GOLD+',stat:'goldBonus',min:20,max:50}];"
    "const ARMOR_AFFIXES=[{name:'ATK',stat:'atk',min:1,max:6},{name:'HP',stat:'maxHp',min:5,max:30},{name:'DEF',stat:'def',min:2,max:10},{name:'SHIELD',stat:'shield',min:5,max:25},{name:'DODGE',stat:'dodge',min:2,max:5},{name:'SPD',stat:'spd',min:2,max:8},{name:'CRIT%',stat:'critChance',min:8,max:15},{name:'CRIT_DMG',stat:'critDmg',min:10,max:25},{name:'LS',stat:'lifesteal',min:2,max:8},{name:'THRNS',stat:'thorns',min:2,max:10},{name:'ATK',stat:'atk',min:6,max:16},{name:'HP',stat:'maxHp',min:30,max:60},{name:'SHIELD',stat:'shield',min:20,max:50},{name:'DODGE',stat:'dodge',min:8,max:18}];"
    "const HIDDEN_AFFIXES=[{name:'ALL_DMG+',stat:'allDmg',min:18,max:30},{name:'ALL_DMG_REDUCTION',stat:'allDmgReduction',min:18,max:30},{name:'AVOID_DEATH',stat:'avoidDeath',min:1,max:1}];"
)

NEW_WEAPON_ARMOR = (
    "const WEAPON_AFFIXES=[{name:'CRIT%',stat:'critChance',min:10,max:12},{name:'CRIT_DMG',stat:'critDmg',min:22,max:28},{name:'GOLD+',stat:'goldBonus',min:10,max:16}];"
    "const ARMOR_AFFIXES=[{name:'ATK',stat:'atk',min:3,max:7},{name:'HP',stat:'maxHp',min:12,max:28},{name:'DEF',stat:'def',lvMinMax:[0.06,0.11]},{name:'SHIELD',stat:'shield',lvMinMax:[0.7,1.2]},{name:'DODGE',stat:'dodge',min:4,max:8},{name:'SPD',stat:'spd',min:2,max:5},{name:'CRIT%',stat:'critChance',min:6,max:10},{name:'CRIT_DMG',stat:'critDmg',min:12,max:18},{name:'LS',stat:'lifesteal',min:4,max:8},{name:'THRNS',stat:'thorns',lvMinMax:[0.04,0.08]}];"
    "const HIDDEN_AFFIXES=[{name:'ALL_DMG+',stat:'allDmg',min:12,max:18},{name:'ALL_DMG_REDUCTION',stat:'allDmgReduction',min:10,max:15},{name:'AVOID_DEATH',stat:'avoidDeath',min:1,max:1}];"
    "const AFFIX_PCT_STATS=['lifesteal','critChance','critDmg','dodge','goldBonus','allDmg','allDmgReduction'];"
    "const AFFIX_LEGENDARY_CAP={critChance:50,critDmg:55,dodge:25,lifesteal:25,goldBonus:75,allDmg:40,allDmgReduction:22};"
    "const RARITY_AFFIX_CAP_MULT={common:0.22,rare:0.42,epic:0.62,legendary:1,hidden:1.05};"
    "const RARITY_BASE_RM={common:1,rare:1.35,epic:1.75,legendary:2.35,hidden:4};"
    "const RARITY_AFFIX_ROLL_RM={common:0.85,rare:0.92,epic:0.97,legendary:1,hidden:1.05};"
    "const BASE_UPGRADE_TARGET_MULT={common:1.18,rare:1.35,epic:1.55,legendary:1.85,hidden:2.05};"
    "function rollEquipAffixValue(affix,mlv,rarity){const rm=RARITY_AFFIX_ROLL_RM[rarity]||1;if(affix.lvMinMax){const v=mlv*randFloat(affix.lvMinMax[0],affix.lvMinMax[1])*rm;return Math.max(1,Math.floor(v));}"
    "if(AFFIX_PCT_STATS.includes(affix.stat))return parseFloat(randFloat(affix.min*rm,affix.max*rm).toFixed(1));return Math.max(1,Math.floor(rand(affix.min,affix.max)*rm));}"
    "function getAffixCapAtMaxUpgrade(stat,rarity){const cap=AFFIX_LEGENDARY_CAP[stat];if(cap==null)return null;return cap*(RARITY_AFFIX_CAP_MULT[rarity]||1);}"
)

OLD_UPGRADE_BLOCK = (
    "const UPGRADE_MAX_LV=10;const UPGRADE_STONE_BY_RARITY={rare:'upgradeStoneRare',epic:'upgradeStone',legendary:'upgradeStoneLegendary',hidden:'upgradeStoneHidden'};"
    "const UPGRADE_SCALE={rare:0.48,epic:0.72,legendary:1,hidden:1.12};const UPGRADE_TARGET_RM={rare:1.45,epic:2.2,legendary:3.5};"
    "function getUpgradeStoneIdForEquip(rarity){return UPGRADE_STONE_BY_RARITY[rarity]||null;}"
    "function canEquipUpgrade(rarity){return !!getUpgradeStoneIdForEquip(rarity);}"
    "function getUpgradeStoneCost(targetLv,rarity){const mult={rare:1,epic:1,legendary:1.1,hidden:1.25};return Math.max(1,Math.ceil(targetLv*(mult[rarity]||1)));}"
    "function getUpgradeSuccessRate(targetLv,rarity){if(targetLv<=6)return 100;if(targetLv<=8)return rarity==='rare'?85:(rarity==='hidden'?80:100);if(targetLv===9)return rarity==='hidden'?45:(rarity==='rare'?70:50);return rarity==='hidden'?35:(rarity==='rare'?55:50);}"
)

NEW_UPGRADE_BLOCK = (
    "const UPGRADE_MAX_BY_RARITY={common:2,rare:4,epic:6,legendary:10,hidden:10};"
    "const UPGRADE_STONE_BY_RARITY={common:'equipFragment',rare:'upgradeStoneRare',epic:'upgradeStone',legendary:'upgradeStoneLegendary',hidden:'upgradeStoneHidden'};"
    "function getUpgradeMaxLv(rarity){return UPGRADE_MAX_BY_RARITY[rarity]||0;}"
    "function getUpgradeStoneIdForEquip(rarity){return UPGRADE_STONE_BY_RARITY[rarity]||null;}"
    "function canEquipUpgrade(rarity){return getUpgradeMaxLv(rarity)>0&&!!getUpgradeStoneIdForEquip(rarity);}"
    "function getUpgradeStoneCost(targetLv,rarity){if(rarity==='common')return Math.max(3,Math.ceil(targetLv*4));const mult={rare:1,epic:1,legendary:1.1,hidden:1.25};return Math.max(1,Math.ceil(targetLv*(mult[rarity]||1)));}"
    "function getUpgradeSuccessRate(targetLv,rarity){const maxLv=getUpgradeMaxLv(rarity)||1;const ratio=targetLv/maxLv;if(ratio<=0.6)return 100;if(ratio<=0.8)return rarity==='rare'?88:(rarity==='hidden'?82:100);if(ratio<=0.9)return rarity==='hidden'?48:(rarity==='rare'?72:55);return rarity==='hidden'?38:(rarity==='rare'?58:52);}"
)

OLD_GEN_NORMAL = (
    "function generateNormalEquipment(slotDef,mlv,rarity){const name=pick(EQUIP_NAME_POOL[slotDef.slot]);const rm={common:1,rare:1.5,epic:2.2,legendary:3.5};const baseVal=Math.floor(slotDef.baseValue*rm[rarity]+mlv*0.5);const count=RARITY_AFFIX_COUNT[rarity]||1;const pool=WEAPON_SLOTS.includes(slotDef.slot)?WEAPON_AFFIXES:ARMOR_AFFIXES;const shuffled=[...pool].sort(()=>Math.random()-0.5);const affixes=[],used=new Set();for(let a of shuffled){if(affixes.length>=count)break;if(used.has(a.stat))continue;const val=['lifesteal','critChance','critDmg','dodge','goldBonus'].includes(a.stat)?randFloat(a.min,a.max):rand(a.min,a.max);affixes.push({name:a.name,stat:a.stat,value:val});used.add(a.stat);}if(rarity==='common'&&Math.random()<0.3)affixes.length=0;const eq={id:'eq_'+Date.now()+'_'+Math.random().toString(36).slice(2,6),name,type:slotDef.slot,rarity,baseStat:slotDef.baseStat,baseValue:baseVal,affixes,level:mlv,upgradeLv:0,origBase:baseVal,origAffixes:affixes.map(a=>({stat:a.stat,value:a.stat==='avoidDeath'?1:parseFloat(a.value)}))};return eq;}"
)

NEW_GEN_NORMAL = (
    "function generateNormalEquipment(slotDef,mlv,rarity){const name=pick(EQUIP_NAME_POOL[slotDef.slot]);const rm=RARITY_BASE_RM[rarity]||1;const baseVal=Math.floor(slotDef.baseValue*rm+mlv*0.32);const count=RARITY_AFFIX_COUNT[rarity]||1;const pool=WEAPON_SLOTS.includes(slotDef.slot)?WEAPON_AFFIXES:ARMOR_AFFIXES;const shuffled=[...pool].sort(()=>Math.random()-0.5);const affixes=[],used=new Set();for(let a of shuffled){if(affixes.length>=count)break;if(used.has(a.stat))continue;const val=rollEquipAffixValue(a,mlv,rarity);affixes.push({name:a.name,stat:a.stat,value:val});used.add(a.stat);}if(rarity==='common'&&Math.random()<0.3)affixes.length=0;const eq={id:'eq_'+Date.now()+'_'+Math.random().toString(36).slice(2,6),name,type:slotDef.slot,rarity,baseStat:slotDef.baseStat,baseValue:baseVal,affixes,level:mlv,upgradeLv:0,origBase:baseVal,origAffixes:affixes.map(a=>({stat:a.stat,value:a.stat==='avoidDeath'?1:parseFloat(a.value)}))};return eq;}"
)

OLD_GEN_HIDDEN = (
    "function generateHiddenEquipment(slotDef,mlv){const name=pick(HIDDEN_EQUIP_NAMES);const baseVal=Math.floor(slotDef.baseValue*5+mlv*1.5);const affixes=[],used=new Set();const affixCount=RARITY_AFFIX_COUNT.hidden;const shuffled=[...HIDDEN_AFFIXES].sort(()=>Math.random()-0.5);for(let a of shuffled){if(affixes.length>=affixCount)break;if(used.has(a.stat))continue;const val=a.stat==='avoidDeath'?1:randFloat(a.min,a.max);affixes.push({name:a.name,stat:a.stat,value:val});used.add(a.stat);}return{id:'eq_'+Date.now()+'_'+Math.random().toString(36).slice(2,6),name,type:slotDef.slot,rarity:'hidden',baseStat:slotDef.baseStat,baseValue:baseVal,affixes,level:mlv,upgradeLv:0,origBase:baseVal,origAffixes:affixes.map(a=>({stat:a.stat,value:a.stat==='avoidDeath'?1:parseFloat(a.value)}))};}"
)

NEW_GEN_HIDDEN = (
    "function generateHiddenEquipment(slotDef,mlv){const name=pick(HIDDEN_EQUIP_NAMES);const baseVal=Math.floor(slotDef.baseValue*RARITY_BASE_RM.hidden+mlv*0.55);const affixes=[],used=new Set();const affixCount=RARITY_AFFIX_COUNT.hidden;const shuffled=[...HIDDEN_AFFIXES].sort(()=>Math.random()-0.5);for(let a of shuffled){if(affixes.length>=affixCount)break;if(used.has(a.stat))continue;const val=a.stat==='avoidDeath'?1:rollEquipAffixValue(a,mlv,'hidden');affixes.push({name:a.name,stat:a.stat,value:val});used.add(a.stat);}return{id:'eq_'+Date.now()+'_'+Math.random().toString(36).slice(2,6),name,type:slotDef.slot,rarity:'hidden',baseStat:slotDef.baseStat,baseValue:baseVal,affixes,level:mlv,upgradeLv:0,origBase:baseVal,origAffixes:affixes.map(a=>({stat:a.stat,value:a.stat==='avoidDeath'?1:parseFloat(a.value)}))};}"
)

OLD_UPGRADE_STATS = (
    "function computeUpgradeTargetBase(eq){const slotDef=EQUIP_SLOTS.find(s=>s.slot===eq.type);if(!slotDef)return eq.origBase||eq.baseValue;const itemLv=eq.level||1;const targetLv=eq.rarity==='hidden'?Math.min(280,itemLv+80):Math.min(300,Math.max(itemLv+60,itemLv<=120?300:itemLv+120));if(eq.rarity==='hidden')return Math.floor(slotDef.baseValue*5+targetLv*1.5);if(eq.rarity==='rare')return Math.floor(slotDef.baseValue*UPGRADE_TARGET_RM.rare+Math.min(280,targetLv)*0.38);const rm=UPGRADE_TARGET_RM;return Math.floor(slotDef.baseValue*(rm[eq.rarity]||2.2)+targetLv*0.5);}"
    "function applyEquipUpgradeStats(eq){captureEquipOrigStats(eq);const upLv=eq.upgradeLv||0;const scale=UPGRADE_SCALE[eq.rarity]||0;if(!scale||upLv<=0){eq.baseValue=eq.origBase;eq.affixes.forEach((a,i)=>{if(eq.origAffixes[i])a.value=eq.origAffixes[i].value;});return;}const progress=upLv/10;const target=computeUpgradeTargetBase(eq);const bonus=(target-eq.origBase)*scale*progress;eq.baseValue=Math.floor(eq.origBase+bonus);const statMult=eq.origBase>0?1+(eq.baseValue/eq.origBase-1)*0.85:1;const pctStats=['lifesteal','critChance','critDmg','dodge','goldBonus','allDmg','allDmgReduction'];eq.affixes.forEach((a,i)=>{const orig=eq.origAffixes[i]?eq.origAffixes[i].value:0;a.value=pctStats.includes(a.stat)?parseFloat((orig*statMult).toFixed(1)):Math.floor(orig*statMult);});}"
    "function upgradeEquipmentStats(eq){applyEquipUpgradeStats(eq);}"
    "function migrateEquipUpgrade(eq){if(!eq||!eq.upgradeLv)return;captureEquipOrigStats(eq);applyEquipUpgradeStats(eq);}"
)

NEW_UPGRADE_STATS = (
    "function computeUpgradeTargetBase(eq){const mult=BASE_UPGRADE_TARGET_MULT[eq.rarity]||1.35;return Math.floor((eq.origBase||eq.baseValue||1)*mult);}"
    "function applyEquipUpgradeStats(eq){captureEquipOrigStats(eq);const maxLv=getUpgradeMaxLv(eq.rarity);const upLv=Math.min(eq.upgradeLv||0,maxLv);if(upLv<=0||!maxLv){eq.baseValue=eq.origBase;eq.affixes.forEach((a,i)=>{if(eq.origAffixes[i])a.value=eq.origAffixes[i].value;});return;}const progress=upLv/maxLv;const targetBase=computeUpgradeTargetBase(eq);eq.baseValue=Math.floor(eq.origBase+(targetBase-eq.origBase)*progress);const flatMult=1+(progress*0.85);eq.affixes.forEach((a,i)=>{const orig=eq.origAffixes[i]?eq.origAffixes[i].value:0;const cap=getAffixCapAtMaxUpgrade(a.stat,eq.rarity);if(cap!=null&&AFFIX_PCT_STATS.includes(a.stat)){a.value=parseFloat((orig+(cap-orig)*progress).toFixed(1));}else{a.value=Math.max(orig,Math.floor(orig*flatMult));}});}"
    "function upgradeEquipmentStats(eq){applyEquipUpgradeStats(eq);}"
    "function migrateEquipUpgrade(eq){if(!eq)return;const maxLv=getUpgradeMaxLv(eq.rarity);if((eq.upgradeLv||0)>maxLv)eq.upgradeLv=maxLv;if(!eq.upgradeLv)return;captureEquipOrigStats(eq);applyEquipUpgradeStats(eq);}"
)

OLD_AFFIX_BOUNDS = (
    "function getAffixBounds(stat,isHidden){const pools=[WEAPON_AFFIXES,ARMOR_AFFIXES];if(isHidden)pools.push(HIDDEN_AFFIXES);let lo=0,hi=99999,found=false;for(const pool of pools)for(const a of pool)if(a.stat===stat){lo=Math.min(lo,a.min);hi=Math.max(hi,a.max);found=true;}if(stat==='avoidDeath')return{min:0,max:1};return found?{min:lo,max:hi}:{min:0,max:99999};}"
    "function validateEquipmentItem(eq){if(!eq||!eq.id||!eq.type||!eq.rarity)return false;if(!['common','rare','epic','legendary','hidden'].includes(eq.rarity))return false;if(eq.level<1||eq.level>2000)return false;if(eq.upgradeLv!=null&&(eq.upgradeLv<0||eq.upgradeLv>50))return false;if(!Array.isArray(eq.affixes))return false;const maxAff=(RARITY_AFFIX_COUNT[eq.rarity]||3)+2;if(eq.affixes.length>maxAff)return false;for(const a of eq.affixes){if(!a||!a.stat)return false;const b=getAffixBounds(a.stat,eq.rarity==='hidden');const v=Number(a.value);const tol=eq.rarity==='hidden'?b.max*0.35:Math.max(5,b.max*0.25);if(!Number.isFinite(v)||v<b.min-tol||v>b.max+tol+(eq.upgradeLv||0)*5)return false;}return true;}"
)

NEW_AFFIX_BOUNDS = (
    "function getAffixBounds(stat,isHidden){const pools=[WEAPON_AFFIXES,ARMOR_AFFIXES];if(isHidden)pools.push(HIDDEN_AFFIXES);let lo=99999,hi=0,found=false;for(const pool of pools)for(const a of pool)if(a.stat===stat){if(a.lvMinMax){lo=Math.min(lo,a.lvMinMax[0]);hi=Math.max(hi,a.lvMinMax[1]);}else{lo=Math.min(lo,a.min);hi=Math.max(hi,a.max);}found=true;}if(stat==='avoidDeath')return{min:0,max:1};const cap=getAffixCapAtMaxUpgrade(stat,isHidden?'hidden':'legendary');if(cap!=null)return{min:0,max:cap*1.08};return found?{min:Math.max(0,lo*0.7),max:Math.max(hi,hi*1.2)}:{min:0,max:99999};}"
    "function validateEquipmentItem(eq){if(!eq||!eq.id||!eq.type||!eq.rarity)return false;if(!['common','rare','epic','legendary','hidden'].includes(eq.rarity))return false;if(eq.level<1||eq.level>2000)return false;const maxUp=getUpgradeMaxLv(eq.rarity);if(eq.upgradeLv!=null&&(eq.upgradeLv<0||eq.upgradeLv>maxUp+2))return false;if(!Array.isArray(eq.affixes))return false;const maxAff=(RARITY_AFFIX_COUNT[eq.rarity]||3)+2;if(eq.affixes.length>maxAff)return false;for(const a of eq.affixes){if(!a||!a.stat)return false;const b=getAffixBounds(a.stat,eq.rarity==='hidden');const cap=getAffixCapAtMaxUpgrade(a.stat,eq.rarity);const hi=cap!=null?cap*1.1:b.max;const v=Number(a.value);const tol=Math.max(3,hi*0.12);if(!Number.isFinite(v)||v<-tol||v>hi+tol)return false;}return true;}"
)


def replace(s, old, new, label):
    if old not in s:
        raise SystemExit(f"MISSING: {label}")
    return s.replace(old, new, 1)


def main():
    s = INDEX.read_text(encoding="utf-8")

    s = s.replace("GAME_VERSION='2.18.40'", "GAME_VERSION='2.19.0'")
    s = s.replace(
        "GAME_VERSION_HISTORY=[{version:'2.18.40'",
        "GAME_VERSION_HISTORY=[{version:'2.19.0',date:'2026-06-09',summary:{zh:'v2.19.0 裝備詞條與強化平衡：各稀有度強化上限、詞條基礎值與成長重算，流派取舍。',en:'v2.19.0 equipment affix & upgrade rebalance; build tradeoffs.'}},{version:'2.18.40'",
    )
    s = s.replace(
        'logBalanceV2199:"[調整 v2.18.40]',
        'logBalanceV2200:"[平衡 v2.19.0] 重算裝備基礎值與詞條數值；普通+2／稀有+4／史詩+6／傳說與隱藏+10；全套傳說+10可逼近單項上限但無法全滿。",logBalanceV2199:"[調整 v2.18.40]',
    )

    s = replace(s, OLD_WEAPON_ARMOR, NEW_WEAPON_ARMOR, "weapon/armor affixes")
    s = replace(s, OLD_UPGRADE_BLOCK, NEW_UPGRADE_BLOCK, "upgrade block")
    s = replace(s, OLD_GEN_NORMAL, NEW_GEN_NORMAL, "generateNormalEquipment")
    s = replace(s, OLD_GEN_HIDDEN, NEW_GEN_HIDDEN, "generateHiddenEquipment")
    s = replace(s, OLD_UPGRADE_STATS, NEW_UPGRADE_STATS, "upgrade stats")
    s = replace(s, OLD_AFFIX_BOUNDS, NEW_AFFIX_BOUNDS, "affix bounds")

    s = s.replace(
        "if(targetLv>UPGRADE_MAX_LV){alert(t('upgradeMaxMsg',UPGRADE_MAX_LV));return;}",
        "const _upMaxLv=getUpgradeMaxLv(eq.rarity);if(targetLv>_upMaxLv){alert(t('upgradeMaxMsg',_upMaxLv));return;}",
    )

    INDEX.write_text(s, encoding="utf-8")
    print("Patched", INDEX)


if __name__ == "__main__":
    main()
