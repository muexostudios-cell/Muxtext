import fs from 'fs';

const h = fs.readFileSync('/workspace/index.html', 'utf8');
const start = h.indexOf('<script>') + 8;
const end = h.lastIndexOf('</script>');
try {
  new Function(h.slice(start, end));
  console.log('JS OK');
} catch (e) {
  console.error('JS FAIL', e.message);
  process.exit(1);
}

for (const s of [
  'updateCombatItemBarVisibility',
  'syncPlayerSeal',
  'ensurePlayerEquipment',
  'dungeonEntryBusy',
  'versionUpdateBlocking',
  'combat-item-bar',
]) {
  console.log(s, h.split(s).length - 1);
}

const i = h.indexOf('id="combat-item-bar"');
console.log('combat bar near battle-screen:', h.slice(i - 120, i + 80).includes('battle-screen') || h.slice(i - 200, i).includes('battle-row'));
console.log('combat bar NOT near action-bar:', !h.includes('combat-item-bar"></div><div id="action-bar">'));

const zh = h.indexOf('versionUpdateBlocking');
const en = h.indexOf('versionUpdateBlocking', zh + 1);
console.log('zh lang', h.slice(zh, zh + 120));
console.log('en lang', h.slice(en, en + 120));
