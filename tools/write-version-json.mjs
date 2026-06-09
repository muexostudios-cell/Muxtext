#!/usr/bin/env node
/** Write version.json from GAME_VERSION in index.html (deploy + local dev). */
import { readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const indexPath = join(root, 'index.html');
let html = readFileSync(indexPath, 'utf8');
const match = html.match(/GAME_VERSION='([^']+)'/);
if (!match) {
  console.error('GAME_VERSION not found in index.html');
  process.exit(1);
}
const version = match[1];
const metaRe = /<meta name="game-version" content="[^"]*">/;
if (metaRe.test(html)) {
  html = html.replace(metaRe, `<meta name="game-version" content="${version}">`);
  writeFileSync(indexPath, html);
}
const payload = { version, publishedAt: Date.now() };
writeFileSync(join(root, 'version.json'), `${JSON.stringify(payload, null, 2)}\n`);
console.log(`version.json -> ${version}`);
