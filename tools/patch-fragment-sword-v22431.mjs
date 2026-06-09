import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const helpers = `function getItemIconRarity(itemId){if(itemId==='legendaryEquipFragment')return'legendary';if(itemId==='hiddenEquipFragment')return'hidden';return'';}function drawEquipFragmentPixels(grid,itemId,mainRgba,hi,lo){const chip=[48,48,56,255];setGridPx(grid,5,2,[hi.r,hi.g,hi.b,255]);setGridPx(grid,6,2,mainRgba);setGridPx(grid,6,3,mainRgba);setGridPx(grid,7,3,mainRgba);setGridPx(grid,7,4,mainRgba);setGridPx(grid,8,4,[hi.r,hi.g,hi.b,255]);setGridPx(grid,8,5,chip);setGridPx(grid,9,5,chip);setGridPx(grid,7,5,[lo.r,lo.g,lo.b,255]);setGridPx(grid,8,6,mainRgba);setGridPx(grid,9,6,[hi.r,hi.g,hi.b,255]);setGridPx(grid,9,7,mainRgba);fillGridRect(grid,6,8,5,1,lo);fillGridRect(grid,7,9,2,5,lo);setGridPx(grid,7,14,lo);setGridPx(grid,4,5,[hi.r,hi.g,hi.b,160]);setGridPx(grid,10,4,[lo.r,lo.g,lo.b,160]);const rarity=getItemIconRarity(itemId);if(rarity)drawRarityParticlePixels(grid,rarity,hashStr(itemId));}`;

if (!html.includes('function getItemIconRarity')) {
  html = html.replace('function drawItemPixels(', helpers + 'function drawItemPixels(');
}

const fragOld = "}else if(id.includes('Fragment')||id==='equipFragment'){setGridPx(grid,5,4,mainRgba);setGridPx(grid,6,5,mainRgba);setGridPx(grid,7,6,mainRgba);setGridPx(grid,8,7,mainRgba);setGridPx(grid,7,8,[hi.r,hi.g,hi.b,255]);setGridPx(grid,6,9,lo.r!=null?[lo.r,lo.g,lo.b,255]:mainRgba);setGridPx(grid,9,5,[hi.r,hi.g,hi.b,255]);}else if(id==='hellTicket')";
const fragNew = "}else if(id.includes('Fragment')||id==='equipFragment'){drawEquipFragmentPixels(grid,id,mainRgba,hi,lo);}else if(id==='hellTicket')";
if (!html.includes(fragOld)) throw new Error('fragment branch not found');
html = html.replace(fragOld, fragNew);

const itemHtmlOld = 'function getItemPixelIconHtml(itemId,size){return pixelIconImgHtml(getItemPixelIconUrl(itemId),size||22);}';
const itemHtmlNew = 'function getItemPixelIconHtml(itemId,size){return pixelIconImgHtml(getItemPixelIconUrl(itemId),size||22,\'\',getItemIconRarity(itemId));}';
if (!html.includes(itemHtmlOld)) throw new Error('getItemPixelIconHtml not found');
html = html.replace(itemHtmlOld, itemHtmlNew);

const detailOld = "pixelIconImgHtml(getItemPixelIconUrl(itemId),32,' pixel-icon-lg')";
const detailNew = "pixelIconImgHtml(getItemPixelIconUrl(itemId),32,' pixel-icon-lg',getItemIconRarity(itemId))";
if (!html.includes(detailOld)) throw new Error('getItemDetailHtml icon not found');
html = html.replace(detailOld, detailNew);

html = html.replace(/GAME_VERSION='2\.24\.30'/, "GAME_VERSION='2.24.31'");
html = html.replace(
  "logBalanceV22430:'[功能 v2.24.30] 背包空間石與裝備背包空間石統一為藍色像素晶體圖示。',logBalanceV22429:",
  "logBalanceV22431:'[功能 v2.24.31] 裝備碎片改為像素斷劍圖示；傳說與隱藏裝備碎片加入粒子光效。',logBalanceV22430:'[功能 v2.24.30] 背包空間石與裝備背包空間石統一為藍色像素晶體圖示。',logBalanceV22429:"
);
html = html.replace(
  "logBalanceV22430:'[Feature v2.24.30] Item bag space stone matches equip bag crystal icon in blue.',logBalanceV22429:",
  "logBalanceV22431:'[Feature v2.24.31] Equip fragments as broken-sword pixels; legendary/hidden fragment particles.',logBalanceV22430:'[Feature v2.24.30] Item bag space stone matches equip bag crystal icon in blue.',logBalanceV22429:"
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.30'",
  "GAME_VERSION_HISTORY=[{version:'2.24.31',date:'2026-06-09',summary:{zh:'v2.24.31 裝備碎片斷劍像素圖；傳說/隱藏碎片粒子光效。',en:'v2.24.31 broken-sword fragment icons; legendary/hidden particles.'}},{version:'2.24.30'"
);

fs.writeFileSync(path, html);
console.log('Patched index.html for v2.24.31');
