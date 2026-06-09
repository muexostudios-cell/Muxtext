import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const earlyBoot = 'loadSettings();applySettings();scheduleChatMetrics();loadLanguage();';
const earlyBootNew = 'loadSettings();applySettings();scheduleChatMetrics();';
const stateAnchor =
  "combatTabBeforeFight='';function startPlaytimeCounter()";
const stateReplacement =
  "combatTabBeforeFight='';loadLanguage();function startPlaytimeCounter()";

if (!html.includes(earlyBoot)) throw new Error('early boot anchor missing');
if (!html.includes(stateAnchor)) throw new Error('state anchor missing');

html = html.replace(earlyBoot, earlyBootNew);
html = html.replace(stateAnchor, stateReplacement);

html = html.replace(/GAME_VERSION='2\.24\.49'/g, "GAME_VERSION='2.24.50'");
html = html.replace(
  '<meta name="game-version" content="2.24.49">',
  '<meta name="game-version" content="2.24.50">',
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.49'",
  "GAME_VERSION_HISTORY=[{version:'2.24.50',date:'2026-06-09',summary:{zh:'v2.24.50 修復已登入玩家重新整理後無法進入遊戲（語言載入觸發雲端同步時機）。',en:'v2.24.50 fix cannot enter after reload (defer language load before cloud sync).'}},{version:'2.24.49'",
);
html = html.replace(
  "logBalanceV22449:'[功能 v2.24.49]",
  "logBalanceV22450:'[修復 v2.24.50] 已登入玩家重新整理或更新後可正常進入遊戲；語言載入改在戰鬥狀態初始化之後執行。',logBalanceV22449:'[功能 v2.24.49]",
);
html = html.replace(
  "logBalanceV22449:'[Feature v2.24.49]",
  "logBalanceV22450:'[Fix v2.24.50] Logged-in players can enter after refresh/update; language load runs after combat state init.',logBalanceV22449:'[Feature v2.24.49]",
);

fs.writeFileSync(path, html);
fs.writeFileSync(
  '/workspace/version.json',
  JSON.stringify({ version: '2.24.50', publishedAt: Date.now() }, null, 2) + '\n',
);
console.log('Patched index.html -> v2.24.50 defer loadLanguage after combat state');
