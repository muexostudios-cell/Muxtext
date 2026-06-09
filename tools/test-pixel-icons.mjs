import fs from 'fs';
import vm from 'vm';

const html = fs.readFileSync('/workspace/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
try { new Function(script); console.log('Script parses OK'); } catch (e) { console.error('Parse error:', e.message); process.exit(1); }

const start = script.indexOf('const PIXEL_ICON_SIZE=16');
const end = script.indexOf('function getEquipDisplayName');
const chunk = script.slice(start, end);

const sandbox = {
  document: {
    documentElement: { appendChild() {}, removeChild() {} },
    createElement() { return { style: {} }; }
  },
  getComputedStyle() { return { color: 'rgb(139, 34, 34)' }; },
  RARITY_COLORS: { hidden: '#8b2222', legendary: '#ff88cc', rare: '#ffff00' },
  WEAPON_SLOTS: ['mainhand', 'offhand'],
  EQUIP_NAME_I18N: { VOID_REAPER: { zh: '虛空收割者', en: 'Void Reaper' }, WIND_BOOTS: { zh: '疾風靴', en: 'Wind Boots' } },
  getEquipDisplayName(nameKey) {
    const m = sandbox.EQUIP_NAME_I18N[nameKey];
    return m ? m.zh : nameKey;
  },
  getItemColor(id) {
    if (id === 'upgradeStoneHidden') return '#8b2222';
    if (id === 'herb_low') return '#44ff44';
    return '#fff';
  }
};

vm.createContext(sandbox);
vm.runInContext(chunk, sandbox);

const eq = { name: 'VOID_REAPER', type: 'boots', rarity: 'hidden' };
const herb = sandbox.getItemPixelIconUrl('herb_low');
const boot = sandbox.getEquipPixelIconUrl(eq);
const voidBoot = sandbox.getEquipPixelIconUrl({ name: 'VOID_REAPER', type: 'mainhand', rarity: 'hidden' });

for (const [label, url] of [['herb', herb], ['void boots', boot], ['void reaper sword', voidBoot]]) {
  if (!url || !url.startsWith('data:image/png')) throw new Error('bad url for ' + label);
  console.log(label, url.slice(0, 40) + '...');
}

console.log('Pixel icon tests passed');
