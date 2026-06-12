import fs from 'fs';

const path = '/workspace/index.html';
let html = fs.readFileSync(path, 'utf8');

const fixes = [];
const required = [];

const add = (oldStr, newStr, label, opt = false) => {
  (opt ? fixes : required).push({ oldStr, newStr, label });
};

// Fix 1: Add image-rendering CSS for combat portraits
add(
  '#combat-dock .combat-slot-btn{flex:1 1 0;width:auto;min-width:0;min-height:46px}',
  '#combat-dock .combat-slot-btn{flex:1 1 0;width:auto;min-width:0;min-height:46px}' +
  '#player-portrait .pixel-icon,#enemy-portrait .pixel-icon{image-rendering:pixelated;image-rendering:crisp-edges}',
  'combat portrait image-rendering'
);

// Fix 2: Improve gridToCombatDataUrl to ensure pixelated rendering
add(
  "function gridToCombatDataUrl(grid){const S=PIXEL_ICON_SIZE,O=S*COMBAT_PORTRAIT_SCALE,c=document.createElement('canvas');c.width=O;c.height=O;const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;const t=document.createElement('canvas');t.width=S;t.height=S;const tc=t.getContext('2d');const img=tc.createImageData(S,S);img.data.set(grid);tc.putImageData(img,0,0);ctx.drawImage(t,0,0,O,O);return c.toDataURL('image/png');}",
  "function gridToCombatDataUrl(grid){const S=PIXEL_ICON_SIZE,O=S*COMBAT_PORTRAIT_SCALE,c=document.createElement('canvas');c.width=O;c.height=O;const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.webkitImageSmoothingEnabled=false;ctx.msImageSmoothingEnabled=false;const t=document.createElement('canvas');t.width=S;t.height=S;const tc=t.getContext('2d');tc.imageSmoothingEnabled=false;const img=tc.createImageData(S,S);img.data.set(grid);tc.putImageData(img,0,0);ctx.drawImage(t,0,0,O,O);return c.toDataURL('image/png');}",
  'gridToCombatDataUrl image smoothing fix'
);

// Fix 3: Also improve gridToDataUrl for consistency
add(
  "function gridToDataUrl(grid){const c=document.createElement('canvas');c.width=PIXEL_ICON_SIZE;c.height=PIXEL_ICON_SIZE;const ctx=c.getContext('2d');const img=ctx.createImageData(PIXEL_ICON_SIZE,PIXEL_ICON_SIZE);img.data.set(grid);ctx.putImageData(img,0,0);return c.toDataURL('image/png');}",
  "function gridToDataUrl(grid){const c=document.createElement('canvas');c.width=PIXEL_ICON_SIZE;c.height=PIXEL_ICON_SIZE;const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.webkitImageSmoothingEnabled=false;ctx.msImageSmoothingEnabled=false;const img=ctx.createImageData(PIXEL_ICON_SIZE,PIXEL_ICON_SIZE);img.data.set(grid);ctx.putImageData(img,0,0);return c.toDataURL('image/png');}",
  'gridToDataUrl image smoothing fix'
);

// Fix 4: Add wrapper styling for pixel icon containers in combat
add(
  '#player-portrait .pixel-icon-wrap,#enemy-portrait .pixel-icon-wrap{display:block;margin:0 auto}',
  '#player-portrait .pixel-icon-wrap,#enemy-portrait .pixel-icon-wrap{display:block;margin:0 auto;image-rendering:pixelated;image-rendering:crisp-edges}#player-portrait .pixel-icon,#enemy-portrait .pixel-icon{image-rendering:pixelated;image-rendering:crisp-edges;filter:none}',
  'combat portrait wrapper styling',
  true
);

// Fix 5: Version bump
add("GAME_VERSION='2.24.61'", "GAME_VERSION='2.24.62'", 'version');
add(
  "GAME_VERSION_HISTORY=[{version:'2.24.61'",
  "GAME_VERSION_HISTORY=[{version:'2.24.62',date:'2026-06-12',summary:{zh:'v2.24.62 修復戰鬥畫面像素圖示渲染異常；禁用 Canvas 圖像平滑，確保像素風格清晰。',en:'v2.24.62 Fixed combat pixel icon rendering; disabled canvas image smoothing for crisp pixels.'}},{version:'2.24.61'",
  'changelog'
);

let failed = 0;
for (const { oldStr, newStr, label } of required) {
  if (!html.includes(oldStr)) {
    console.error('FAIL required:', label);
    failed++;
    continue;
  }
  html = html.replace(oldStr, newStr);
  console.log('✓ OK', label);
}
for (const { oldStr, newStr, label } of fixes) {
  if (!html.includes(oldStr)) {
    console.log('⊘ SKIP optional:', label);
    continue;
  }
  html = html.replace(oldStr, newStr);
  console.log('✓ OK optional', label);
}

if (failed) {
  console.error(failed, 'required replacements failed');
  process.exit(1);
}

// Validate JS syntax
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
try {
  new Function(html.slice(start, end));
  console.log('✓ JS syntax OK');
} catch (e) {
  console.error('✗ JS syntax FAIL', e.message);
  process.exit(1);
}

fs.writeFileSync(path, html);
fs.writeFileSync('/workspace/version.json', JSON.stringify({ version: '2.24.62', updated: '2026-06-12' }, null, 2) + '\n');
console.log('✓ Written. Patched to v2.24.62 - pixel icon rendering fix');
