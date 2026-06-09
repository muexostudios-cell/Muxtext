import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const CSS_ADD = `.pixel-icon{display:inline-block;width:22px;height:22px;image-rendering:pixelated;image-rendering:crisp-edges;vertical-align:middle;flex-shrink:0;border:1px solid #222;background:#050505}.pixel-icon-lg{width:32px;height:32px}.equip-entry-row,.item-entry-row{display:flex;align-items:flex-start;gap:6px}.equip-entry-text,.item-entry-text{flex:1;min-width:0;line-height:1.35}.equip-slot .equip-entry-row{align-items:center}`;

if (!html.includes('.pixel-icon{')) {
  html = html.replace('</style>', CSS_ADD + '</style>');
}

const PIXEL_MODULE = [
  "const PIXEL_ICON_SIZE=16;let _pixelIconCache=new Map();const _PIXEL_ICON_CACHE_MAX=800;",
  "function hashStr(s){let h=2166136261>>>0;const str=String(s||'');for(let i=0;i<str.length;i++){h^=str.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}",
  "function resolvePixelColor(color){if(!color)return '#ffffff';if(/^#[0-9a-f]{3,8}$/i.test(color)){if(color.length===4)return '#'+color[1]+color[1]+color[2]+color[2]+color[3]+color[3];return color;}try{const el=document.documentElement,tmp=document.createElement('span');tmp.style.color=color;el.appendChild(tmp);const resolved=getComputedStyle(tmp).color;el.removeChild(tmp);const m=resolved.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);if(m)return '#'+((1<<24)+(+m[1]<<16)+(+m[2]<<8)+ +m[3]).toString(16).slice(1);}catch(e){}return '#ffffff';}",
  "function hexToRgb(hex){const h=resolvePixelColor(hex).replace('#','');const n=parseInt(h.length===3?h.split('').map(c=>c+c).join(''):h,16);return{r:(n>>16)&255,g:(n>>8)&255,b:n&255};}",
  "function rgbToHex(r,g,b){return '#'+[r,g,b].map(v=>Math.max(0,Math.min(255,v|0)).toString(16).padStart(2,'0')).join('');}",
  "function shadeColor(hex,amt){const c=hexToRgb(hex),f=amt>=0?255:0,t=Math.abs(amt);return rgbToHex(Math.round(c.r+(f-c.r)*t),Math.round(c.g+(f-c.g)*t),Math.round(c.b+(f-c.b)*t));}",
  "function makePixelGrid(){return new Uint8ClampedArray(PIXEL_ICON_SIZE*PIXEL_ICON_SIZE*4);}",
  "function setGridPx(g,x,y,rgba){if(x<0||y<0||x>=PIXEL_ICON_SIZE||y>=PIXEL_ICON_SIZE)return;const i=(y*PIXEL_ICON_SIZE+x)*4;g[i]=rgba[0];g[i+1]=rgba[1];g[i+2]=rgba[2];g[i+3]=rgba[3]!=null?rgba[3]:255;}",
  "function fillGridRect(g,x,y,w,h,rgba){for(let dy=0;dy<h;dy++)for(let dx=0;dx<w;dx++)setGridPx(g,x+dx,y+dy,rgba);}",
  "function gridToDataUrl(grid){const c=document.createElement('canvas');c.width=PIXEL_ICON_SIZE;c.height=PIXEL_ICON_SIZE;const ctx=c.getContext('2d');const img=ctx.createImageData(PIXEL_ICON_SIZE,PIXEL_ICON_SIZE);img.data.set(grid);ctx.putImageData(img,0,0);return c.toDataURL('image/png');}",
  "function cachePixelIcon(key,grid){if(_pixelIconCache.size>=_PIXEL_ICON_CACHE_MAX)_pixelIconCache.clear();const url=gridToDataUrl(grid);_pixelIconCache.set(key,url);return url;}",
  "function getCachedPixelIcon(key,drawFn){if(_pixelIconCache.has(key))return _pixelIconCache.get(key);const grid=makePixelGrid();drawFn(grid);return cachePixelIcon(key,grid);}",
  "function parseNameThemes(nameKey,displayName){const s=(String(nameKey||'')+' '+String(displayName||'')).toLowerCase();return{void:/void|虚空|虛空|abyss|深淵/.test(s),shadow:/shadow|幽|shade|night|夢魘|nightmare|cloak|披風/.test(s),fire:/flame|fire|chaos|混沌|plasma|等离|等離子|overclock|超頻/.test(s),ice:/frost|ice|eclipse|日蝕/.test(s),energy:/ion|離子|beam|光|quantum|量子|pulse|脈衝|omega|核心|photon|光子/.test(s),heavy:/hammer|鎚|axe|斧|apocalypse|dragon|龍|titan|泰坦|plate|甲/.test(s),swift:/wind|風|dagger|刀|shuriken|飛刃|boot|靴|boots|dash/.test(s),reaper:/reaper|收割|scythe|void|requiem|安魂/.test(s),shield:/shield|盾|buckler|圓盾|field|力場/.test(s)};}",
  "function drawEquipPixels(grid,slot,nameKey,colorHex,seed){const disp=typeof getEquipDisplayName==='function'?getEquipDisplayName(nameKey):nameKey;const themes=parseNameThemes(nameKey,disp);const main=hexToRgb(colorHex);const mainRgba=[main.r,main.g,main.b,255];const hi=hexToRgb(shadeColor(colorHex,0.32));const lo=hexToRgb(shadeColor(colorHex,-0.38));const bg=[6,6,10,255];const accent=themes.void?[130,50,170,255]:themes.fire?[255,110,50,255]:themes.ice?[120,200,255,255]:themes.energy?[70,220,255,255]:themes.shadow?[70,70,100,255]:[hi.r,hi.g,hi.b,255];fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,bg);const v=seed%7;if(slot==='mainhand'||slot==='offhand'){const tall=slot==='mainhand';const bx=tall?6:7;const len=tall?9+v%3:6+v%2;for(let i=0;i<len;i++){setGridPx(grid,bx,2+i,mainRgba);setGridPx(grid,bx+(themes.heavy?1:0),2+i,[hi.r,hi.g,hi.b,255]);if(themes.reaper&&i<len-1)setGridPx(grid,bx-1,3+i,accent);if(themes.energy&&i%3===1)setGridPx(grid,bx+2,2+i,accent);}fillGridRect(grid,bx,2+len,2,3,[lo.r,lo.g,lo.b,255]);if(themes.shield&&slot==='offhand'){fillGridRect(grid,3,5,4,7,[main.r,main.g,main.b,220]);fillGridRect(grid,4,6,2,5,[hi.r,hi.g,hi.b,255]);}else if(slot==='offhand')fillGridRect(grid,3,8,3,3,[lo.r,lo.g,lo.b,200]);}else if(slot==='armor'){fillGridRect(grid,4,3,8,9,mainRgba);fillGridRect(grid,5,4,6,7,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,6,2,4,2,[lo.r,lo.g,lo.b,255]);if(themes.heavy){fillGridRect(grid,3,5,2,6,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,11,5,2,6,[lo.r,lo.g,lo.b,255]);}if(themes.shadow)setGridPx(grid,2,7,accent);if(themes.fire)setGridPx(grid,8,6,accent);}else if(slot==='armguard'){fillGridRect(grid,3,6,10,3,mainRgba);fillGridRect(grid,4,7,8,1,[hi.r,hi.g,hi.b,255]);if(themes.energy)for(let x=4;x<12;x+=2)setGridPx(grid,x,5,accent);}else if(slot==='legguard'){fillGridRect(grid,4,4,3,10,mainRgba);fillGridRect(grid,9,4,3,10,mainRgba);fillGridRect(grid,5,5,2,8,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,10,5,2,8,[hi.r,hi.g,hi.b,255]);}else if(slot==='boots'){fillGridRect(grid,3,10,5,3,mainRgba);fillGridRect(grid,4,6,3,5,mainRgba);fillGridRect(grid,9,11,4,2,[hi.r,hi.g,hi.b,255]);if(themes.swift)for(let x=1;x<5;x++)setGridPx(grid,x,12,accent);}if(seed%3===0)setGridPx(grid,1,1,accent);if(seed%5===0)setGridPx(grid,14,13,accent);}",
  "function drawItemPixels(grid,itemId,colorHex){const main=hexToRgb(colorHex);const mainRgba=[main.r,main.g,main.b,255];const hi=hexToRgb(shadeColor(colorHex,0.3));const lo=hexToRgb(shadeColor(colorHex,-0.35));const bg=[6,6,10,255];fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,bg);const id=String(itemId||'');if(id.startsWith('herb_')){const tall=id==='herb_high'?10:id==='herb_mid'?8:6;fillGridRect(grid,7,16-tall,2,tall-2,mainRgba);fillGridRect(grid,6,14,4,2,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,5,12,2,3,[hi.r,hi.g,hi.b,255]);setGridPx(grid,8,11,mainRgba);}else if(id.includes('upgradeStone')){const pts=[[8,3],[12,8],[8,13],[4,8]];for(let i=0;i<4;i++){const a=pts[i],b=pts[(i+1)%4];setGridPx(grid,a[0],a[1],mainRgba);setGridPx(grid,b[0],b[1],[hi.r,hi.g,hi.b,255]);}setGridPx(grid,8,8,[255,255,255,255]);}else if(id.includes('Fragment')||id==='equipFragment'){setGridPx(grid,5,4,mainRgba);setGridPx(grid,6,5,mainRgba);setGridPx(grid,7,6,mainRgba);setGridPx(grid,8,7,mainRgba);setGridPx(grid,7,8,[hi.r,hi.g,hi.b,255]);setGridPx(grid,6,9,lo.r!=null?[lo.r,lo.g,lo.b,255]:mainRgba);setGridPx(grid,9,5,[hi.r,hi.g,hi.b,255]);}else if(id==='hellTicket'){fillGridRect(grid,4,4,8,9,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,5,5,6,7,mainRgba);fillGridRect(grid,6,7,4,2,[hi.r,hi.g,hi.b,255]);}else if(id==='spaceStone'||id==='itemBagStone'){fillGridRect(grid,4,6,8,6,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,5,5,6,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,6,7,4,3,mainRgba);}else if(id==='encryptedWeaponCrate'){fillGridRect(grid,4,5,8,7,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,5,6,6,5,mainRgba);setGridPx(grid,7,8,[hi.r,hi.g,hi.b,255]);setGridPx(grid,8,9,mainRgba);}else if(id==='weaponCrateDecoder'){fillGridRect(grid,4,6,8,4,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,5,7,6,2,mainRgba);for(let x=5;x<11;x++)setGridPx(grid,x,5,[hi.r,hi.g,hi.b,255]);}else if(id==='renameCard'){fillGridRect(grid,4,5,8,7,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,5,6,6,5,mainRgba);fillGridRect(grid,6,8,4,1,[hi.r,hi.g,hi.b,255]);}else{fillGridRect(grid,5,5,6,6,mainRgba);setGridPx(grid,8,4,[hi.r,hi.g,hi.b,255]);setGridPx(grid,4,8,[lo.r,lo.g,lo.b,255]);}}",
  "function drawEmptySlotPixels(grid,slot){const bg=[6,6,10,255],ghost=[40,40,48,120];fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,bg);if(slot==='mainhand'||slot==='offhand'){for(let y=3;y<12;y++){setGridPx(grid,7,y,ghost);setGridPx(grid,8,y,ghost);}fillGridRect(grid,7,12,2,2,ghost);}else if(slot==='armor')fillGridRect(grid,5,4,6,8,ghost);else if(slot==='armguard')fillGridRect(grid,4,7,8,2,ghost);else if(slot==='legguard'){fillGridRect(grid,5,4,2,9,ghost);fillGridRect(grid,9,4,2,9,ghost);}else if(slot==='boots'){fillGridRect(grid,5,7,3,5,ghost);fillGridRect(grid,4,12,5,2,ghost);}else fillGridRect(grid,6,6,4,4,ghost);}",
  "function getEquipPixelIconUrl(eq){if(!eq)return'';const color=resolvePixelColor((typeof RARITY_COLORS!=='undefined'&&RARITY_COLORS[eq.rarity])||'#fff');const seed=hashStr((eq.name||'')+'|'+(eq.type||'')+'|'+eq.rarity);const key='eq|'+(eq.name||'')+'|'+(eq.type||'')+'|'+eq.rarity+'|'+color;return getCachedPixelIcon(key,g=>drawEquipPixels(g,eq.type||'mainhand',eq.name,color,seed));}",
  "function getItemPixelIconUrl(itemId){const color=resolvePixelColor(getItemColor(itemId));const key='it|'+itemId+'|'+color;return getCachedPixelIcon(key,g=>drawItemPixels(g,itemId,color));}",
  "function getEmptySlotPixelIconUrl(slot){const key='empty|'+slot;return getCachedPixelIcon(key,g=>drawEmptySlotPixels(g,slot));}",
  "function pixelIconImgHtml(url,size,cls){if(!url)return'';const px=size||22;const extra=cls?' '+cls:'';return '<img class=\"pixel-icon'+extra+'\" src=\"'+url+'\" width=\"'+px+'\" height=\"'+px+'\" alt=\"\" draggable=\"false\">';}",
  "function getEquipPixelIconHtml(eq,size){return pixelIconImgHtml(getEquipPixelIconUrl(eq),size||22);}",
  "function getItemPixelIconHtml(itemId,size){return pixelIconImgHtml(getItemPixelIconUrl(itemId),size||22);}",
  "function getEmptySlotPixelIconHtml(slot,size){return pixelIconImgHtml(getEmptySlotPixelIconUrl(slot),size||22);}"
].join('\n');

if (!html.includes('function getEquipPixelIconUrl(')) {
  html = html.replace('function getEquipDisplayName(nameKey)', PIXEL_MODULE + '\nfunction getEquipDisplayName(nameKey)');
}

const oldEquipToString = "function equipToString(eq,full=true){if(!eq)return`<span style=\"color:#555;\">${getEmptySlotDisplay()}</span>`;const c=RARITY_COLORS[eq.rarity]||'#fff';const tag=getEquipSlotLabel(eq.type);const rarityTag=getRarityDisplay(eq.rarity);const upgradeText=eq.upgradeLv?` <span style=\"color:var(--epic);\">+${eq.upgradeLv}</span>`:'';let out=`<span style=\"color:#555;\">[${tag}]</span> <span style=\"color:${c}\">${rarityTag} ${getEquipDisplayName(eq.name)}${upgradeText}</span> <span style=\"color:#666;\">Lv.${eq.level}</span>`;if(full){out+=` <span style=\"color:#555;\">|</span> +${eq.baseValue} ${getEquipStatLabel(eq.baseStat)}`;if(eq.affixes.length===0){out+=` <span style=\"color:#555;\">${getBasicModDisplay()}</span>`;}else{for(let a of eq.affixes){out+=`<br><span style=\"color:#555;\">  - ${getAffixDisplay(a)}</span>`;}}}return out;}";

const newEquipToString = "function equipToString(eq,full=true){if(!eq)return`<span style=\"color:#555;\">${getEmptySlotDisplay()}</span>`;const c=RARITY_COLORS[eq.rarity]||'#fff';const tag=getEquipSlotLabel(eq.type);const rarityTag=getRarityDisplay(eq.rarity);const upgradeText=eq.upgradeLv?` <span style=\"color:var(--epic);\">+${eq.upgradeLv}</span>`:'';const icon=getEquipPixelIconHtml(eq,22);let out=`<span class=\"equip-entry-row\">${icon}<span class=\"equip-entry-text\"><span style=\"color:#555;\">[${tag}]</span> <span style=\"color:${c}\">${rarityTag} ${getEquipDisplayName(eq.name)}${upgradeText}</span> <span style=\"color:#666;\">Lv.${eq.level}</span>`;if(full){out+=` <span style=\"color:#555;\">|</span> +${eq.baseValue} ${getEquipStatLabel(eq.baseStat)}`;if(eq.affixes.length===0){out+=` <span style=\"color:#555;\">${getBasicModDisplay()}</span>`;}else{for(let a of eq.affixes){out+=`<br><span style=\"color:#555;\">  - ${getAffixDisplay(a)}</span>`;}}}out+='</span></span>';return out;}";

if (!html.includes(oldEquipToString)) throw new Error('equipToString not found');
html = html.replace(oldEquipToString, newEquipToString);

const oldEmptySlot = "else div.innerHTML=`<span style=\"color:#555;\">[${getEquipSlotLabel(slotDef.slot)}] ${getEmptySlotDisplay()}</span>`;equipSlots.appendChild(div);}";
const newEmptySlot = "else div.innerHTML=`<span class=\"equip-entry-row\">${getEmptySlotPixelIconHtml(slotDef.slot,22)}<span class=\"equip-entry-text\" style=\"color:#555;\">[${getEquipSlotLabel(slotDef.slot)}] ${getEmptySlotDisplay()}</span></span>`;equipSlots.appendChild(div);}";
if (!html.includes(oldEmptySlot)) throw new Error('empty slot render not found');
html = html.replace(oldEmptySlot, newEmptySlot);

const oldItemToString = "function itemToString(itemId){const nameColor=getItemColor(itemId);return `<b style=\"color:${nameColor}\">${getItemIcon(itemId)} ${getItemName(itemId)}</b> <span style=\"color:#666;\">x${getItemQty(itemId)}</span>`;}";
const newItemToString = "function itemToString(itemId){const nameColor=getItemColor(itemId);return `<span class=\"item-entry-row\">${getItemPixelIconHtml(itemId,22)}<span class=\"item-entry-text\"><b style=\"color:${nameColor}\">${getItemName(itemId)}</b> <span style=\"color:#666;\">x${getItemQty(itemId)}</span></span></span>`;}";
if (!html.includes(oldItemToString)) throw new Error('itemToString not found');
html = html.replace(oldItemToString, newItemToString);

const oldItemDetail = 'let html=`<div style="color:${itemColor};font-size:0.65rem;margin-bottom:0.3rem;">${getItemName(itemId)}</div>`;';
const newItemDetail = 'let html=`<div style="display:flex;align-items:center;gap:8px;margin-bottom:0.3rem;">${pixelIconImgHtml(getItemPixelIconUrl(itemId),32,\' pixel-icon-lg\')}<div style="color:${itemColor};font-size:0.65rem;">${getItemName(itemId)}</div></div>`;';
if (!html.includes(oldItemDetail)) throw new Error('getItemDetailHtml not found');
html = html.replace(oldItemDetail, newItemDetail);

const oldEquipDetailBlock = 'let html=`<div style="color:${c};font-size:${titleFs};margin-bottom:${mbTitle};line-height:1.35;">${rarityTag} ${getEquipDisplayName(eq.name)}${upgradeText} [${tag}]</div><div style="color:#666;font-size:${subFs};">Lv.${eq.level}</div><div style="margin-top:${mtBase};font-size:${bodyFs};"><span style="color:#aaa;">${getEquipStatLabel(eq.baseStat)}: +${eq.baseValue}</span></div><div style="margin-top:${mtAffix};font-size:${bodyFs};">`;';
const newEquipDetailBlock = 'let html=`<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:${mbTitle};">${pixelIconImgHtml(getEquipPixelIconUrl(eq),32,\' pixel-icon-lg\')}<div style="flex:1;min-width:0;"><div style="color:${c};font-size:${titleFs};line-height:1.35;">${rarityTag} ${getEquipDisplayName(eq.name)}${upgradeText} [${tag}]</div><div style="color:#666;font-size:${subFs};">Lv.${eq.level}</div></div></div><div style="margin-top:${mtBase};font-size:${bodyFs};"><span style="color:#aaa;">${getEquipStatLabel(eq.baseStat)}: +${eq.baseValue}</span></div><div style="margin-top:${mtAffix};font-size:${bodyFs};">`;';
if (!html.includes(oldEquipDetailBlock)) throw new Error('getEquipDetailHtml not found');
html = html.replace(oldEquipDetailBlock, newEquipDetailBlock);

// Version bump
html = html.replace("GAME_VERSION='2.24.25'", "GAME_VERSION='2.24.26'");
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.25',date:'2026-06-09',summary:{zh:'v2.24.25 遊戲小助手可生成地城裝備攻略、角色達標分析與各系統攻略。',en:'v2.24.25 assistant strategy guides: dungeon gear, readiness, system tips.'}}",
  "GAME_VERSION_HISTORY=[{version:'2.24.26',date:'2026-06-09',summary:{zh:'v2.24.26 裝備與背包物品新增依名稱/部位生成的像素風圖示。',en:'v2.24.26 procedural pixel icons for equipment and inventory items.'}},{version:'2.24.25',date:'2026-06-09',summary:{zh:'v2.24.25 遊戲小助手可生成地城裝備攻略、角色達標分析與各系統攻略。',en:'v2.24.25 assistant strategy guides: dungeon gear, readiness, system tips.'}}"
);

html = html.replace(
  "logBalanceV22425:'[功能 v2.24.25] 遊戲小助手可生成地城裝備攻略、角色達標分析與強化/合成/天賦等系統攻略。'",
  "logBalanceV22426:'[功能 v2.24.26] 裝備欄與背包物品改為依名稱元素與部位生成的像素風圖示（保留原有稀有度/物品顏色）。',logBalanceV22425:'[功能 v2.24.25] 遊戲小助手可生成地城裝備攻略、角色達標分析與強化/合成/天賦等系統攻略。'"
);

html = html.replace(
  'logBalanceV22425:"[Feature v2.24.25] Game Assistant strategy guides: dungeon gear, readiness, enhance/craft/talent tips."',
  'logBalanceV22426:"[Feature v2.24.26] Procedural pixel icons for gear and inventory (slot/name themed, rarity colors).",logBalanceV22425:"[Feature v2.24.25] Game Assistant strategy guides: dungeon gear, readiness, enhance/craft/talent tips."'
);

fs.writeFileSync(path, html);
console.log('Pixel icon patch applied');
