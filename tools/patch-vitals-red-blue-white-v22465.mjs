#!/usr/bin/env node
import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const NEON_BARS =
  '.pixel-bar-hp .pixel-bar-cell.filled{background:linear-gradient(180deg,#ff4d7a 0%,#ff003c 55%,#d40030 100%);border-color:#ff6688;box-shadow:0 0 8px rgba(255,23,68,.95),0 0 3px rgba(255,80,120,.85),inset 0 -1px 0 rgba(255,150,170,.6)}.pixel-bar-shield .pixel-bar-cell.filled{background:linear-gradient(180deg,#ffffff 0%,#e8fcff 55%,#c8f0ff 100%);border-color:#fff;box-shadow:0 0 9px rgba(255,255,255,.98),0 0 4px rgba(180,240,255,.9),inset 0 -1px 0 rgba(255,255,255,.75)}.pixel-bar-xp .pixel-bar-cell.filled{background:linear-gradient(180deg,#66f8ff 0%,#00e5ff 55%,#00b8d4 100%);border-color:#88f6ff;box-shadow:0 0 8px rgba(0,229,255,.95),0 0 3px rgba(80,240,255,.85),inset 0 -1px 0 rgba(180,250,255,.6)}';

const CLASSIC_BARS =
  '.pixel-bar-hp .pixel-bar-cell.filled{background:linear-gradient(180deg,#e82828 0%,#a01010 100%);border-color:#c82020;box-shadow:0 0 3px rgba(180,30,30,.4)}.pixel-bar-shield .pixel-bar-cell.filled{background:linear-gradient(180deg,#ffffff 0%,#e8e8e8 100%);border-color:#fff;box-shadow:0 0 3px rgba(255,255,255,.35)}.pixel-bar-xp .pixel-bar-cell.filled{background:linear-gradient(180deg,#5aabf0 0%,#2878d8 100%);border-color:#7ec0ff;box-shadow:0 0 3px rgba(60,140,220,.4)}';

const NEON_VALS =
  '.pixel-neon-hp{color:#ff1744;text-shadow:0 0 4px rgba(255,23,68,.95),0 0 10px rgba(255,0,80,.8)}.pixel-neon-xp{color:#00e5ff;text-shadow:0 0 4px rgba(0,229,255,.95),0 0 10px rgba(0,200,255,.8)}.pixel-neon-shield{color:#fff;text-shadow:0 0 4px rgba(255,255,255,.98),0 0 10px rgba(200,240,255,.9)}';

const CLASSIC_VALS =
  '.pixel-neon-hp{color:#ff4444;text-shadow:none}.pixel-neon-xp{color:#4488ff;text-shadow:none}.pixel-neon-shield{color:#ffffff;text-shadow:none}';

if (!html.includes(NEON_BARS)) {
  throw new Error('Neon bar CSS block not found');
}
html = html.replace(NEON_BARS, CLASSIC_BARS);

if (!html.includes(NEON_VALS)) {
  throw new Error('Neon value CSS block not found');
}
html = html.replace(NEON_VALS, CLASSIC_VALS);

const cyberStart = html.indexOf('#game-main.in-dungeon{--dungeon-neon-hp');
if (cyberStart >= 0) {
  const cyberEnd = html.indexOf('#combat-dock{', cyberStart);
  if (cyberEnd < 0) throw new Error('combat-dock anchor not found after cyberpunk block');
  html = html.slice(0, cyberStart) + html.slice(cyberEnd);
}

html = html.replace(/content="2\.24\.64"/g, 'content="2.24.65"');
html = html.replace(/GAME_VERSION='2\.24\.64'/g, "GAME_VERSION='2.24.65'");
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.64'",
  "GAME_VERSION_HISTORY=[{version:'2.24.65',date:'2026-06-09',summary:{zh:'v2.24.65 生命／經驗／護盾改紅／藍／白像素條；地下城移除賽博朋克覆寫。',en:'v2.24.65 red/blue/white vital bars; remove dungeon cyberpunk overrides.'}},{version:'2.24.64'"
);
html = html.replace(
  "logBalanceV22464:'[功能 v2.24.64] 地下城套用賽博朋克調色：黑紫底、生命霓虹、經驗电光藍、護盾铬銀；玩家與怪物戰鬥卡同步。'",
  "logBalanceV22465:'[功能 v2.24.65] 生命／經驗／護盾像素條改紅／藍／白；地下城移除黑紫賽博朋克覆寫。',logBalanceV22464:'[功能 v2.24.64] 地下城套用賽博朋克調色：黑紫底、生命霓虹、經驗电光藍、護盾铬銀；玩家與怪物戰鬥卡同步。'"
);

const enLog = "logBalanceV22464:'[v2.24.64] Dungeon cyberpunk palette: black-purple base, neon HP, electric XP, chrome shield; battle cards synced.'";
const enLogNew =
  "logBalanceV22465:'[v2.24.65] HP/XP/shield pixel bars use red/blue/white; dungeon cyberpunk overrides removed.',logBalanceV22464:'[v2.24.64] Dungeon cyberpunk palette: black-purple base, neon HP, electric XP, chrome shield; battle cards synced.'";
if (html.includes(enLog)) html = html.replace(enLog, enLogNew);

fs.writeFileSync(path, html);
fs.writeFileSync(
  '/workspace/version.json',
  JSON.stringify({ version: '2.24.65', updated: '2026-06-09' }, null, 2) + '\n'
);
console.log('Patched to v2.24.65');
