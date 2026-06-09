#!/usr/bin/env python3
"""v2.19.1 — migrate existing player equipment to v2.19.0 balance values."""
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"

OLD_INFER = (
    "function inferEquipOrigBase(eq){const slotDef=EQUIP_SLOTS.find(s=>s.slot===eq.type);"
    "if(!slotDef)return eq.baseValue;if(eq.rarity==='hidden')return Math.floor(slotDef.baseValue*5+(eq.level||1)*1.5);"
    "const rm={common:1,rare:1.5,epic:2.2,legendary:3.5};"
    "return Math.floor(slotDef.baseValue*(rm[eq.rarity]||1)+(eq.level||1)*0.5);}"
)

NEW_INFER = (
    "function inferEquipOrigBase(eq){const slotDef=EQUIP_SLOTS.find(s=>s.slot===eq.type);"
    "if(!slotDef)return eq.baseValue;const mlv=eq.level||1,rm=RARITY_BASE_RM[eq.rarity]||1;"
    "if(eq.rarity==='hidden')return Math.floor(slotDef.baseValue*RARITY_BASE_RM.hidden+mlv*0.55);"
    "return Math.floor(slotDef.baseValue*rm+mlv*0.32);}"
)

OLD_MIGRATE_UPGRADE = (
    "function migrateEquipUpgrade(eq){if(!eq)return;const maxLv=getUpgradeMaxLv(eq.rarity);"
    "if((eq.upgradeLv||0)>maxLv)eq.upgradeLv=maxLv;if(!eq.upgradeLv)return;"
    "captureEquipOrigStats(eq);applyEquipUpgradeStats(eq);}"
)

NEW_MIGRATE_UPGRADE = (
    "const LEGACY_AFFIX_PEAK={atk:[1,16],maxHp:[5,60],def:[2,10],shield:[5,50],dodge:[2,18],"
    "spd:[2,8],critChance:[8,28],critDmg:[10,35],lifesteal:[2,8],thorns:[2,10],goldBonus:[5,50],"
    "allDmg:[18,30],allDmgReduction:[18,30]};"
    "function rebalanceExistingEquipment(eq){if(!eq||!eq.type||!eq.rarity)return;"
    "captureEquipOrigStats(eq);const slotDef=EQUIP_SLOTS.find(s=>s.slot===eq.type);if(!slotDef)return;"
    "const mlv=eq.level||1,rm=RARITY_BASE_RM[eq.rarity]||1;"
    "eq.origBase=eq.rarity==='hidden'?Math.floor(slotDef.baseValue*RARITY_BASE_RM.hidden+mlv*0.55):"
    "Math.floor(slotDef.baseValue*rm+mlv*0.32);"
    "const pool=eq.rarity==='hidden'?HIDDEN_AFFIXES:(WEAPON_SLOTS.includes(eq.type)?WEAPON_AFFIXES:ARMOR_AFFIXES),"
    "affixRm=RARITY_AFFIX_ROLL_RM[eq.rarity]||1,allPools=[...WEAPON_AFFIXES,...ARMOR_AFFIXES,...HIDDEN_AFFIXES];"
    "eq.origAffixes=(eq.origAffixes||eq.affixes||[]).map(oa=>{"
    "const def=pool.find(a=>a.stat===oa.stat)||allPools.find(a=>a.stat===oa.stat);"
    "const oldVal=parseFloat(oa.value)||0;let newVal;"
    "if(oa.stat==='avoidDeath')newVal=1;else if(def){"
    "const leg=LEGACY_AFFIX_PEAK[oa.stat];"
    "const ratio=leg?Math.max(0,Math.min(1,(oldVal-leg[0])/(leg[1]-leg[0]||1))):0.5;"
    "if(def.lvMinMax){const lo=mlv*def.lvMinMax[0]*affixRm,hi=mlv*def.lvMinMax[1]*affixRm;"
    "newVal=Math.max(1,Math.floor(lo+ratio*(hi-lo)));}"
    "else if(AFFIX_PCT_STATS.includes(oa.stat))"
    "newVal=parseFloat((def.min*affixRm+ratio*(def.max*affixRm-def.min*affixRm)).toFixed(1));"
    "else newVal=Math.max(1,Math.floor(def.min*affixRm+ratio*(def.max*affixRm-def.min*affixRm)));"
    "}else newVal=oldVal;return{stat:oa.stat,value:newVal};});"
    "eq.affixes.forEach(a=>{const def=pool.find(d=>d.stat===a.stat)||allPools.find(d=>d.stat===a.stat);if(def)a.name=def.name;});"
    "const maxLv=getUpgradeMaxLv(eq.rarity);if((eq.upgradeLv||0)>maxLv)eq.upgradeLv=maxLv;applyEquipUpgradeStats(eq);}"
    "function migrateEquipUpgrade(eq){if(!eq)return;const maxLv=getUpgradeMaxLv(eq.rarity);"
    "if((eq.upgradeLv||0)>maxLv)eq.upgradeLv=maxLv;if(!eq.upgradeLv)return;"
    "captureEquipOrigStats(eq);applyEquipUpgradeStats(eq);}"
)


def replace(s, old, new, label):
    if old not in s:
        raise SystemExit(f"MISSING: {label}")
    return s.replace(old, new, 1)


def main():
    s = INDEX.read_text(encoding="utf-8")

    s = s.replace("GAME_VERSION='2.19.0'", "GAME_VERSION='2.19.1'")
    s = s.replace(
        "GAME_VERSION_HISTORY=[{version:'2.19.0'",
        "GAME_VERSION_HISTORY=[{version:'2.19.1',date:'2026-06-09',summary:{zh:'v2.19.1 已獲取裝備依 v2.19.0 新數值重算（保留詞條品質）。',en:'v2.19.1 rebalance existing gear to v2.19.0 values.'}},{version:'2.19.0'",
    )
    s = s.replace("SAVE_VERSION=70", "SAVE_VERSION=71")

    s = s.replace(
        'logBalanceV2200:"[平衡 v2.19.0]',
        'logBalanceV2201:"[平衡 v2.19.1] 已依 v2.19.0 新數值重算你背包與已裝備的全部裝備（保留詞條品質比例）。",logBalanceV2200:"[平衡 v2.19.0]',
    )
    s = s.replace(
        'logBalanceV2200:"[Balance v2.19.0]',
        'logBalanceV2201:"[Balance v2.19.1] Rebalanced all equipped and inventory gear to v2.19.0 values (affix roll quality preserved).",logBalanceV2200:"[Balance v2.19.0]',
    )

    s = replace(s, OLD_INFER, NEW_INFER, "inferEquipOrigBase")
    s = replace(s, OLD_MIGRATE_UPGRADE, NEW_MIGRATE_UPGRADE, "migrateEquipUpgrade block")

    s = s.replace(
        "function migrateSave(data){if(data.version<70){",
        "function migrateSave(data){if(data.version<71){const rebalanceEq=eq=>{if(eq)rebalanceExistingEquipment(eq);};"
        "if(data.player){for(let slot in data.player.equipment||{})rebalanceEq(data.player.equipment[slot]);"
        "(data.player.equipInventory||[]).forEach(rebalanceEq);}"
        "data._balanceV2201Notice=true;data.version=71;}"
        "if(data.version<70){",
    )

    s = s.replace(
        "const _balanceV2194Notice=!!data._balanceV2194Notice;delete data._balanceV2194Notice;",
        "const _balanceV2201Notice=!!data._balanceV2201Notice;delete data._balanceV2201Notice;"
        "const _balanceV2194Notice=!!data._balanceV2194Notice;delete data._balanceV2194Notice;",
    )

    s = s.replace(
        "if(_balanceV2194Notice)logInfo(t('logBalanceV2194'));",
        "if(_balanceV2201Notice)logInfo(t('logBalanceV2201'));"
        "if(_balanceV2194Notice)logInfo(t('logBalanceV2194'));",
    )

    INDEX.write_text(s, encoding="utf-8")
    print("Patched", INDEX)


if __name__ == "__main__":
    main()
