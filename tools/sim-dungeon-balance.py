#!/usr/bin/env python3
"""Simulate player vs enemy combat for dungeon rebalance tuning."""
import math

RARITY_BASE_RM = dict(common=1, rare=1.35, epic=1.75, legendary=2.35, hidden=4)
UPGRADE_MULT = dict(common=1.18, rare=1.35, epic=1.55, legendary=1.85, hidden=2.05)
UPGRADE_MAX = dict(common=2, rare=4, epic=6, legendary=10, hidden=10)
SLOTS = dict(mainhand=8, offhand=5, armor=6, armguard=3, legguard=12, boots=3)

MONSTER_OLD = [dict(hp=28, atk=7, defense=3)]
MONSTER_NEW = [dict(hp=52, atk=14, defense=5)]
BOSS_OLD = [dict(hp=80, atk=14, defense=6)]
BOSS_NEW = [dict(hp=200, atk=32, defense=10)]

TIERS_OLD = dict(normal=dict(hp=1, atk=1, defense=1), hard=dict(hp=1.75, atk=1.65, defense=1.85), hell=dict(hp=3.2, atk=2.65, defense=3.55))
TIERS_NEW = dict(normal=dict(hp=1, atk=1, defense=1), hard=dict(hp=1.85, atk=1.75, defense=1.45), hell=dict(hp=3.4, atk=3.0, defense=2.2))


def lv_mult_old(fl):
    if fl <= 100: return 1.02 ** (fl - 1)
    if fl <= 400: return (1.008 ** (fl - 1)) * 2
    return 5 + (fl - 400) * 0.03


def lv_mult_new(fl):
    if fl <= 100: return 1.026 ** (fl - 1)
    if fl <= 400: return (1.011 ** (fl - 1)) * 2.6
    return 7 + (fl - 400) * 0.04


def hp_scale(lv): return lv
def atk_scale(lv): return lv * 1.35
def def_scale(lv): return lv ** 0.58


def slot_val(slot, lv, rarity, upgraded=True):
    base = SLOTS[slot]
    rm = RARITY_BASE_RM[rarity]
    orig = math.floor(base * rm + lv * 0.32)
    return math.floor(orig * UPGRADE_MULT[rarity]) if upgraded else orig


def player_stats(lv, rarity='legendary', upgraded=True, affix_atk=0, affix_def=0, affix_hp=0):
    eq = {s: slot_val(s, lv, rarity, upgraded) for s in SLOTS}
    return dict(
        atk=10 + lv * 3 + eq['mainhand'] + eq['offhand'] + affix_atk,
        defense=3 + math.floor(lv * 1.2) + eq['armor'] + eq['armguard'] + affix_def,
        hp=100 + lv * 20 + eq['legguard'] + affix_hp,
    )


def mob_stats(base, fl, tier, is_boss, use_new=True):
    lm = lv_mult_new(fl) if use_new else lv_mult_old(fl)
    t = TIERS_NEW[tier] if use_new else TIERS_OLD[tier]
    hs, as_, ds = hp_scale(lm), atk_scale(lm), def_scale(lm)
    if is_boss:
        hp = math.floor(base['hp'] * hs * t['hp'] * (2.4 if use_new else 1.65))
        atk = math.floor(base['atk'] * as_ * t['atk'] * (1.28 if use_new else 1.1))
        if use_new:
            atk += math.floor(fl * 0.38 * t['atk'])
        defense = math.floor(base['defense'] * ds * t['defense'] * (1.05 if use_new else 1.15))
    else:
        hp = math.floor(base['hp'] * hs * t['hp'] * (1.15 if use_new else 1.0))
        atk = math.floor(base['atk'] * as_ * t['atk'] * (1.1 if use_new else 1.0))
        if use_new:
            atk += math.floor(fl * 0.28 * t['atk'])
        defense = math.floor(base['defense'] * ds * t['defense'])
    return dict(hp=hp, atk=atk, defense=defense)


def report(name, fl, tier, rarity, upgraded, use_new, affix_atk=0, affix_def=0, affix_hp=0):
    p = player_stats(fl, rarity, upgraded, affix_atk, affix_def, affix_hp)
    mob_b = MONSTER_NEW if use_new else MONSTER_OLD
    boss_b = BOSS_NEW if use_new else BOSS_OLD
    mob = mob_stats(mob_b[0], fl, tier, False, use_new)
    boss = mob_stats(boss_b[0], fl, tier, True, use_new)
    md = max(1, p['atk'] - mob['defense'])
    bd = max(1, p['atk'] - boss['defense'])
    mh = math.ceil(mob['hp'] / (md * 0.95))
    bh = math.ceil(boss['hp'] / (bd * 0.95))
    mt = max(1, mob['atk'] - p['defense'])
    bt = max(1, boss['atk'] - p['defense'])
    print(
        f"{name:12s} fl={fl:3d} {tier:6s} {rarity:9s} | "
        f"mob {mh:2d}hits/{mt:4d}({mt/p['hp']*100:4.1f}%) "
        f"boss {bh:2d}hits/{bt:4d}({bt/p['hp']*100:4.1f}%) | "
        f"P {p['atk']}/{p['defense']}/{p['hp']}"
    )


print("OLD")
for fl in [10, 50, 100, 200]:
    report("old", fl, "normal", "epic", True, False)

print("\nNEW")
for fl in [10, 30, 50, 100, 200]:
    report("new-norm", fl, "normal", "legendary", True, True)
    report("new-epic", fl, "normal", "epic", True, True)
    report("new-rare", fl, "normal", "rare", False, True)
    report("new-hard", fl, "hard", "legendary", True, True, affix_atk=15)
    report("new-hell", fl, "hell", "legendary", True, True, affix_atk=35, affix_def=20, affix_hp=80)
