#!/usr/bin/env python3
"""Apply v2.11.0 ultra-hardcore + daily curse patch."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:200]}")
    s = s.replace(old, new, 1)


rep("GAME_VERSION='2.10.0'", "GAME_VERSION='2.11.0'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.10.0'",
    "GAME_VERSION_HISTORY=[{version:'2.11.0',date:'2026-06-07',summary:{zh:'v2.11 極限硬核：崩壞懲罰加重、詞綴更兇、每日詛咒地城（全服同日詛咒、通關額外減崩壞）。',en:'v2.11 ultra-hardcore: stronger decay, harsher modifiers, daily cursed dungeon curse.'}},{version:'2.10.0'",
    "hist",
)
rep("SAVE_VERSION=38", "SAVE_VERSION=39", "save")

# i18n zh
rep(
    'logBalanceV210:"[平衡 v2.10]',
    'logBalanceV211:"[平衡 v2.11] 崩壞懲罰加重；詞綴強化；每日詛咒地城（入場顯示、通關額外減崩壞）。",dailyCurseTag:"☠ 今日詛咒: {0}",dailyCursePreview:"今日詛咒地城: {0}",curseBleed:"裂血",curseAbyss:"深淵",curseHollow:"空殼",curseRuin:"崩壞",curseWither:"枯萎",curseDread:"恐懼",curseEclipse:"蝕日",logCurseEntry:"[詛咒] 入場記憶崩壞 +{0}%",logCurseClearBonus:"[詛咒通關] 額外記憶崩壞 -2%",logBalanceV210:"[平衡 v2.10]',
    "i18n zh",
)
rep(
    'logBalanceV210:"[Balance v2.10]',
    'logBalanceV211:"[Balance v2.11] Stronger decay penalty; harsher modifiers; daily cursed dungeon with clear bonus.",dailyCurseTag:"☠ Daily curse: {0}",dailyCursePreview:"Today\'s cursed dungeon: {0}",curseBleed:"Bleed",curseAbyss:"Abyss",curseHollow:"Hollow",curseRuin:"Ruin",curseWither:"Wither",curseDread:"Dread",curseEclipse:"Eclipse",logCurseEntry:"[Curse] Entry memory decay +{0}%",logCurseClearBonus:"[Curse clear] Extra decay -2%",logBalanceV210:"[Balance v2.10]',
    "i18n en",
)

# Harsher constants + daily curses array
rep(
    "DUNGEON_MODIFIERS=[{id:'swift',enemySpd:1.15,xpMult:1.12,dropMult:1.08,labelKey:'modSwift',descKey:'modSwiftDesc'},{id:'armored',enemyDef:1.2,enemyHp:1.1,goldMult:1.15,labelKey:'modArmored',descKey:'modArmoredDesc'},{id:'frenzy',enemyAtk:1.15,dropMult:1.12,labelKey:'modFrenzy',descKey:'modFrenzyDesc'},{id:'plague',playerHpStart:0.88,dropMult:1.18,labelKey:'modPlague',descKey:'modPlagueDesc'},{id:'greed',goldMult:1.25,xpMult:0.92,labelKey:'modGreed',descKey:'modGreedDesc'},{id:'mist',playerDodgeMult:0.85,dropMult:1.1,labelKey:'modMist',descKey:'modMistDesc'}],DUNGEON_LAYOUTS=",
    "DUNGEON_MODIFIERS=[{id:'swift',enemySpd:1.22,xpMult:1.15,dropMult:1.1,labelKey:'modSwift',descKey:'modSwiftDesc'},{id:'armored',enemyDef:1.28,enemyHp:1.15,goldMult:1.18,labelKey:'modArmored',descKey:'modArmoredDesc'},{id:'frenzy',enemyAtk:1.22,dropMult:1.18,labelKey:'modFrenzy',descKey:'modFrenzyDesc'},{id:'plague',playerHpStart:0.82,dropMult:1.25,labelKey:'modPlague',descKey:'modPlagueDesc'},{id:'greed',goldMult:1.32,xpMult:0.88,labelKey:'modGreed',descKey:'modGreedDesc'},{id:'mist',playerDodgeMult:0.78,dropMult:1.15,labelKey:'modMist',descKey:'modMistDesc'}],DAILY_CURSES=[{id:'curse_bleed',isCurse:true,enemyAtk:1.2,playerHpStart:0.92,dropMult:1.22,labelKey:'curseBleed'},{id:'curse_abyss',isCurse:true,enemyHp:1.25,enemyDef:1.15,xpMult:1.25,labelKey:'curseAbyss'},{id:'curse_hollow',isCurse:true,playerDodgeMult:0.72,goldMult:1.3,labelKey:'curseHollow'},{id:'curse_ruin',isCurse:true,decayOnEntry:1.5,dropMult:1.35,labelKey:'curseRuin'},{id:'curse_wither',isCurse:true,enemySpd:1.2,playerHpStart:0.9,goldMult:1.22,labelKey:'curseWither'},{id:'curse_dread',isCurse:true,enemyAtk:1.18,enemySpd:1.12,xpMult:1.22,labelKey:'curseDread'},{id:'curse_eclipse',isCurse:true,enemyHp:1.2,enemyAtk:1.18,enemyDef:1.12,dropMult:1.28,labelKey:'curseEclipse'}],DUNGEON_LAYOUTS=",
    "modifiers",
)

rep(
    "ELITE_SPAWN_CHANCE=0.09,MEMORY_DECAY_COMBAT_MAX=0.45,MEMORY_DECAY_CLEAR_NORMAL=1,MEMORY_DECAY_CLEAR_HARD=3,MEMORY_DECAY_CLEAR_HELL=5,ESCAPE_DECAY_SUCCESS=0.8,ESCAPE_DECAY_FAIL=0.3,REPEAT_RUN_PENALTY=0.88,REPEAT_RUN_THRESHOLD=3;",
    "ELITE_SPAWN_CHANCE=0.12,MEMORY_DECAY_COMBAT_MAX=0.60,MEMORY_DECAY_CLEAR_NORMAL=2,MEMORY_DECAY_CLEAR_HARD=5,MEMORY_DECAY_CLEAR_HELL=8,MEMORY_DECAY_CURSE_CLEAR_BONUS=2,ESCAPE_DECAY_SUCCESS=1.2,ESCAPE_DECAY_FAIL=0.5,REPEAT_RUN_PENALTY=0.82,REPEAT_RUN_THRESHOLD=2,DEATH_STREAK_DECAY_RATE=0.18;",
    "consts",
)

rep(
    "function rollDungeonModifiers(tier){const n=tier==='hell'?2:tier==='hard'?2:1;return shuffleArray(DUNGEON_MODIFIERS).slice(0,n);}",
    "function getDailyCurse(){const key=new Date().toDateString();let h=0;for(let i=0;i<key.length;i++)h=((h<<5)-h)+key.charCodeAt(i)|0;return{...DAILY_CURSES[Math.abs(h)%DAILY_CURSES.length]};}function getDailyCurseLabel(){return t(getDailyCurse().labelKey);}function rollDungeonModifiers(tier){const n=tier==='hell'?3:tier==='hard'?2:1;const rolled=shuffleArray(DUNGEON_MODIFIERS).slice(0,n);rolled.push(getDailyCurse());return rolled;}",
    "roll mods",
)

rep(
    "function getDungeonModMult(key){if(!currentDungeon||!currentDungeon.modifiers)return 1;let m=1;for(const mod of currentDungeon.modifiers){if(mod[key]!=null)m*=mod[key];}return m;}",
    "function getDungeonModMult(key){if(!currentDungeon||!currentDungeon.modifiers)return 1;let m=1;for(const mod of currentDungeon.modifiers){if(mod[key]!=null&&key!=='decayOnEntry')m*=mod[key];}return m;}function getDungeonModFlat(key){if(!currentDungeon||!currentDungeon.modifiers)return 0;let sum=0;for(const mod of currentDungeon.modifiers){if(mod[key]!=null)sum+=mod[key];}return sum;}function hasActiveDailyCurse(){return!!(currentDungeon&&currentDungeon.modifiers&&currentDungeon.modifiers.some(m=>m.isCurse));}",
    "mod mult",
)

rep(
    "function formatDungeonModifierList(){if(!currentDungeon||!currentDungeon.modifiers||!currentDungeon.modifiers.length)return'';return currentDungeon.modifiers.map(m=>t(m.labelKey)).join(' · ');}",
    "function formatDungeonModifierList(){if(!currentDungeon||!currentDungeon.modifiers||!currentDungeon.modifiers.length)return'';const curse=currentDungeon.modifiers.find(m=>m.isCurse);const rest=currentDungeon.modifiers.filter(m=>!m.isCurse).map(m=>t(m.labelKey)).join(' · ');const cursePart=curse?t('dailyCurseTag',t(curse.labelKey)):'';return cursePart?(rest?cursePart+' · '+rest:cursePart):rest;}",
    "format mods",
)

rep(
    "el.textContent=mods?(layout+' · '+mods):layout;el.style.display='block';}",
    "el.textContent=mods?(layout+' · '+mods):layout;el.classList.toggle('cursed-run',hasActiveDailyCurse());el.style.display='block';}",
    "banner curse class",
)

rep(
    "function applyDecayReliefOnClear(tier){const relief=tier==='hell'?MEMORY_DECAY_CLEAR_HELL:tier==='hard'?MEMORY_DECAY_CLEAR_HARD:MEMORY_DECAY_CLEAR_NORMAL;if(relief<=0)return;const before=player.memoryDecay||0;player.memoryDecay=Math.max(0,parseFloat((before-relief).toFixed(1)));if(before>player.memoryDecay)logInfo(t('logDecayRelief',relief,player.memoryDecay.toFixed(1)));}",
    "function applyDecayReliefOnClear(tier,hadCurse){let relief=tier==='hell'?MEMORY_DECAY_CLEAR_HELL:tier==='hard'?MEMORY_DECAY_CLEAR_HARD:MEMORY_DECAY_CLEAR_NORMAL;if(hadCurse)relief+=MEMORY_DECAY_CURSE_CLEAR_BONUS;if(relief<=0)return;const before=player.memoryDecay||0;player.memoryDecay=Math.max(0,parseFloat((before-relief).toFixed(1)));if(before>player.memoryDecay)logInfo(t('logDecayRelief',relief,player.memoryDecay.toFixed(1)));if(hadCurse&&MEMORY_DECAY_CURSE_CLEAR_BONUS>0)logInfo(t('logCurseClearBonus'));}",
    "decay relief",
)

rep(
    "const clearedTier=currentDungeon?currentDungeon.tier:null;bossDefeatOverlay.style.display='none';",
    "const clearedTier=currentDungeon?currentDungeon.tier:null;const hadCurse=hasActiveDailyCurse();bossDefeatOverlay.style.display='none';",
    "leave curse flag",
)
rep(
    "if(cleared){if(player.stats)player.stats.deathStreak=0;if(clearedTier)applyDecayReliefOnClear(clearedTier);}",
    "if(cleared){if(player.stats)player.stats.deathStreak=0;if(clearedTier)applyDecayReliefOnClear(clearedTier,hadCurse);}",
    "leave apply",
)

rep(
    "return parseFloat((base*(1+Math.max(0,streak-1)*0.12)).toFixed(1));}",
    "return parseFloat((base*(1+Math.max(0,streak-1)*DEATH_STREAK_DECAY_RATE)).toFixed(1));}",
    "death streak",
)

rep(
    "generateDungeon(tierLevel,tier);trackDungeonRunStart(tierLevel,tier);recalcPlayerStats();const hpStart=getDungeonModMult('playerHpStart');",
    "generateDungeon(tierLevel,tier);trackDungeonRunStart(tierLevel,tier);const entryDecay=getDungeonModFlat('decayOnEntry');if(entryDecay>0){player.memoryDecay=Math.min(100,parseFloat(((player.memoryDecay||0)+entryDecay).toFixed(1)));logInfo(t('logCurseEntry',entryDecay));}recalcPlayerStats();const hpStart=getDungeonModMult('playerHpStart');",
    "curse entry",
)

rep(
    'diffInfo.innerHTML=`<div style="color:var(--accent);">已選擇地城等級: Lv.${levelStart} - ${levelEnd}</div><div style="color:#888;font-size:0.55rem;margin-top:0.35rem;">${t(\'diffVarietyHint\')}</div>`;',
    'diffInfo.innerHTML=`<div style="color:var(--accent);">已選擇地城等級: Lv.${levelStart} - ${levelEnd}</div><div style="color:#888;font-size:0.55rem;margin-top:0.35rem;">${t(\'diffVarietyHint\')}</div><div style="color:var(--decay);font-size:0.55rem;margin-top:0.3rem;">${t(\'dailyCursePreview\',getDailyCurseLabel())}</div>`;',
    "diff preview",
)

# CSS for cursed banner
rep(
    "#dungeon-run-banner{font-size:0.55rem;color:#aaa;padding:0.2rem 0.35rem 0.35rem;text-align:center;line-height:1.35;width:100%;display:none}",
    "#dungeon-run-banner{font-size:0.55rem;color:#aaa;padding:0.2rem 0.35rem 0.35rem;text-align:center;line-height:1.35;width:100%;display:none}#dungeon-run-banner.cursed-run{color:var(--decay)}",
    "css curse",
)

# Migration
rep(
    'function migrateSave(data){if(data.version<38){data._balanceV210Notice=true;data.version=38;}',
    'function migrateSave(data){if(data.version<39){data._balanceV211Notice=true;data.version=39;}if(data.version<38){data._balanceV210Notice=true;data.version=38;}',
    "migrate",
)
rep(
    'const _balanceV210Notice=!!data._balanceV210Notice;delete data._balanceV210Notice;',
    'const _balanceV210Notice=!!data._balanceV210Notice;delete data._balanceV210Notice;const _balanceV211Notice=!!data._balanceV211Notice;delete data._balanceV211Notice;',
    "load var",
)
rep(
    "if(_balanceV210Notice)logInfo(t('logBalanceV210'));leaderboardTrackedLevel=-1;",
    "if(_balanceV210Notice)logInfo(t('logBalanceV210'));if(_balanceV211Notice)logInfo(t('logBalanceV211'));leaderboardTrackedLevel=-1;",
    "load log",
)

path.write_text(s)
print("v2.11.0 patch OK")
