import fs from 'fs';
import vm from 'vm';

const html = fs.readFileSync('/workspace/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
try { new Function(script); console.log('Script parses OK'); } catch (e) { console.error('Parse error:', e.message); process.exit(1); }

const start = script.indexOf('const PIXEL_ICON_SIZE=16');
const end = script.indexOf('function getEquipDisplayName');
const chunk = script.slice(start, end);

function mockCanvas() {
  const data = new Uint8ClampedArray(16 * 16 * 4);
  return {
    width: 16,
    height: 16,
    getContext() {
      return {
        createImageData(w, h) { return { data: new Uint8ClampedArray(w * h * 4), width: w, height: h }; },
        putImageData(img) { data.set(img.data); }
      };
    },
    toDataURL() { return 'data:image/png;base64,test'; }
  };
}

const sandbox = {
  document: {
    documentElement: { appendChild() {}, removeChild() {} },
    createElement() { return mockCanvas(); }
  },
  getComputedStyle() { return { color: 'rgb(139, 34, 34)' }; },
  RARITY_COLORS: { hidden: '#8b2222', legendary: '#ff88cc', rare: '#ffff00' },
  WEAPON_SLOTS: ['mainhand', 'offhand'],
  EQUIP_NAME_I18N: {
    VOID_REAPER: { zh: '虛空收割者', en: 'Void Reaper' },
    WIND_BOOTS: { zh: '疾風靴', en: 'Wind Boots' },
    PLASMA_GUN: { zh: '等離子側槍', en: 'Plasma Sidearm' },
    BUCKLER: { zh: '脈衝圓盾', en: 'Pulse Buckler' },
    IRON_PLATE: { zh: '裝甲板外骨骼', en: 'Plated Exosuit' }
  },
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

const cases = [
  ['herb_low', () => sandbox.getItemPixelIconUrl('herb_low')],
  ['herb_mid', () => sandbox.getItemPixelIconUrl('herb_mid')],
  ['herb_high', () => sandbox.getItemPixelIconUrl('herb_high')],
  ['hidden boots', () => sandbox.getEquipPixelIconUrl({ name: 'VOID_REAPER', type: 'boots', rarity: 'hidden' })],
  ['hidden scythe', () => sandbox.getEquipPixelIconUrl({ name: 'VOID_REAPER', type: 'mainhand', rarity: 'hidden' })],
  ['plasma gun', () => sandbox.getEquipPixelIconUrl({ name: 'PLASMA_GUN', type: 'mainhand', rarity: 'rare' })],
  ['buckler shield', () => sandbox.getEquipPixelIconUrl({ name: 'BUCKLER', type: 'offhand', rarity: 'rare' })],
  ['iron plate armor', () => sandbox.getEquipPixelIconUrl({ name: 'IRON_PLATE', type: 'armor', rarity: 'epic' })],
  ['space stone crystal', () => sandbox.getItemPixelIconUrl('spaceStone')],
  ['item bag stone crystal', () => sandbox.getItemPixelIconUrl('itemBagStone')]
];

const spaceUrl = sandbox.getItemPixelIconUrl('spaceStone');
const bagUrl = sandbox.getItemPixelIconUrl('itemBagStone');
if (spaceUrl !== bagUrl) throw new Error('spaceStone and itemBagStone icons should match');

for (const [label, fn] of cases) {
  const url = fn();
  if (!url || !url.startsWith('data:image/png')) throw new Error('bad url for ' + label);
  console.log(label, 'ok');
}

const legendaryHtml = sandbox.getEquipPixelIconHtml({ name: 'VOID_REAPER', type: 'mainhand', rarity: 'legendary' }, 22);
if (!legendaryHtml.includes('pixel-icon-wrap') || !legendaryHtml.includes('pixel-spark p4')) {
  throw new Error('legendary particle wrap missing');
}
console.log('legendary particle wrap ok');

console.log('Pixel icon tests passed');
