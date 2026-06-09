#!/usr/bin/env python3
"""v2.20.0 dungeon enemy rebalance to match v2.19 equipment power."""
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"

OLD_MONSTER_BOSS_TIERS = (
    "const MONSTER_POOL=[{hp:28,atk:7,def:3,spd:4,dodge:3,gold:10,xp:5},{hp:18,atk:11,def:1,spd:9,dodge:14,gold:12,xp:6},{hp:46,atk:4,def:6,spd:3,dodge:1,gold:8,xp:4},{hp:32,atk:8,def:2,spd:7,dodge:9,gold:14,xp:7},{hp:58,atk:13,def:8,spd:2,dodge:0,gold:20,xp:10},{hp:38,atk:9,def:4,spd:5,dodge:5,gold:18,xp:9}];"
    "const BOSS_POOL=[{hp:80,atk:14,def:6,spd:4,dodge:2,gold:50,xp:25},{hp:120,atk:18,def:8,spd:5,dodge:3,gold:80,xp:40},{hp:160,atk:22,def:10,spd:3,dodge:1,gold:120,xp:60}];"
    "const DUNGEON_TIERS={normal:{mult:1,hp:1,atk:1,def:1,dodge:1,resist:0},hard:{mult:1.8,hp:1.75,atk:1.65,def:1.85,dodge:1.25,resist:0.08},hell:{mult:3,hp:3.2,atk:2.65,def:3.55,dodge:1.75,resist:0.22}};"
)

NEW_MONSTER_BOSS_TIERS = (
    "const MONSTER_POOL=[{hp:52,atk:14,def:5,spd:4,dodge:3,gold:10,xp:5},{hp:34,atk:20,def:2,spd:9,dodge:14,gold:12,xp:6},{hp:88,atk:8,def:10,spd:3,dodge:1,gold:8,xp:4},{hp:60,atk:16,def:4,spd:7,dodge:9,gold:14,xp:7},{hp:110,atk:24,def:12,spd:2,dodge:0,gold:20,xp:10},{hp:72,atk:18,def:7,spd:5,dodge:5,gold:18,xp:9}];"
    "const BOSS_POOL=[{hp:200,atk:32,def:10,spd:4,dodge:2,gold:50,xp:25},{hp:300,atk:42,def:14,spd:5,dodge:3,gold:80,xp:40},{hp:400,atk:52,def:18,spd:3,dodge:1,gold:120,xp:60}];"
    "const DUNGEON_TIERS={normal:{mult:1,hp:1,atk:1,def:1,dodge:1,resist:0},hard:{mult:1.8,hp:1.85,atk:1.75,def:1.45,dodge:1.2,resist:0.10},hell:{mult:3,hp:3.4,atk:3.0,def:2.2,dodge:1.5,resist:0.18}};"
)

OLD_LEVEL_MULT = (
    "function getLevelMultiplier(fl){if(fl<=100)return Math.pow(1.02,fl-1);"
    "else if(fl<=400)return Math.pow(1.008,fl-1)*2;else return 5+(fl-400)*0.03;}"
)

NEW_LEVEL_MULT = (
    "function getLevelMultiplier(fl){fl=Math.max(1,fl);if(fl<=100)return Math.pow(1.026,fl-1);"
    "if(fl<=400)return Math.pow(1.011,fl-1)*2.6;"
    "return Math.pow(1.011,399)*2.6+(fl-400)*0.18;}"
    "function getEnemyHpScale(lvMult){return lvMult;}"
    "function getEnemyAtkScale(lvMult){return lvMult*1.35;}"
    "function getEnemyDefScale(lvMult){return Math.pow(lvMult,0.58);}"
)

OLD_SPAWN_MONSTER = (
    "function spawnMonster(isBoss=false){if(!currentDungeon)return null;if(isBoss)return applyDungeonModsToEnemy(spawnBoss(),true);"
    "const lvMult=getLevelMultiplier(currentDungeon.floorLevel),hpM=getTierCombatMult('hp'),atkM=getTierCombatMult('atk'),defM=getTierCombatMult('def'),tierMult=getTierCombatMult('mult');"
    "const pool=MONSTER_POOL;const base=pick(pool);const names=t('enemyNames');const idx=pool.indexOf(base);"
    "const enemy={name:names[idx]||'怪物',char:'#',isBoss:false,maxHp:Math.floor(base.hp*lvMult*hpM),hp:Math.floor(base.hp*lvMult*hpM),"
    "atk:Math.floor(base.atk*lvMult*atkM),def:Math.floor(base.def*lvMult*defM),spd:getScaledEnemySpd(base.spd,false),"
    "dodge:getScaledEnemyDodge(base.dodge,false),resist:getTierCombatMult('resist')||0,gold:Math.floor(base.gold*lvMult*(1+tierMult*0.3)),"
    "xp:calcEnemyXpReward(base.xp,currentDungeon.floorLevel,currentDungeon.tier,false)};return applyDungeonModsToEnemy(enemy,false);}"
)

NEW_SPAWN_MONSTER = (
    "function spawnMonster(isBoss=false){if(!currentDungeon)return null;if(isBoss)return applyDungeonModsToEnemy(spawnBoss(),true);"
    "const fl=Math.max(1,currentDungeon.floorLevel),lvMult=getLevelMultiplier(fl),hpM=getTierCombatMult('hp'),atkM=getTierCombatMult('atk'),"
    "defM=getTierCombatMult('def'),tierMult=getTierCombatMult('mult'),hpS=getEnemyHpScale(lvMult),atkS=getEnemyAtkScale(lvMult),defS=getEnemyDefScale(lvMult);"
    "const pool=MONSTER_POOL;const base=pick(pool);const names=t('enemyNames');const idx=pool.indexOf(base);"
    "const enemy={name:names[idx]||'怪物',char:'#',isBoss:false,maxHp:Math.floor(base.hp*hpS*hpM*1.15),hp:Math.floor(base.hp*hpS*hpM*1.15),"
    "atk:Math.floor(base.atk*atkS*atkM*1.1)+Math.floor(fl*0.28*atkM),def:Math.floor(base.def*defS*defM),"
    "spd:getScaledEnemySpd(base.spd,false),dodge:getScaledEnemyDodge(base.dodge,false),resist:getTierCombatMult('resist')||0,"
    "gold:Math.floor(base.gold*lvMult*(1+tierMult*0.3)),xp:calcEnemyXpReward(base.xp,fl,currentDungeon.tier,false)};"
    "return applyDungeonModsToEnemy(enemy,false);}"
)

OLD_SPAWN_BOSS = (
    "function spawnBoss(){if(!currentDungeon)return null;const lvMult=getLevelMultiplier(currentDungeon.floorLevel),hpM=getTierCombatMult('hp'),"
    "atkM=getTierCombatMult('atk'),defM=getTierCombatMult('def'),tierMult=getTierCombatMult('mult');const pool=BOSS_POOL;const base=pick(pool);"
    "const names=t('bossNames');const idx=Math.floor(Math.random()*names.length);"
    "return{name:names[idx]||'BOSS',char:'M',isBoss:true,maxHp:Math.floor(base.hp*lvMult*hpM*1.1*1.5),hp:Math.floor(base.hp*lvMult*hpM*1.1*1.5),"
    "atk:Math.floor(base.atk*lvMult*atkM*1.1),def:Math.floor(base.def*lvMult*defM*1.15),spd:getScaledEnemySpd(base.spd,true),"
    "dodge:getScaledEnemyDodge(base.dodge||2,true),resist:getTierCombatMult('resist')||0,gold:Math.floor(base.gold*lvMult*(1+tierMult*0.5)*2),"
    "xp:calcEnemyXpReward(base.xp,currentDungeon.floorLevel,currentDungeon.tier,true)};}"
)

NEW_SPAWN_BOSS = (
    "function spawnBoss(){if(!currentDungeon)return null;const fl=Math.max(1,currentDungeon.floorLevel),lvMult=getLevelMultiplier(fl),"
    "hpM=getTierCombatMult('hp'),atkM=getTierCombatMult('atk'),defM=getTierCombatMult('def'),tierMult=getTierCombatMult('mult'),"
    "hpS=getEnemyHpScale(lvMult),atkS=getEnemyAtkScale(lvMult),defS=getEnemyDefScale(lvMult);const pool=BOSS_POOL;const base=pick(pool);"
    "const names=t('bossNames');const idx=Math.floor(Math.random()*names.length);"
    "return{name:names[idx]||'BOSS',char:'M',isBoss:true,maxHp:Math.floor(base.hp*hpS*hpM*2.4),hp:Math.floor(base.hp*hpS*hpM*2.4),"
    "atk:Math.floor(base.atk*atkS*atkM*1.28)+Math.floor(fl*0.38*atkM),def:Math.floor(base.def*defS*defM*1.05),"
    "spd:getScaledEnemySpd(base.spd,true),dodge:getScaledEnemyDodge(base.dodge||2,true),resist:getTierCombatMult('resist')||0,"
    "gold:Math.floor(base.gold*lvMult*(1+tierMult*0.5)*2),xp:calcEnemyXpReward(base.xp,fl,currentDungeon.tier,true)};}"
)

OLD_ELITE = (
    "function maybeMakeElite(enemy){if(!enemy||enemy.isBoss||Math.random()>=ELITE_SPAWN_CHANCE)return enemy;enemy.elite=true;"
    "enemy.name=(currentLang==='zh'?'精英 ':'Elite ')+enemy.name;enemy.maxHp=Math.floor(enemy.maxHp*1.45);enemy.hp=enemy.maxHp;"
    "enemy.atk=Math.floor(enemy.atk*1.25);enemy.gold=Math.floor(enemy.gold*1.55);enemy.xp=Math.floor(enemy.xp*1.45);return enemy;}"
)

NEW_ELITE = (
    "function maybeMakeElite(enemy){if(!enemy||enemy.isBoss||Math.random()>=ELITE_SPAWN_CHANCE)return enemy;enemy.elite=true;"
    "enemy.name=(currentLang==='zh'?'精英 ':'Elite ')+enemy.name;enemy.maxHp=Math.floor(enemy.maxHp*1.55);enemy.hp=enemy.maxHp;"
    "enemy.atk=Math.floor(enemy.atk*1.32);enemy.gold=Math.floor(enemy.gold*1.55);enemy.xp=Math.floor(enemy.xp*1.45);return enemy;}"
)


def replace(s, old, new, label):
    if old not in s:
        raise SystemExit(f"MISSING: {label}")
    return s.replace(old, new, 1)


def main():
    s = INDEX.read_text(encoding="utf-8")

    s = s.replace("GAME_VERSION='2.19.1'", "GAME_VERSION='2.20.0'")
    s = s.replace(
        "GAME_VERSION_HISTORY=[{version:'2.19.1'",
        "GAME_VERSION_HISTORY=[{version:'2.20.0',date:'2026-06-09',summary:{zh:'v2.20.0 地下城怪物全面重平衡：依 v2.19 裝備數值重算 HP／攻擊／防禦與樓層成長。',en:'v2.20.0 dungeon enemy rebalance aligned to v2.19 equipment power.'}},{version:'2.19.1'",
    )
    s = s.replace("SAVE_VERSION=71", "SAVE_VERSION=72")

    s = s.replace(
        'logBalanceV2201:"[平衡 v2.19.1]',
        'logBalanceV2202:"[平衡 v2.20.0] 地下城怪物全面重平衡：依現行裝備數值重算 HP／攻擊／防禦與樓層成長；普通約 2–4 擊、Boss 約 8–15 擊（依難度與裝備）。",logBalanceV2201:"[平衡 v2.19.1]',
    )
    s = s.replace(
        'logBalanceV2201:"[Balance v2.19.1]',
        'logBalanceV2202:"[Balance v2.20.0] Full dungeon enemy rebalance vs current gear: HP/ATK/DEF and floor scaling reworked; ~2–4 hits per mob, ~8–15 on bosses by tier.",logBalanceV2201:"[Balance v2.19.1]',
    )

    s = replace(s, OLD_MONSTER_BOSS_TIERS, NEW_MONSTER_BOSS_TIERS, "monster/boss/tiers")
    s = replace(s, OLD_LEVEL_MULT, NEW_LEVEL_MULT, "level multiplier")
    s = replace(s, OLD_SPAWN_MONSTER, NEW_SPAWN_MONSTER, "spawnMonster")
    s = replace(s, OLD_SPAWN_BOSS, NEW_SPAWN_BOSS, "spawnBoss")
    s = replace(s, OLD_ELITE, NEW_ELITE, "maybeMakeElite")

    s = s.replace(
        "function migrateSave(data){if(data.version<71){",
        "function migrateSave(data){if(data.version<72){data._balanceV2202Notice=true;data.version=72;}"
        "if(data.version<71){",
    )
    s = s.replace(
        "const _balanceV2201Notice=!!data._balanceV2201Notice;delete data._balanceV2201Notice;",
        "const _balanceV2202Notice=!!data._balanceV2202Notice;delete data._balanceV2202Notice;"
        "const _balanceV2201Notice=!!data._balanceV2201Notice;delete data._balanceV2201Notice;",
    )
    s = s.replace(
        "if(_balanceV2201Notice)logInfo(t('logBalanceV2201'));",
        "if(_balanceV2202Notice)logInfo(t('logBalanceV2202'));"
        "if(_balanceV2201Notice)logInfo(t('logBalanceV2201'));",
    )

    INDEX.write_text(s, encoding="utf-8")
    print("Patched", INDEX)


if __name__ == "__main__":
    main()
