#!/usr/bin/env python3
"""Apply v2.10.0 hardcore + dungeon variety patch to index.html."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:220]}")
    s = s.replace(old, new, 1)


# HTML + CSS
rep(
    '<div id="map-container"><div id="map"></div></div>',
    '<div id="map-container"><div id="dungeon-run-banner"></div><div id="map"></div></div>',
    "html",
)
rep(
    "#map-container{padding:.5rem .67rem;border-bottom:1px solid #1a1a1a;flex-shrink:0;display:flex;justify-content:center}",
    "#map-container{padding:.5rem .67rem 0;border-bottom:1px solid #1a1a1a;flex-shrink:0;display:flex;flex-direction:column;align-items:center}#dungeon-run-banner{font-size:0.55rem;color:#aaa;padding:0.2rem 0.35rem 0.35rem;text-align:center;line-height:1.35;width:100%;display:none}",
    "css",
)

rep("GAME_VERSION='2.9.2'", "GAME_VERSION='2.10.0'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.9.2'",
    "GAME_VERSION_HISTORY=[{version:'2.10.0',date:'2026-06-07',summary:{zh:'v2.10 硬核變數：每趟隨機詞綴與布局、事件格、精英怪；記憶崩壞影響屬性；通關減崩壞、逃脫懲罰、重複刷圖懲罰。',en:'v2.10 hardcore variety: run modifiers, layouts, events, elites; decay hurts stats; clear relief, escape penalty, repeat-run tax.'}},{version:'2.9.2'",
    "hist",
)
rep("SAVE_VERSION=37", "SAVE_VERSION=38", "save")

rep(
    'logBalanceV292:"[平衡 v2.9.2]',
    'logBalanceV210:"[平衡 v2.10] 地城每趟隨機詞綴/布局/事件；記憶崩壞削弱屬性；通關可緩解崩壞。",modSwift:"疾風",modSwiftDesc:"敵人速度+15% · 經驗+12%",modArmored:"重甲",modArmoredDesc:"敵人防禦+20% 生命+10% · 金幣+15%",modFrenzy:"狂怒",modFrenzyDesc:"敵人攻擊+15% · 掉落+12%",modPlague:"瘟疫",modPlagueDesc:"入場生命88% · 掉落+18%",modGreed:"貪欲",modGreedDesc:"金幣+25% · 經驗-8%",modMist:"迷霧",modMistDesc:"閃避-15% · 掉落+10%",layoutOpen:"開闊",layoutDense:"密集",layoutHunter:"獵殺",layoutScatter:"分散",logDungeonLayout:"[地城] 布局: {0}",logDungeonMods:"[地城] 詞綴: {0}",logShrineHeal:"[聖壇] 恢復 {0} 生命",logShrineDecay:"[聖壇] 記憶崩壞 -1.2%",logShrineRisk:"[聖壇] 不穩定能量，受到 {0} 傷害",logTrap:"[陷阱] 受到 {0} 傷害",logCacheEquip:"[密藏] {0}",logCacheFrag:"[密藏] 背包已滿，裝備化為碎片",logDecayRelief:"[通關] 記憶崩壞 -{0}%（目前 {1}%）",logEscapeDecay:"[逃脫] 記憶崩壞 +{0}%",logRepeatRunPenalty:"[疲勞] 今日同地城重複挑戰，獎勵 x88%",diffVarietyHint:"每趟隨機布局與詞綴 · 精英怪與事件格",logBalanceV292:"[平衡 v2.9.2]',
    "i18n zh",
)
rep(
    'logBalanceV292:"[Balance v2.9.2]',
    'logBalanceV210:"[Balance v2.10] Random modifiers/layouts/events per run; memory decay weakens stats; clears ease decay.",modSwift:"Swift",modSwiftDesc:"Enemy SPD +15% · XP +12%",modArmored:"Armored",modArmoredDesc:"Enemy DEF +20% HP +10% · Gold +15%",modFrenzy:"Frenzy",modFrenzyDesc:"Enemy ATK +15% · Drops +12%",modPlague:"Plague",modPlagueDesc:"Enter at 88% HP · Drops +18%",modGreed:"Greed",modGreedDesc:"Gold +25% · XP -8%",modMist:"Mist",modMistDesc:"Dodge -15% · Drops +10%",layoutOpen:"Open",layoutDense:"Dense",layoutHunter:"Hunter",layoutScatter:"Scatter",logDungeonLayout:"[Dungeon] Layout: {0}",logDungeonMods:"[Dungeon] Modifiers: {0}",logShrineHeal:"[Shrine] Healed {0} HP",logShrineDecay:"[Shrine] Memory decay -1.2%",logShrineRisk:"[Shrine] Unstable energy — {0} damage",logTrap:"[Trap] Took {0} damage",logCacheEquip:"[Cache] {0}",logCacheFrag:"[Cache] Bag full — recycled to fragments",logDecayRelief:"[Clear] Memory decay -{0}% (now {1}%)",logEscapeDecay:"[Escape] Memory decay +{0}%",logRepeatRunPenalty:"[Fatigue] Same dungeon repeated today — rewards x88%",diffVarietyHint:"Random layout & modifiers · elites & events",logBalanceV292:"[Balance v2.9.2]',
    "i18n en",
)

rep(
    "hell:{mult:3,hp:3.2,atk:2.65,def:3.55,dodge:1.75,resist:0.22}};const PLAYER_BASE_SPD",
    "hell:{mult:3,hp:3.2,atk:2.65,def:3.55,dodge:1.75,resist:0.22}};const DUNGEON_MODIFIERS=[{id:'swift',enemySpd:1.15,xpMult:1.12,dropMult:1.08,labelKey:'modSwift',descKey:'modSwiftDesc'},{id:'armored',enemyDef:1.2,enemyHp:1.1,goldMult:1.15,labelKey:'modArmored',descKey:'modArmoredDesc'},{id:'frenzy',enemyAtk:1.15,dropMult:1.12,labelKey:'modFrenzy',descKey:'modFrenzyDesc'},{id:'plague',playerHpStart:0.88,dropMult:1.18,labelKey:'modPlague',descKey:'modPlagueDesc'},{id:'greed',goldMult:1.25,xpMult:0.92,labelKey:'modGreed',descKey:'modGreedDesc'},{id:'mist',playerDodgeMult:0.85,dropMult:1.1,labelKey:'modMist',descKey:'modMistDesc'}],DUNGEON_LAYOUTS=['open','dense','hunter','scatter'],ELITE_SPAWN_CHANCE=0.09,MEMORY_DECAY_COMBAT_MAX=0.45,MEMORY_DECAY_CLEAR_NORMAL=1,MEMORY_DECAY_CLEAR_HARD=3,MEMORY_DECAY_CLEAR_HELL=5,ESCAPE_DECAY_SUCCESS=0.8,ESCAPE_DECAY_FAIL=0.3,REPEAT_RUN_PENALTY=0.88,REPEAT_RUN_THRESHOLD=3;const PLAYER_BASE_SPD",
    "consts",
)

rep(
    "function pick(arr){return arr[Math.floor(Math.random()*arr.length)];}",
    "function pick(arr){return arr[Math.floor(Math.random()*arr.length)];}function shuffleArray(arr){const a=arr.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}",
    "shuffle",
)

OLD_GEN = (
    "function generateDungeon(tierLevel,tier){currentDungeon={tierLevel,tier,floorLevel:tierLevel*TIERS_PER_LEVEL-2};"
    "const monsterCount=rand(18,26);monstersRemaining=monsterCount;bossDefeated=false;bossLeaveAvailable=false;mapData=[];"
    "for(let r=0;r<7;r++){mapData[r]=[];for(let c=0;c<7;c++)mapData[r][c]={type:'empty',explored:false,enemy:null,droneLocked:false};}"
    "mapData[3][3]={type:'start',explored:true,enemy:null,droneLocked:false};playerPos={r:3,c:3};const edges=[];"
    "for(let r=0;r<7;r++)for(let c=0;c<7;c++)if((r===0||r===6||c===0||c===6)&&!(r===3&&c===3))edges.push({r,c});"
    "const exitPos=pick(edges);mapData[exitPos.r][exitPos.c]={type:'exit',explored:false,enemy:null,droneLocked:false};"
    "const allCells=[];for(let r=0;r<7;r++)for(let c=0;c<7;c++)if(!(r===3&&c===3)&&!(r===exitPos.r&&c===exitPos.c))allCells.push({r,c});"
    "const bossPos=pick(allCells);mapData[bossPos.r][bossPos.c]={type:'boss',explored:false,enemy:spawnMonster(true),droneLocked:false};"
    "const remaining=allCells.filter(p=>!(p.r===bossPos.r&&p.c===bossPos.c));"
    "for(let i=0;i<rand(2,4);i++){if(remaining.length===0)break;const idx=rand(0,remaining.length-1),p=remaining.splice(idx,1)[0];"
    "mapData[p.r][p.c]={type:'treasure',explored:false,enemy:null,droneLocked:false};}"
    "let placedMonsters=0;for(let i=0;i<monsterCount;i++){if(remaining.length===0)break;const idx=rand(0,remaining.length-1),p=remaining.splice(idx,1)[0];"
    "mapData[p.r][p.c]={type:'monster',explored:false,enemy:spawnMonster(false),droneLocked:false};placedMonsters++;}"
    "monstersRemaining=placedMonsters;inDungeon=true;}"
)

NEW_HELPERS = (
    "function rollDungeonModifiers(tier){const n=tier==='hell'?2:tier==='hard'?2:1;return shuffleArray(DUNGEON_MODIFIERS).slice(0,n);}"
    "function getDungeonModMult(key){if(!currentDungeon||!currentDungeon.modifiers)return 1;let m=1;for(const mod of currentDungeon.modifiers){if(mod[key]!=null)m*=mod[key];}return m;}"
    "function formatDungeonModifierList(){if(!currentDungeon||!currentDungeon.modifiers||!currentDungeon.modifiers.length)return'';return currentDungeon.modifiers.map(m=>t(m.labelKey)).join(' · ');}"
    "function formatDungeonLayoutLabel(){if(!currentDungeon||!currentDungeon.layout)return'';const k='layout'+currentDungeon.layout.charAt(0).toUpperCase()+currentDungeon.layout.slice(1);return t(k);}"
    "function updateDungeonRunBanner(){const el=document.getElementById('dungeon-run-banner');if(!el)return;if(!inDungeon||!currentDungeon){el.textContent='';el.style.display='none';return;}const layout=formatDungeonLayoutLabel(),mods=formatDungeonModifierList();el.textContent=mods?(layout+' · '+mods):layout;el.style.display='block';}"
    "function applyDungeonModsToEnemy(enemy,isBoss){if(!enemy||!currentDungeon)return enemy;const hpM=getDungeonModMult('enemyHp'),atkM=getDungeonModMult('enemyAtk'),defM=getDungeonModMult('enemyDef'),spdM=getDungeonModMult('enemySpd');"
    "if(hpM!==1){enemy.maxHp=Math.floor(enemy.maxHp*hpM);enemy.hp=enemy.maxHp;}if(atkM!==1)enemy.atk=Math.floor(enemy.atk*atkM);if(defM!==1)enemy.def=Math.floor(enemy.def*defM);if(spdM!==1)enemy.spd=Math.max(1,Math.floor(enemy.spd*spdM));"
    "if(isBoss&&currentDungeon.layout==='hunter'){enemy.maxHp=Math.floor(enemy.maxHp*1.1);enemy.hp=enemy.maxHp;enemy.atk=Math.floor(enemy.atk*1.08);}return enemy;}"
    "function maybeMakeElite(enemy){if(!enemy||enemy.isBoss||Math.random()>=ELITE_SPAWN_CHANCE)return enemy;enemy.elite=true;enemy.name=(currentLang==='zh'?'精英 ':'Elite ')+enemy.name;"
    "enemy.maxHp=Math.floor(enemy.maxHp*1.45);enemy.hp=enemy.maxHp;enemy.atk=Math.floor(enemy.atk*1.25);enemy.gold=Math.floor(enemy.gold*1.55);enemy.xp=Math.floor(enemy.xp*1.45);return enemy;}"
    "function getMemoryDecayCombatMult(){return Math.max(1-MEMORY_DECAY_COMBAT_MAX,1-((player.memoryDecay||0)/100)*MEMORY_DECAY_COMBAT_MAX);}"
    "function getRepeatRunRewardMult(){if(!currentDungeon||!player.stats)return 1;const key=currentDungeon.tierLevel+'_'+currentDungeon.tier,today=new Date().toDateString();if(player.stats.runDayKey!==today)return 1;"
    "const n=(player.stats.runsByKey&&player.stats.runsByKey[key])||0;return n>=REPEAT_RUN_THRESHOLD?REPEAT_RUN_PENALTY:1;}"
    "function trackDungeonRunStart(tierLevel,tier){if(!player.stats)player.stats=getDefaultPlayer().stats;const today=new Date().toDateString();if(player.stats.runDayKey!==today){player.stats.runDayKey=today;player.stats.runsByKey={};}"
    "const key=tierLevel+'_'+tier;player.stats.runsByKey[key]=(player.stats.runsByKey[key]||0)+1;if(player.stats.runsByKey[key]>=REPEAT_RUN_THRESHOLD)logInfo(t('logRepeatRunPenalty'));}"
    "function applyDecayReliefOnClear(tier){const relief=tier==='hell'?MEMORY_DECAY_CLEAR_HELL:tier==='hard'?MEMORY_DECAY_CLEAR_HARD:MEMORY_DECAY_CLEAR_NORMAL;if(relief<=0)return;"
    "const before=player.memoryDecay||0;player.memoryDecay=Math.max(0,parseFloat((before-relief).toFixed(1)));if(before>player.memoryDecay)logInfo(t('logDecayRelief',relief,player.memoryDecay.toFixed(1)));}"
    "function logDungeonRunVariety(){if(!currentDungeon)return;logInfo(t('logDungeonLayout',formatDungeonLayoutLabel()));if(currentDungeon.modifiers&&currentDungeon.modifiers.length)logInfo(t('logDungeonMods',formatDungeonModifierList()));}"
    "function handleShrineCell(){const roll=Math.random();if(roll<0.45){const heal=Math.floor(player.maxHp*0.22);player.hp=clamp(player.hp+heal,0,player.maxHp);logInfo(t('logShrineHeal',heal));}"
    "else if(roll<0.75){player.memoryDecay=Math.max(0,parseFloat(((player.memoryDecay||0)-1.2).toFixed(1)));logInfo(t('logShrineDecay'));}else{const dmg=Math.floor(player.maxHp*0.12);player.hp=clamp(player.hp-dmg,0,player.maxHp);logInfo(t('logShrineRisk',dmg));if(player.hp<=0)checkDeath();}}"
    "function handleTrapCell(){const dmg=Math.max(1,Math.floor(player.maxHp*0.14));player.hp=clamp(player.hp-dmg,0,player.maxHp);flashEntity('player-card');logInfo(t('logTrap',dmg));if(player.hp<=0)checkDeath();}"
    "function handleCacheCell(){const roll=Math.random();if(roll<0.35){addItem('herb_mid',1);logItemLoot('herb_mid');}else if(roll<0.55){addItem('upgradeStone',1);logItemLoot('upgradeStone');}"
    "else if(roll<0.75){addItem('equipFragment',rand(8,20));logInfo(t('msgLootItem',formatItemName('equipFragment')));}else{const eq=generateEquipment(getDungeonEquipmentLevel(currentDungeon.floorLevel));"
    "if(tryAddEquipToInventory(eq,true))logInfo(t('logCacheEquip',equipToString(eq,false)));else{addItem('equipFragment',getRecycleFragments(eq));logInfo(t('logCacheFrag'));}}}"
)

NEW_GEN_BODY = (
    "function generateDungeon(tierLevel,tier){const layout=pick(DUNGEON_LAYOUTS),modifiers=rollDungeonModifiers(tier);"
    "currentDungeon={tierLevel,tier,floorLevel:tierLevel*TIERS_PER_LEVEL-2,layout,modifiers};let monsterCount=rand(18,26),treasureCount=rand(2,4),startPos={r:3,c:3};"
    "if(layout==='dense'){monsterCount+=5;treasureCount=Math.max(1,treasureCount-1);}if(layout==='scatter')startPos={r:rand(1,5),c:rand(1,5)};"
    "monstersRemaining=monsterCount;bossDefeated=false;bossLeaveAvailable=false;mapData=[];"
    "for(let r=0;r<7;r++){mapData[r]=[];for(let c=0;c<7;c++)mapData[r][c]={type:'empty',explored:false,enemy:null,droneLocked:false};}"
    "mapData[startPos.r][startPos.c]={type:'start',explored:true,enemy:null,droneLocked:false};playerPos={r:startPos.r,c:startPos.c};const edges=[];"
    "for(let r=0;r<7;r++)for(let c=0;c<7;c++)if((r===0||r===6||c===0||c===6)&&!(r===startPos.r&&c===startPos.c))edges.push({r,c});"
    "let exitPos;if(layout==='scatter'){const far=edges.filter(p=>Math.abs(p.r-startPos.r)+Math.abs(p.c-startPos.c)>=8);exitPos=pick(far.length?far:edges);}else exitPos=pick(edges);"
    "mapData[exitPos.r][exitPos.c]={type:'exit',explored:false,enemy:null,droneLocked:false};const allCells=[];"
    "for(let r=0;r<7;r++)for(let c=0;c<7;c++)if(!((r===startPos.r&&c===startPos.c)||(r===exitPos.r&&c===exitPos.c)))allCells.push({r,c});"
    "let bossPos;if(layout==='hunter'){const huntEdges=edges.filter(p=>!(p.r===exitPos.r&&p.c===exitPos.c));bossPos=pick(huntEdges.length?huntEdges:allCells);}else bossPos=pick(allCells);"
    "mapData[bossPos.r][bossPos.c]={type:'boss',explored:false,enemy:spawnMonster(true),droneLocked:false};"
    "const remaining=allCells.filter(p=>!(p.r===bossPos.r&&p.c===bossPos.c));const eventTypes=shuffleArray(['shrine','trap','cache']);const eventCount=layout==='dense'?2:rand(1,2);"
    "for(let i=0;i<eventCount&&remaining.length;i++){const idx=rand(0,remaining.length-1),p=remaining.splice(idx,1)[0];mapData[p.r][p.c]={type:eventTypes[i%eventTypes.length],explored:false,enemy:null,droneLocked:false};}"
    "for(let i=0;i<treasureCount;i++){if(remaining.length===0)break;const idx=rand(0,remaining.length-1),p=remaining.splice(idx,1)[0];mapData[p.r][p.c]={type:'treasure',explored:false,enemy:null,droneLocked:false};}"
    "let placedMonsters=0;for(let i=0;i<monsterCount;i++){if(remaining.length===0)break;const idx=rand(0,remaining.length-1),p=remaining.splice(idx,1)[0];"
    "mapData[p.r][p.c]={type:'monster',explored:false,enemy:maybeMakeElite(spawnMonster(false)),droneLocked:false};placedMonsters++;}monstersRemaining=placedMonsters;inDungeon=true;}"
)

rep(OLD_GEN, NEW_HELPERS + NEW_GEN_BODY, "generateDungeon")

rep(
    "function spawnMonster(isBoss=false){if(!currentDungeon)return null;if(isBoss)return spawnBoss();",
    "function spawnMonster(isBoss=false){if(!currentDungeon)return null;if(isBoss)return applyDungeonModsToEnemy(spawnBoss(),true);",
    "spawn boss",
)
rep(
    "xp:calcEnemyXpReward(base.xp,currentDungeon.floorLevel,currentDungeon.tier,false)};}",
    "xp:calcEnemyXpReward(base.xp,currentDungeon.floorLevel,currentDungeon.tier,false)};return applyDungeonModsToEnemy(enemy,false);}",
    "spawn mob",
)

rep(
    "else if(cell.type==='treasure'){const eq=generateEquipment(getDungeonEquipmentLevel(currentDungeon.floorLevel+TIERS_PER_LEVEL-1));tryAddEquipToInventory(eq);logInfo(`寶箱: ${equipToString(eq,false)}`);mapData[r][c].type='empty';}",
    "else if(cell.type==='shrine'){handleShrineCell();mapData[r][c].type='empty';}else if(cell.type==='trap'){handleTrapCell();mapData[r][c].type='empty';}else if(cell.type==='cache'){handleCacheCell();mapData[r][c].type='empty';}else if(cell.type==='treasure'){const eq=generateEquipment(getDungeonEquipmentLevel(currentDungeon.floorLevel+TIERS_PER_LEVEL-1));tryAddEquipToInventory(eq);logInfo(`寶箱: ${equipToString(eq,false)}`);mapData[r][c].type='empty';}",
    "moveTo events",
)

rep(
    "if(cell.droneLocked&&cell.enemy)return'!';switch(cell.type){case'start':return'S';case'exit':return'E';case'boss':return cell.enemy?'M':'X';case'monster':return cell.enemy?'M':'X';case'treasure':return'$';default:return'.';}",
    "if(cell.droneLocked&&cell.enemy)return'!';if(cell.enemy&&cell.enemy.elite)return'!';switch(cell.type){case'start':return'S';case'exit':return'E';case'boss':return cell.enemy?'M':'X';case'monster':return cell.enemy?(cell.enemy.elite?'!':'M'):'X';case'treasure':return'$';case'shrine':return cell.explored?'+':'?';case'trap':return cell.explored?'^':'?';case'cache':return cell.explored?'C':'?';default:return'.';}",
    "getCellChar",
)

rep(
    "else if(cell.type==='treasure')classes.push('unexplored-treasure');else classes.push('unexplored');",
    "else if(cell.type==='treasure')classes.push('unexplored-treasure');else if(cell.type==='shrine'||cell.type==='trap'||cell.type==='cache')classes.push('unexplored-event');else classes.push('unexplored');",
    "getCellClasses",
)

rep(
    "function leaveDungeon(cleared=false){bossDefeatOverlay.style.display='none';clearAllTimers();clearDroneTimers();inCombat=false;currentEnemy=null;inDungeon=false;currentDungeon=null;",
    "function leaveDungeon(cleared=false){const clearedTier=currentDungeon?currentDungeon.tier:null;bossDefeatOverlay.style.display='none';clearAllTimers();clearDroneTimers();inCombat=false;currentEnemy=null;inDungeon=false;currentDungeon=null;",
    "leave start",
)
rep(
    "if(cleared&&player.drone&&player.drone.dead){repairDrone();}if(cleared)logInfo(t('msgDungeonCleared'));throttleSave();}",
    "if(cleared){if(player.stats)player.stats.deathStreak=0;if(clearedTier)applyDecayReliefOnClear(clearedTier);}if(cleared&&player.drone&&player.drone.dead){repairDrone();}if(cleared)logInfo(t('msgDungeonCleared'));updateDungeonRunBanner();throttleSave();}",
    "leave end",
)

rep(
    "function tryEscape(){if(!inDungeon||droneDungeonActive)return;const escapeChance=getEscapeChance();if(Math.random()<escapeChance){logInfo(t('msgEscapeSuccess'));leaveDungeon(false);}else{logInfo(t('msgEscapeFail'));}}",
    "function tryEscape(){if(!inDungeon||droneDungeonActive)return;const escapeChance=getEscapeChance();if(Math.random()<escapeChance){player.memoryDecay=Math.min(100,parseFloat(((player.memoryDecay||0)+ESCAPE_DECAY_SUCCESS).toFixed(1)));logInfo(t('msgEscapeSuccess'));logInfo(t('logEscapeDecay',ESCAPE_DECAY_SUCCESS));leaveDungeon(false);}else{player.memoryDecay=Math.min(100,parseFloat(((player.memoryDecay||0)+ESCAPE_DECAY_FAIL).toFixed(1)));logInfo(t('msgEscapeFail'));logInfo(t('logEscapeDecay',ESCAPE_DECAY_FAIL));}}",
    "escape",
)

rep(
    "function getMemoryDecayIncrease(){return Math.min(MEMORY_DECAY_CAP,parseFloat((MEMORY_DECAY_BASE+Math.floor((player.level||1)*MEMORY_DECAY_LEVEL_FACTOR)).toFixed(1)));}",
    "function getMemoryDecayIncrease(){const base=Math.min(MEMORY_DECAY_CAP,parseFloat((MEMORY_DECAY_BASE+Math.floor((player.level||1)*MEMORY_DECAY_LEVEL_FACTOR)).toFixed(1)));const streak=player.stats?(player.stats.deathStreak||0):0;return parseFloat((base*(1+Math.max(0,streak-1)*0.12)).toFixed(1));}",
    "decay inc",
)

rep(
    "const decayIncrease=getMemoryDecayIncrease();player.memoryDecay=Math.min(100,parseFloat((player.memoryDecay+decayIncrease).toFixed(1)));",
    "if(!player.stats)player.stats=getDefaultPlayer().stats;player.stats.deathStreak=(player.stats.deathStreak||0)+1;const decayIncrease=getMemoryDecayIncrease();player.memoryDecay=Math.min(100,parseFloat((player.memoryDecay+decayIncrease).toFixed(1)));",
    "checkDeath streak",
)

rep(
    "let baseAtk=baseLevelAtk+equipAtk*(1+talentAtkPct),baseDef=baseLevelDef+equipDef*(1+talentDefPct),baseMaxHp=baseLevelMaxHp+equipMaxHp*(1+talentHpPct),baseSpd=baseLevelSpd+equipSpd*(1+talentSpdPct);let lifesteal=0,critChance=0.05,critDmg=0,dodge=equipDodge/100,goldBonus=0;",
    "let baseAtk=baseLevelAtk+equipAtk*(1+talentAtkPct),baseDef=baseLevelDef+equipDef*(1+talentDefPct),baseMaxHp=baseLevelMaxHp+equipMaxHp*(1+talentHpPct),baseSpd=baseLevelSpd+equipSpd*(1+talentSpdPct);const decayMult=getMemoryDecayCombatMult();baseAtk*=decayMult;baseDef*=decayMult;baseMaxHp*=decayMult;let lifesteal=0,critChance=0.05,critDmg=0,dodge=(equipDodge/100)*(inDungeon?getDungeonModMult('playerDodgeMult'):1),goldBonus=0;",
    "recalc stats",
)

rep(
    "const _fl=currentDungeon?currentDungeon.floorLevel:(player.level||1);const _goldGap=getGoldLevelGapMult(_fl);const baseGold=Math.floor(currentEnemy.gold*_goldGap);",
    "const _fl=currentDungeon?currentDungeon.floorLevel:(player.level||1);const _goldGap=getGoldLevelGapMult(_fl);const _runMult=getRepeatRunRewardMult();const _modGold=getDungeonModMult('goldMult');const _modXp=getDungeonModMult('xpMult');const baseGold=Math.floor(currentEnemy.gold*_goldGap*_runMult*_modGold);",
    "kill gold",
)
rep(
    "player.xp+=currentEnemy.xp;lootArea.innerHTML+=` | 經驗: +${currentEnemy.xp}`;",
    "const _xpGain=Math.floor(currentEnemy.xp*_runMult*_modXp);player.xp+=_xpGain;lootArea.innerHTML+=` | 經驗: +${_xpGain}`;",
    "kill xp",
)

rep(
    "const common=Math.max(0.15,1-rare-epic-legendary-hidden);return{common,rare,epic,legendary,hidden};}",
    "const dropBoost=getDungeonModMult('dropMult');epic*=dropBoost;legendary*=dropBoost;hidden*=dropBoost;const common=Math.max(0.15,1-rare-epic-legendary-hidden);return{common,rare,epic,legendary,hidden};}",
    "drops",
)

rep(
    "generateDungeon(tierLevel,tier);player.hp=player.maxHp;player.shield=player.maxShield;if(useDrone){",
    "generateDungeon(tierLevel,tier);trackDungeonRunStart(tierLevel,tier);recalcPlayerStats();const hpStart=getDungeonModMult('playerHpStart');player.hp=hpStart<1?Math.floor(player.maxHp*hpStart):player.maxHp;player.shield=player.maxShield;if(useDrone){",
    "start internal hp",
)
rep(
    "logInfo(t('msgEnterDungeon',tierName,currentDungeon.floorLevel,currentDungeon.floorLevel+2,monstersRemaining));logInfo('擊殺BOSS即可解鎖出口');battleScreen.classList.remove('active');",
    "logInfo(t('msgEnterDungeon',tierName,currentDungeon.floorLevel,currentDungeon.floorLevel+2,monstersRemaining));logDungeonRunVariety();logInfo('擊殺BOSS即可解鎖出口');battleScreen.classList.remove('active');",
    "start manual log",
)
rep(
    "logInfo(t('msgEnterDungeon',tierName,currentDungeon.floorLevel,currentDungeon.floorLevel+2,monstersRemaining));logInfo('無人機正在自動探索地城...');",
    "logInfo(t('msgEnterDungeon',tierName,currentDungeon.floorLevel,currentDungeon.floorLevel+2,monstersRemaining));logDungeonRunVariety();logInfo('無人機正在自動探索地城...');",
    "start drone log",
)
rep(
    "renderMap();updateStatusBar();updateButtons();}throttleSave();}",
    "renderMap();updateDungeonRunBanner();updateStatusBar();updateButtons();}throttleSave();}",
    "start banner",
)

rep(
    "div.textContent=getCellChar(cell,r,c);}}}",
    "div.textContent=getCellChar(cell,r,c);}}updateDungeonRunBanner();}",
    "renderMap",
)

rep(
    "diffInfo.innerHTML=`<div style=\"color:var(--accent);\">已選擇地城等級: Lv.${levelStart} - ${levelEnd}</div>`;",
    "diffInfo.innerHTML=`<div style=\"color:var(--accent);\">已選擇地城等級: Lv.${levelStart} - ${levelEnd}</div><div style=\"color:#888;font-size:0.55rem;margin-top:0.35rem;\">${t('diffVarietyHint')}</div>`;",
    "difficulty hint",
)

rep(
    'function migrateSave(data){if(data.version<37){data._balanceV292Notice=true;data.version=37;}',
    'function migrateSave(data){if(data.version<38){data._balanceV210Notice=true;data.version=38;}if(data.version<37){data._balanceV292Notice=true;data.version=37;}',
    "migrate",
)
rep(
    'const _balanceV292Notice=!!data._balanceV292Notice;delete data._balanceV292Notice;',
    'const _balanceV292Notice=!!data._balanceV292Notice;delete data._balanceV292Notice;const _balanceV210Notice=!!data._balanceV210Notice;delete data._balanceV210Notice;',
    "load var",
)
rep(
    "if(_balanceV292Notice)logInfo(t('logBalanceV292'));leaderboardTrackedLevel=-1;",
    "if(_balanceV292Notice)logInfo(t('logBalanceV292'));if(_balanceV210Notice)logInfo(t('logBalanceV210'));leaderboardTrackedLevel=-1;",
    "load log",
)

# Tutorial updates
rep(
    "死亡會累積記憶崩壞值，達 100% 將永久刪除角色，請謹慎作戰。",
    "死亡會累積記憶崩壞值（越高屬性越弱），達 100% 將永久刪除角色。每趟地城有隨機布局、詞綴與事件格，請謹慎作戰。",
    "tut zh1",
)
rep(
    "Death raises Memory Decay; at 100% your character is permanently lost.",
    "Death raises Memory Decay (weakens stats); at 100% your character is permanently lost. Each dungeon run rolls layout, modifiers, and event cells.",
    "tut en1",
)
rep(
    "選定等級段後進入「選擇難度」：普通（x1.0）、困難（x1.8）、地獄（x3.0，需地獄門禁卡 #）。",
    "選定等級段後進入「選擇難度」：普通（x1.0）、困難（x1.8）、地獄（x3.0，需地獄門禁卡 #）。每趟會隨機布局（開闊/密集/獵殺/分散）與 1–2 個詞綴。",
    "tut zh2",
)
rep(
    "Then pick difficulty: Normal (x1.0), Hard (x1.8), Hell (x3.0, needs Hell Access Card #).",
    "Then pick difficulty: Normal/Hard/Hell. Each run rolls a layout (Open/Dense/Hunter/Scatter) and 1–2 modifiers.",
    "tut en2",
)

# CSS for unexplored-event - optional tint
rep(
    ".cell.unexplored-treasure{color:#fa0}",
    ".cell.unexplored-event{color:#8af}.cell.unexplored-treasure{color:#fa0}",
    "css event",
)

path.write_text(s)
print("v2.10.0 patch applied OK")
