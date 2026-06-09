import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync } from 'fs';
import { join } from 'path';

const root = '/workspace';
const server = createServer((req, res) => {
  const path = req.url === '/' ? '/index.html' : req.url.split('?')[0];
  try {
    const body = readFileSync(join(root, path));
    const type = path.endsWith('.html') ? 'text/html' : 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': type });
    res.end(body);
  } catch {
    res.writeHead(404);
    res.end('not found');
  }
});

await new Promise((r) => server.listen(8765, '127.0.0.1', r));

const errors = [];
const browser = await chromium.launch();
const page = await browser.newPage();
page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
page.on('console', (msg) => {
  if (msg.type() === 'error') errors.push('console: ' + msg.text());
});

await page.goto('http://127.0.0.1:8765/', { waitUntil: 'domcontentloaded', timeout: 30000 });
await page.waitForTimeout(2500);

const state = await page.evaluate(() => ({
  loading: document.getElementById('loading-overlay')?.style.display,
  account: document.getElementById('account-overlay')?.style.display,
  version: typeof GAME_VERSION !== 'undefined' ? GAME_VERSION : null,
  player: typeof player !== 'undefined' && !!player,
}));

console.log('state', JSON.stringify(state, null, 2));
console.log('errors', errors.length ? errors : 'none');

server.close();
await browser.close();
process.exit(errors.length ? 1 : 0);
