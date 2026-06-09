import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const cssOld = '.pixel-icon-wrap.rarity-hidden .pixel-spark.p3{top:5px;left:-1px;animation:pixelSparkC 1.8s ease-in-out infinite .9s}@keyframes pixelSparkA';
const cssNew = '.pixel-icon-wrap.rarity-hidden .pixel-spark.p3{top:5px;left:-1px;animation:pixelSparkC 1.8s ease-in-out infinite .9s}.pixel-icon-wrap.rarity-legendary .pixel-spark.p4{bottom:-1px;right:3px;animation:pixelSparkA 2.3s ease-in-out infinite 1.1s}.pixel-icon-wrap.rarity-hidden .pixel-spark.p4{top:2px;left:6px;animation:pixelSparkB 2s ease-in-out infinite 1.2s}.pixel-icon-wrap.rarity-legendary::before,.pixel-icon-wrap.rarity-hidden::before{content:"";position:absolute;inset:-3px;border-radius:2px;pointer-events:none;animation:pixelAura 2.4s ease-in-out infinite}.pixel-icon-wrap.rarity-legendary::before{box-shadow:0 0 6px 1px rgba(255,136,204,.45)}.pixel-icon-wrap.rarity-hidden::before{box-shadow:0 0 6px 1px rgba(139,34,34,.5)}@keyframes pixelAura{0%,100%{opacity:.35}50%{opacity:.9}}@keyframes pixelSparkA';

if (!html.includes(cssOld)) throw new Error('Particle CSS anchor not found');
html = html.replace(cssOld, cssNew);

const drawCrystalFns = `function drawSpaceCrystalPixels(grid,mainRgba,hi,lo){const core=[210,255,255,255],spark=[255,255,255,220];setGridPx(grid,8,2,spark);setGridPx(grid,7,3,mainRgba);setGridPx(grid,8,3,[hi.r,hi.g,hi.b,255]);setGridPx(grid,9,3,mainRgba);fillGridRect(grid,6,4,5,1,mainRgba);fillGridRect(grid,5,5,7,2,mainRgba);fillGridRect(grid,4,7,9,3,mainRgba);fillGridRect(grid,5,8,7,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,5,10,7,2,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,6,12,5,1,[lo.r,lo.g,lo.b,255]);setGridPx(grid,8,13,[lo.r,lo.g,lo.b,255]);setGridPx(grid,5,6,[lo.r,lo.g,lo.b,255]);setGridPx(grid,4,8,[lo.r,lo.g,lo.b,255]);setGridPx(grid,10,6,[hi.r,hi.g,hi.b,255]);setGridPx(grid,11,8,[hi.r,hi.g,hi.b,255]);setGridPx(grid,8,7,core);setGridPx(grid,7,8,core);setGridPx(grid,8,8,[255,255,255,255]);setGridPx(grid,9,8,core);setGridPx(grid,6,3,spark);setGridPx(grid,10,5,[180,255,255,180]);setGridPx(grid,3,9,[hi.r,hi.g,hi.b,140]);setGridPx(grid,12,10,[hi.r,hi.g,hi.b,140]);}function drawItemBagStonePixels(grid,mainRgba,hi,lo){fillGridRect(grid,4,5,8,7,mainRgba);fillGridRect(grid,5,4,6,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,6,7,4,3,[lo.r,lo.g,lo.b,255]);setGridPx(grid,5,6,hi);setGridPx(grid,10,6,hi);fillGridRect(grid,7,11,2,2,lo);}`;

if (!html.includes('function drawSpaceCrystalPixels')) {
  html = html.replace('function drawItemPixels(', drawCrystalFns + 'function drawItemPixels(');
}

const drawItemOld = "}else if(id==='spaceStone'||id==='itemBagStone'){fillGridRect(grid,4,6,8,6,[lo.r,lo.g,lo.b,255]);fillGridRect(grid,5,5,6,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,6,7,4,3,mainRgba);}else if(id==='encryptedWeaponCrate')";
const drawItemNew = "}else if(id==='spaceStone'){drawSpaceCrystalPixels(grid,mainRgba,hi,lo);}else if(id==='itemBagStone'){drawItemBagStonePixels(grid,mainRgba,hi,lo);}else if(id==='encryptedWeaponCrate')";
if (!html.includes(drawItemOld)) throw new Error('drawItemPixels spaceStone branch not found');
html = html.replace(drawItemOld, drawItemNew);

const rarityParticlesOld = "function drawRarityParticlePixels(grid,rarity,seed){if(rarity!=='legendary'&&rarity!=='hidden')return;const col=rarity==='legendary'?[255,180,220,255]:[210,70,70,255];const pts=[[1,1],[14,2],[2,14],[13,13],[0,7],[15,8],[7,0],[8,15]];for(let i=0;i<4;i++){const p=pts[(seed+i)%pts.length];setGridPx(grid,p[0],p[1],col);if(p[0]>0)setGridPx(grid,p[0]-1,p[1],[col[0],col[1],col[2],150]);}}";
const rarityParticlesNew = "function drawRarityParticlePixels(grid,rarity,seed){if(rarity!=='legendary'&&rarity!=='hidden')return;const col=rarity==='legendary'?[255,180,220,255]:[230,80,80,255];const dim=rarity==='legendary'?[255,120,200,120]:[180,40,40,120];const pts=[[1,1],[14,2],[2,14],[13,13],[0,7],[15,8],[7,0],[8,15],[3,5],[12,11]];for(let i=0;i<6;i++){const p=pts[(seed+i)%pts.length];setGridPx(grid,p[0],p[1],col);if(p[0]>0)setGridPx(grid,p[0]-1,p[1],dim);if(p[1]>0)setGridPx(grid,p[0],p[1]-1,dim);}}";
if (!html.includes(rarityParticlesOld)) throw new Error('drawRarityParticlePixels not found');
html = html.replace(rarityParticlesOld, rarityParticlesNew);

const pixelIconOld = "if(rarity==='legendary'||rarity==='hidden')return'<span class=\"pixel-icon-wrap rarity-'+rarity+'\" style=\"width:'+px+'px;height:'+px+'px\">'+img+'<span class=\"pixel-spark p1\"></span><span class=\"pixel-spark p2\"></span><span class=\"pixel-spark p3\"></span></span>';";
const pixelIconNew = "if(rarity==='legendary'||rarity==='hidden')return'<span class=\"pixel-icon-wrap rarity-'+rarity+'\" style=\"width:'+px+'px;height:'+px+'px\">'+img+'<span class=\"pixel-spark p1\"></span><span class=\"pixel-spark p2\"></span><span class=\"pixel-spark p3\"></span><span class=\"pixel-spark p4\"></span></span>';";
if (!html.includes(pixelIconOld)) throw new Error('pixelIconImgHtml wrap not found');
html = html.replace(pixelIconOld, pixelIconNew);

const colorOld = "if(itemId==='advancedEquipFragment')return 'var(--chip)';";
const colorNew = "if(itemId==='spaceStone')return 'var(--chip)';if(itemId==='advancedEquipFragment')return 'var(--chip)';";
if (!html.includes(colorOld)) throw new Error('getItemColor anchor not found');
html = html.replace(colorOld, colorNew);

html = html.replace(/GAME_VERSION='2\.24\.28'/, "GAME_VERSION='2.24.29'");
html = html.replace(
  "logBalanceV22428:'[功能 v2.24.28] 裝備像素圖依部位重繪（劍/槍/盾/頭盔甲/護腿/鞋）；三種針劑針筒更逼真；傳說與隱藏裝備加入粒子光效。',logBalanceV22427:",
  "logBalanceV22429:'[功能 v2.24.29] 空間石改為像素晶體圖示；傳說與隱藏裝備粒子光效加強（光暈與更多光點）。',logBalanceV22428:'[功能 v2.24.28] 裝備像素圖依部位重繪（劍/槍/盾/頭盔甲/護腿/鞋）；三種針劑針筒更逼真；傳說與隱藏裝備加入粒子光效。',logBalanceV22427:"
);
html = html.replace(
  "logBalanceV22428:'[Feature v2.24.28] Slot-based equip pixel art (sword/gun/shield/helm/legs/boots); sharper syringes; legendary/hidden particle FX.',logBalanceV22427:",
  "logBalanceV22429:'[Feature v2.24.29] Space stone pixel crystal icon; stronger legendary/hidden particle aura.',logBalanceV22428:'[Feature v2.24.28] Slot-based equip pixel art (sword/gun/shield/helm/legs/boots); sharper syringes; legendary/hidden particle FX.',logBalanceV22427:"
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.28'",
  "GAME_VERSION_HISTORY=[{version:'2.24.29',date:'2026-06-09',summary:{zh:'v2.24.29 空間石像素晶體；傳說/隱藏粒子光效加強。',en:'v2.24.29 space stone crystal; stronger legendary/hidden particles.'}},{version:'2.24.28'"
);

fs.writeFileSync(path, html);
console.log('Patched index.html for v2.24.29');
