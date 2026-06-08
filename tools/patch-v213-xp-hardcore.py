#!/usr/bin/env python3
"""Apply v2.13.0 hardcore XP rebalance."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:240]}")
    s = s.replace(old, new, 1)


rep("GAME_VERSION='2.12.0'", "GAME_VERSION='2.13.0'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.12.0'",
    "GAME_VERSION_HISTORY=[{version:'2.13.0',date:'2026-06-07',summary:{zh:'v2.13 硬核經驗值優化：手動戰鬥收益提升、通關獎勵、重複刷圖懲罰放寬。',en:'v2.13 hardcore XP rebalance: better manual combat rewards and clear bonuses.'}},{version:'2.12.0'",
    "hist",
)
rep("SAVE_VERSION=41", "SAVE_VERSION=42", "save")

rep(
    'logBalanceV212:"[更新 v2.12] 已移除掛機系統與無人機戰鬥功能。",',
    'logBalanceV213:"[平衡 v2.13] 經驗值優化：貼合純手動硬核戰鬥，適等級地城約 1 趟升 1 級；通關額外獎勵；重複刷圖經驗懲罰放寬。",logBalanceV212:"[更新 v2.12] 已移除掛機系統與無人機戰鬥功能。",',
    "i18n zh",
)
rep(
    'logBalanceV212:"[Update v2.12] Idle system and drone battle features removed.",',
    'logBalanceV213:"[Balance v2.13] XP tuned for manual hardcore combat; clear bonus; softer repeat-run XP penalty.",logBalanceV212:"[Update v2.12] Idle system and drone battle features removed.",',
    "i18n en",
)

rep(
    "REPEAT_RUN_PENALTY=0.82,REPEAT_RUN_THRESHOLD=2,DEATH_STREAK_DECAY_RATE=0.18;",
    "REPEAT_RUN_PENALTY=0.82,REPEAT_RUN_XP_PENALTY=0.90,REPEAT_RUN_THRESHOLD=2,DEATH_STREAK_DECAY_RATE=0.18,XP_CLEAR_BONUS_NORMAL=0.05,XP_CLEAR_BONUS_HARD=0.06,XP_CLEAR_BONUS_HELL=0.05,HARDCORE_XP_MULT_NORMAL=1.12,HARDCORE_XP_MULT_HARD=1.10,HARDCORE_XP_MULT_HELL=1.06;",
    "consts",
)

rep("XP_REWARD_GROWTH=1.003", "XP_REWARD_GROWTH=1.0055", "reward growth")

rep(
    "function getXpDifficultyMult(tier){return tier==='hell'?2.4:tier==='hard'?1.65:1;}",
    "function getXpDifficultyMult(tier){return tier==='hell'?2.4:tier==='hard'?1.65:1;}function getHardcoreXpMult(tier){return tier==='hell'?HARDCORE_XP_MULT_HELL:tier==='hard'?HARDCORE_XP_MULT_HARD:HARDCORE_XP_MULT_NORMAL;}function getDungeonClearXpBonus(tier){const rate=tier==='hell'?XP_CLEAR_BONUS_HELL:tier==='hard'?XP_CLEAR_BONUS_HARD:XP_CLEAR_BONUS_NORMAL;return Math.max(0,Math.floor((player.xpToNext||1)*rate));}",
    "hardcore mult",
)

rep(
    "function calcEnemyXpReward(baseXp,floorLevel,tier,isBoss,refLevel){const pl=Math.max(1,refLevel!=null?refLevel:(player.level||1)),fl=Math.max(1,floorLevel),need=getXpRewardRef(fl),share=isBoss?0.19:0.033,gap=getLevelGapMult(fl,pl),tierMult=getXpDifficultyMult(tier),typeVar=0.92+(baseXp||6)/55;return Math.max(1,Math.floor(need*share*tierMult*gap*typeVar));}",
    "function calcEnemyXpReward(baseXp,floorLevel,tier,isBoss,refLevel){const pl=Math.max(1,refLevel!=null?refLevel:(player.level||1)),fl=Math.max(1,floorLevel),need=getXpRewardRef(fl),share=isBoss?0.20:0.036,gap=getLevelGapMult(fl,pl),tierMult=getXpDifficultyMult(tier),hc=getHardcoreXpMult(tier),typeVar=0.92+(baseXp||6)/55;return Math.max(1,Math.floor(need*share*tierMult*gap*typeVar*hc));}",
    "calc xp",
)

rep(
    "function getLevelGapMult(floorLevel,refLevel){const pl=Math.max(1,refLevel!=null?refLevel:(player.level||1)),fl=Math.max(1,floorLevel);if(pl>fl)return Math.max(0.12,1-(pl-fl)*0.09);return Math.min(1.30,1+(fl-pl)*0.05);}",
    "function getLevelGapMult(floorLevel,refLevel){const pl=Math.max(1,refLevel!=null?refLevel:(player.level||1)),fl=Math.max(1,floorLevel);if(pl>fl)return Math.max(0.18,1-(pl-fl)*0.075);return Math.min(1.30,1+(fl-pl)*0.05);}",
    "gap mult",
)

rep(
    "function getRepeatRunRewardMult(){if(!currentDungeon||!player.stats)return 1;const key=currentDungeon.tierLevel+'_'+currentDungeon.tier,today=new Date().toDateString();if(player.stats.runDayKey!==today)return 1;const n=(player.stats.runsByKey&&player.stats.runsByKey[key])||0;return n>=REPEAT_RUN_THRESHOLD?REPEAT_RUN_PENALTY:1;}",
    "function getRepeatRunRewardMult(){if(!currentDungeon||!player.stats)return 1;const key=currentDungeon.tierLevel+'_'+currentDungeon.tier,today=new Date().toDateString();if(player.stats.runDayKey!==today)return 1;const n=(player.stats.runsByKey&&player.stats.runsByKey[key])||0;return n>=REPEAT_RUN_THRESHOLD?REPEAT_RUN_PENALTY:1;}function getRepeatRunXpMult(){if(!currentDungeon||!player.stats)return 1;const key=currentDungeon.tierLevel+'_'+currentDungeon.tier,today=new Date().toDateString();if(player.stats.runDayKey!==today)return 1;const n=(player.stats.runsByKey&&player.stats.runsByKey[key])||0;return n>=REPEAT_RUN_THRESHOLD?REPEAT_RUN_XP_PENALTY:1;}",
    "repeat xp mult",
)

rep(
    "const _runMult=getRepeatRunRewardMult();const _modGold=getDungeonModMult('goldMult');const _modXp=getDungeonModMult('xpMult');const baseGold=Math.floor(currentEnemy.gold*_goldGap*_runMult*_modGold);const bonusGold=Math.floor(baseGold*player.goldBonus);const totalGold=baseGold+bonusGold;player.gold+=totalGold;lootArea.innerHTML=`金幣: +${totalGold}`;const _xpGain=Math.floor(currentEnemy.xp*_runMult*_modXp);player.xp+=_xpGain;lootArea.innerHTML+=` | 經驗: +${_xpGain}`;",
    "const _runGoldMult=getRepeatRunRewardMult();const _runXpMult=getRepeatRunXpMult();const _modGold=getDungeonModMult('goldMult');const _modXp=getDungeonModMult('xpMult');const baseGold=Math.floor(currentEnemy.gold*_goldGap*_runGoldMult*_modGold);const bonusGold=Math.floor(baseGold*player.goldBonus);const totalGold=baseGold+bonusGold;player.gold+=totalGold;lootArea.innerHTML=`金幣: +${totalGold}`;const _xpGain=Math.floor(currentEnemy.xp*_runXpMult*_modXp);player.xp+=_xpGain;lootArea.innerHTML+=` | 經驗: +${_xpGain}`;if(wasBoss&&currentDungeon){const _clearBonus=getDungeonClearXpBonus(currentDungeon.tier);if(_clearBonus>0){player.xp+=_clearBonus;lootArea.innerHTML+=` | 通關: +${_clearBonus}`;}}",
    "kill enemy xp",
)

rep(
    "function migrateSave(data){if(data.version<41){data._balanceV212Notice=true;data.version=41;}",
    "function migrateSave(data){if(data.version<42){data._balanceV213Notice=true;data.version=42;}if(data.version<41){data._balanceV212Notice=true;data.version=41;}",
    "migrate",
)
rep(
    "const _balanceV212Notice=!!data._balanceV212Notice;delete data._balanceV212Notice;",
    "const _balanceV212Notice=!!data._balanceV212Notice;delete data._balanceV212Notice;const _balanceV213Notice=!!data._balanceV213Notice;delete data._balanceV213Notice;",
    "load var",
)
rep(
    "if(_balanceV212Notice)logInfo(t('logBalanceV212'));leaderboardTrackedLevel=-1;",
    "if(_balanceV212Notice)logInfo(t('logBalanceV212'));if(_balanceV213Notice)logInfo(t('logBalanceV213'));leaderboardTrackedLevel=-1;",
    "load log",
)

path.write_text(s)
print("v2.13.0 XP patch OK")
