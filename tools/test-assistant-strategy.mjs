import fs from 'fs';
import vm from 'vm';

const html = fs.readFileSync('/workspace/index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) throw new Error('script not found');

// Extract only the assistant + minimal deps for isolated test
const src = scriptMatch[1];
const start = src.indexOf('function parseAssistantQuery');
const end = src.indexOf('function ensureChatLazyInit');
const chunk = src.slice(start, end);

const sandbox = {
  currentLang: 'zh',
  player: {
    level: 100,
    atk: 5000,
    def: 2000,
    maxHp: 25000,
    critChance: 0.15,
    allDmg: 0.08,
    equipment: {},
    talents: { talentAtk: 50, talentHp: 30 },
    memoryDecay: 5
  },
  currentDungeon: null,
  DUNGEON_TIERS: { normal: { mult: 1, hp: 1, atk: 1, def: 1, dodge: 1, resist: 0 }, hard: { mult: 1.8, hp: 1.85, atk: 1.75, def: 1.45, dodge: 1.2, resist: 0.1 }, hell: { mult: 3, hp: 3.4, atk: 3.0, def: 2.2, dodge: 1.5, resist: 0.18 } },
  MONSTER_POOL: [{ hp: 52, atk: 14, def: 5, spd: 4, dodge: 3 }],
  BOSS_POOL: [{ hp: 200, atk: 32, def: 10, spd: 4, dodge: 2 }],
  EQUIP_SLOTS: [{ slot: 'mainhand', baseStat: 'atk', baseValue: 8 }, { slot: 'offhand', baseStat: 'atk', baseValue: 5 }, { slot: 'armor', baseStat: 'def', baseValue: 6 }],
  RARITY_BASE_RM: { common: 1, rare: 1.35, epic: 1.75, legendary: 2.35, hidden: 4 },
  RARITY_AFFIX_COUNT: { common: 1, rare: 2, epic: 3, legendary: 3, hidden: 3 },
  CRAFT_RECIPES: [{ id: 'herb_mid', resultId: 'herb_mid', cost: { herb_low: 3 } }],
  TALENT_STATS: [{ key: 'talentAtk', name: '攻擊力', nameEn: 'ATK', max: 400, perPoint: 0.25 }],
  PLAYER_LEVEL_GAP: 50,
  EARLY_FLOOR_EASE_CAP: 20,
  NORMAL_FARM_EASE_END: 800,
  ENEMY_MAX_DODGE: 0.45,
  ENEMY_BOSS_MAX_DODGE: 0.35,
  console
};

const deps = `
function pct(n,d=2){return (Number(n)*100).toFixed(d)+'%';}
function getLevelMultiplier(fl){fl=Math.max(1,fl);if(fl<=100)return Math.pow(1.026,fl-1);if(fl<=400)return Math.pow(1.011,fl-1)*2.6;return Math.pow(1.011,399)*2.6+(fl-400)*0.18;}
function getEnemyHpScale(lvMult){return lvMult;}
function getEnemyAtkScale(lvMult){return lvMult*1.35;}
function getEnemyDefScale(lvMult){return Math.pow(lvMult,0.58);}
function getEarlyFloorEaseMult(fl,stat){fl=Math.max(1,fl|0);if(fl>20)return 1;const t=(fl-1)/19;if(stat==='hp')return 0.30+t*0.52;if(stat==='atk')return 0.22+t*0.56;if(stat==='def')return 0.40+t*0.48;if(stat==='flatAtk')return 0.15+t*0.85;return 1;}
function getNormalFarmEaseT(fl,tier){if(tier!=='normal')return 1;fl=Math.max(1,fl|0);if(fl<=20)return 0;if(fl>=800)return 1;return (fl-20)/(800-20);}
function getDropRates(tier,fl){return{common:0.15,rare:0.30,epic:0.05,legendary:0.000000021,hidden:0.000000052};}
function getItemQty(){return 2;}
function getUpgradeSuccessRate(lv){return Math.max(0.1,0.9-lv*0.08);}
function getTalentPercent(key){return 12.5;}
function getEquipPowerScore(){return 100;}
function recalcPlayerStats(){}
`;

vm.createContext(sandbox);
vm.runInContext(deps + chunk, sandbox);

const q1 = sandbox.queryGameStrategy('如果我想打100级的地狱级地城 装备需求是什么');
const q2 = sandbox.queryGameStrategy('分析我的角色');
const q3 = sandbox.buildDungeonStrategyGuide(100, 'hell');

for (const [label, out] of [['hell gear', q1], ['analysis', q2], ['direct', q3]]) {
  if (!out || !out.includes('><')) throw new Error(`bad output for ${label}`);
  console.log('---', label, '---');
  console.log(out.slice(0, 500));
  console.log('...');
}

console.log('All assistant strategy tests passed');
