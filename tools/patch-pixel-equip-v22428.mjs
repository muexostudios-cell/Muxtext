import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const cssOld = '.pixel-icon{display:inline-block;width:22px;height:22px;image-rendering:pixelated;image-rendering:crisp-edges;vertical-align:middle;flex-shrink:0;border:1px solid #222;background:#050505}.pixel-icon-lg{width:32px;height:32px}';
const cssNew = '.pixel-icon{display:inline-block;width:22px;height:22px;image-rendering:pixelated;image-rendering:crisp-edges;vertical-align:middle;flex-shrink:0;border:1px solid #222;background:#050505}.pixel-icon-lg{width:32px;height:32px}.pixel-icon-wrap{position:relative;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;vertical-align:middle;overflow:visible}.pixel-icon-wrap>.pixel-icon{display:block}.pixel-icon-wrap.rarity-legendary>.pixel-icon{border-color:rgba(255,136,204,.55);box-shadow:0 0 4px rgba(255,136,204,.35)}.pixel-icon-wrap.rarity-hidden>.pixel-icon{border-color:rgba(139,34,34,.65);box-shadow:0 0 4px rgba(139,34,34,.4)}.pixel-icon-wrap .pixel-spark{position:absolute;width:2px;height:2px;pointer-events:none;image-rendering:pixelated}.pixel-icon-wrap.rarity-legendary .pixel-spark{background:#ffc8e8;box-shadow:0 0 3px #ff88cc}.pixel-icon-wrap.rarity-hidden .pixel-spark{background:#ff6666;box-shadow:0 0 3px #8b2222}.pixel-icon-wrap.rarity-legendary .pixel-spark.p1{top:-1px;left:2px;animation:pixelSparkA 1.6s ease-in-out infinite}.pixel-icon-wrap.rarity-legendary .pixel-spark.p2{top:3px;right:-1px;animation:pixelSparkB 2.1s ease-in-out infinite .4s}.pixel-icon-wrap.rarity-legendary .pixel-spark.p3{bottom:1px;left:4px;animation:pixelSparkC 1.9s ease-in-out infinite .8s}.pixel-icon-wrap.rarity-hidden .pixel-spark.p1{top:0;right:1px;animation:pixelSparkB 1.7s ease-in-out infinite}.pixel-icon-wrap.rarity-hidden .pixel-spark.p2{bottom:0;left:1px;animation:pixelSparkA 2.2s ease-in-out infinite .5s}.pixel-icon-wrap.rarity-hidden .pixel-spark.p3{top:5px;left:-1px;animation:pixelSparkC 1.8s ease-in-out infinite .9s}@keyframes pixelSparkA{0%,100%{opacity:.15;transform:translate(0,0)}50%{opacity:1;transform:translate(1px,-2px)}}@keyframes pixelSparkB{0%,100%{opacity:.2;transform:translate(0,0) scale(1)}50%{opacity:1;transform:translate(-1px,1px) scale(1.2)}}@keyframes pixelSparkC{0%,100%{opacity:.1;transform:translate(0,0)}50%{opacity:.95;transform:translate(2px,-1px)}}';

if (!html.includes(cssOld)) throw new Error('CSS block not found');
html = html.replace(cssOld, cssNew);

const parseWeaponKindFn = `function parseWeaponKind(nameKey,displayName){const s=(String(nameKey||'')+' '+String(displayName||'')).toLowerCase();if(/gun|plasma|sidearm|槍|光槍/.test(s)&&!/shield|盾|field|力場/.test(s))return'gun';if(/buckler|shield|盾|field|力場|emitter/.test(s))return'shield';if(/hammer|鎚|axe|斧|cleaver/.test(s))return'hammer';if(/dagger|刀|shiv|shuriken|飛刃|hatchet|手斧/.test(s))return'dagger';if(/knuckle|拳|fist|gauntlet|指虎/.test(s))return'fist';if(/reaper|scythe|收割/.test(s))return'scythe';return'sword';}`;
const drawRarityParticlePixelsFn = `function drawRarityParticlePixels(grid,rarity,seed){if(rarity!=='legendary'&&rarity!=='hidden')return;const col=rarity==='legendary'?[255,180,220,255]:[210,70,70,255];const pts=[[1,1],[14,2],[2,14],[13,13],[0,7],[15,8],[7,0],[8,15]];for(let i=0;i<4;i++){const p=pts[(seed+i)%pts.length];setGridPx(grid,p[0],p[1],col);if(p[0]>0)setGridPx(grid,p[0]-1,p[1],[col[0],col[1],col[2],150]);}}`;

const drawHerbSyringeFn = `function drawHerbSyringePixels(grid,id,mainRgba,hi,lo){const needle=[200,205,215,255],glass=[230,235,245,90],rubber=[lo.r,lo.g,lo.b,255];if(id==='herb_low'){fillGridRect(grid,7,2,2,2,rubber);fillGridRect(grid,6,4,4,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,6,5,4,5,mainRgba);fillGridRect(grid,7,6,2,3,glass);fillGridRect(grid,6,10,4,1,rubber);fillGridRect(grid,5,11,6,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,8,12,1,3,needle);setGridPx(grid,8,15,needle);}else if(id==='herb_mid'){fillGridRect(grid,6,1,4,2,rubber);fillGridRect(grid,5,3,6,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,5,4,6,6,mainRgba);fillGridRect(grid,6,5,4,4,glass);fillGridRect(grid,5,10,6,1,rubber);fillGridRect(grid,4,11,8,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,7,12,2,3,needle);setGridPx(grid,7,15,needle);setGridPx(grid,5,6,[lo.r,lo.g,lo.b,220]);setGridPx(grid,10,6,[lo.r,lo.g,lo.b,220]);setGridPx(grid,5,8,[lo.r,lo.g,lo.b,220]);setGridPx(grid,10,8,[lo.r,lo.g,lo.b,220]);}else{fillGridRect(grid,5,1,6,2,rubber);fillGridRect(grid,4,3,8,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,4,4,8,7,mainRgba);fillGridRect(grid,5,5,6,5,glass);fillGridRect(grid,4,11,8,1,rubber);fillGridRect(grid,3,12,10,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,7,13,2,2,needle);setGridPx(grid,6,12,needle);setGridPx(grid,9,12,needle);setGridPx(grid,7,15,needle);setGridPx(grid,8,15,needle);fillGridRect(grid,5,7,6,1,mainRgba);fillGridRect(grid,5,9,6,1,mainRgba);setGridPx(grid,7,4,[255,255,255,220]);}}`;

const drawEquipFn = `function drawEquipPixels(grid,slot,nameKey,colorHex,seed,rarity){const disp=typeof getEquipDisplayName==='function'?getEquipDisplayName(nameKey):nameKey;const themes=parseNameThemes(nameKey,disp);const kind=parseWeaponKind(nameKey,disp);const main=hexToRgb(colorHex);const mainRgba=[main.r,main.g,main.b,255];const hi=hexToRgb(shadeColor(colorHex,0.32));const lo=hexToRgb(shadeColor(colorHex,-0.38));const bg=[6,6,10,255];const accent=themes.void?[130,50,170,255]:themes.fire?[255,110,50,255]:themes.ice?[120,200,255,255]:themes.energy?[70,220,255,255]:themes.shadow?[70,70,100,255]:[hi.r,hi.g,hi.b,255];fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,bg);if(slot==='mainhand'){if(kind==='gun'){fillGridRect(grid,2,6,10,2,mainRgba);fillGridRect(grid,3,5,8,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,2,8,3,4,lo);setGridPx(grid,5,8,lo);fillGridRect(grid,11,6,3,2,[lo.r,lo.g,lo.b,255]);setGridPx(grid,14,6,accent);}else if(kind==='hammer'){fillGridRect(grid,3,4,8,3,mainRgba);fillGridRect(grid,4,3,6,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,7,7,2,7,lo);setGridPx(grid,7,14,lo);}else if(kind==='scythe'){for(let i=0;i<8;i++){setGridPx(grid,8-i,2+i,mainRgba);setGridPx(grid,9-i,2+i,[hi.r,hi.g,hi.b,255]);}fillGridRect(grid,8,10,2,4,lo);setGridPx(grid,6,4,accent);}else{const bx=7;for(let i=0;i<9;i++){setGridPx(grid,bx,2+i,mainRgba);setGridPx(grid,bx+1,2+i,[hi.r,hi.g,hi.b,255]);}setGridPx(grid,bx,1,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,bx-1,11,3,1,lo);fillGridRect(grid,bx,12,2,3,lo);setGridPx(grid,bx,15,accent);}}else if(slot==='offhand'){if(kind==='shield'){fillGridRect(grid,5,3,6,8,mainRgba);fillGridRect(grid,6,4,4,6,[hi.r,hi.g,hi.b,255]);setGridPx(grid,7,2,mainRgba);setGridPx(grid,8,2,mainRgba);fillGridRect(grid,6,11,4,2,lo);setGridPx(grid,7,6,lo);setGridPx(grid,8,6,lo);}else if(kind==='gun'){fillGridRect(grid,3,7,8,2,mainRgba);fillGridRect(grid,4,6,6,1,hi);fillGridRect(grid,3,9,2,3,lo);setGridPx(grid,10,7,accent);}else if(kind==='fist'){fillGridRect(grid,4,6,8,4,mainRgba);fillGridRect(grid,5,5,6,1,[hi.r,hi.g,hi.b,255]);setGridPx(grid,4,8,lo);setGridPx(grid,11,8,lo);setGridPx(grid,5,10,lo);setGridPx(grid,10,10,lo);}else{fillGridRect(grid,7,3,1,6,mainRgba);fillGridRect(grid,6,9,3,1,lo);fillGridRect(grid,7,10,2,3,lo);setGridPx(grid,7,2,[hi.r,hi.g,hi.b,255]);}}else if(slot==='armor'){fillGridRect(grid,5,2,6,3,mainRgba);fillGridRect(grid,4,4,8,2,mainRgba);setGridPx(grid,6,5,[18,18,26,255]);setGridPx(grid,9,5,[18,18,26,255]);fillGridRect(grid,4,6,8,5,mainRgba);fillGridRect(grid,5,7,6,3,[hi.r,hi.g,hi.b,255]);if(themes.heavy){fillGridRect(grid,3,7,1,4,lo);fillGridRect(grid,12,7,1,4,lo);}setGridPx(grid,7,3,accent);}else if(slot==='armguard'){fillGridRect(grid,3,5,10,4,mainRgba);fillGridRect(grid,4,6,8,2,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,2,5,1,4,lo);fillGridRect(grid,13,5,1,4,lo);if(themes.energy)for(let x=4;x<12;x+=2)setGridPx(grid,x,4,accent);}else if(slot==='legguard'){fillGridRect(grid,4,3,3,9,mainRgba);fillGridRect(grid,9,3,3,9,mainRgba);fillGridRect(grid,5,4,1,7,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,10,4,1,7,[hi.r,hi.g,hi.b,255]);fillGridRect(grid,4,6,3,2,lo);fillGridRect(grid,9,6,3,2,lo);fillGridRect(grid,5,11,2,2,lo);fillGridRect(grid,10,11,2,2,lo);}else if(slot==='boots'){fillGridRect(grid,4,5,4,5,mainRgba);fillGridRect(grid,3,10,6,3,lo);fillGridRect(grid,3,12,7,1,[hi.r,hi.g,hi.b,255]);setGridPx(grid,4,7,[hi.r,hi.g,hi.b,255]);if(themes.swift)for(let x=1;x<4;x++)setGridPx(grid,x,13,accent);}drawRarityParticlePixels(grid,rarity,seed);if(seed%3===0&&!rarity)setGridPx(grid,1,1,accent);if(seed%5===0&&!rarity)setGridPx(grid,14,13,accent);}`;

const drawEmptyFn = `function drawEmptySlotPixels(grid,slot){const bg=[6,6,10,255],ghost=[40,40,48,120];fillGridRect(grid,0,0,PIXEL_ICON_SIZE,PIXEL_ICON_SIZE,bg);if(slot==='mainhand'){for(let y=3;y<11;y++){setGridPx(grid,7,y,ghost);setGridPx(grid,8,y,ghost);}fillGridRect(grid,6,11,3,1,ghost);fillGridRect(grid,7,12,2,3,ghost);}else if(slot==='offhand'){fillGridRect(grid,5,4,6,7,ghost);setGridPx(grid,7,3,ghost);setGridPx(grid,8,3,ghost);}else if(slot==='armor'){fillGridRect(grid,5,3,6,2,ghost);fillGridRect(grid,4,5,8,5,ghost);}else if(slot==='armguard')fillGridRect(grid,3,6,10,3,ghost);else if(slot==='legguard'){fillGridRect(grid,4,4,3,9,ghost);fillGridRect(grid,9,4,3,9,ghost);}else if(slot==='boots'){fillGridRect(grid,4,6,4,5,ghost);fillGridRect(grid,3,11,6,2,ghost);}else fillGridRect(grid,6,6,4,4,ghost);}`;

const pixelIconImgFn = `function pixelIconImgHtml(url,size,cls,rarity){if(!url)return'';const px=size||22;const extra=cls?' '+cls:'';const img='<img class="pixel-icon'+extra+'" src="'+url+'" width="'+px+'" height="'+px+'" alt="" draggable="false">';if(rarity==='legendary'||rarity==='hidden')return'<span class="pixel-icon-wrap rarity-'+rarity+'" style="width:'+px+'px;height:'+px+'px">'+img+'<span class="pixel-spark p1"></span><span class="pixel-spark p2"></span><span class="pixel-spark p3"></span></span>';return img;}`;
const getEquipPixelIconHtmlFn = `function getEquipPixelIconHtml(eq,size){return pixelIconImgHtml(getEquipPixelIconUrl(eq),size||22,'',eq&&eq.rarity);}`;
const getEquipPixelIconUrlFn = `function getEquipPixelIconUrl(eq){if(!eq)return'';const color=resolvePixelColor((typeof RARITY_COLORS!=='undefined'&&RARITY_COLORS[eq.rarity])||'#fff');const seed=hashStr((eq.name||'')+'|'+(eq.type||'')+'|'+eq.rarity);const key='eq|'+(eq.name||'')+'|'+(eq.type||'')+'|'+eq.rarity+'|'+color;return getCachedPixelIcon(key,g=>drawEquipPixels(g,eq.type||'mainhand',eq.name,color,seed,eq.rarity));}`;

function replaceFn(name, nextName, newBody) {
  const start = `function ${name}(`;
  const end = `function ${nextName}(`;
  const i = html.indexOf(start);
  const j = html.indexOf(end, i + start.length);
  if (i < 0 || j < 0) throw new Error(`Function ${name} not found (next: ${nextName})`);
  html = html.slice(0, i) + newBody + html.slice(j);
}

// Insert parseWeaponKind and drawRarityParticlePixels before drawEquipPixels
if (!html.includes('function parseWeaponKind')) {
  html = html.replace(
    'function drawEquipPixels(',
    parseWeaponKindFn + drawRarityParticlePixelsFn + 'function drawEquipPixels('
  );
}

replaceFn('drawEquipPixels', 'drawHerbSyringePixels', drawEquipFn);
replaceFn('drawHerbSyringePixels', 'drawDecoderKeyPixels', drawHerbSyringeFn);
replaceFn('drawEmptySlotPixels', 'getEquipPixelIconUrl', drawEmptyFn);
replaceFn('pixelIconImgHtml', 'getEquipPixelIconHtml', pixelIconImgFn);
replaceFn('getEquipPixelIconHtml', 'getItemPixelIconHtml', getEquipPixelIconHtmlFn);
replaceFn('getEquipPixelIconUrl', 'getItemPixelIconUrl', getEquipPixelIconUrlFn);

// getEquipDetailHtml: pass rarity to pixelIconImgHtml
html = html.replace(
  "pixelIconImgHtml(getEquipPixelIconUrl(eq),32,' pixel-icon-lg')",
  "pixelIconImgHtml(getEquipPixelIconUrl(eq),32,' pixel-icon-lg',eq.rarity)"
);

// Version bump
html = html.replace(/GAME_VERSION='2\.24\.27'/, "GAME_VERSION='2.24.28'");
html = html.replace(
  "logBalanceV22427:'[功能 v2.24.27] 三種回復針劑改為專屬像素針筒圖示；高級武器箱破解器改為像素鎖匙圖示。',logBalanceV22426:",
  "logBalanceV22428:'[功能 v2.24.28] 裝備像素圖依部位重繪（劍/槍/盾/頭盔甲/護腿/鞋）；三種針劑針筒更逼真；傳說與隱藏裝備加入粒子光效。',logBalanceV22427:'[功能 v2.24.27] 三種回復針劑改為專屬像素針筒圖示；高級武器箱破解器改為像素鎖匙圖示。',logBalanceV22426:"
);
html = html.replace(
  "logBalanceV22427:'[Feature v2.24.27] Distinct pixel syringes and decoder key icon.',logBalanceV22426:",
  "logBalanceV22428:'[Feature v2.24.28] Slot-based equip pixel art (sword/gun/shield/helm/legs/boots); sharper syringes; legendary/hidden particle FX.',logBalanceV22427:'[Feature v2.24.27] Distinct pixel syringes and decoder key icon.',logBalanceV22426:"
);
html = html.replace(
  "GAME_VERSION_HISTORY=[{version:'2.24.27'",
  "GAME_VERSION_HISTORY=[{version:'2.24.28',date:'2026-06-09',summary:{zh:'v2.24.28 裝備依部位重繪像素圖；針劑針筒優化；傳說/隱藏粒子光效。',en:'v2.24.28 slot-based equip pixels, syringe polish, legendary/hidden particles.'}},{version:'2.24.27'"
);

fs.writeFileSync(path, html);
console.log('Patched index.html for v2.24.28');
