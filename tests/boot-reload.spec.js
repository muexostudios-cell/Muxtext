const path = require('path');
const { createServer } = require('http');
const { readFileSync } = require('fs');
const { join } = require('path');
const { expect, test } = require('@playwright/test');

test.use({ viewport: { width: 390, height: 844 } });

function startStaticServer() {
  const root = path.join(__dirname, '..');
  const server = createServer((req, res) => {
    const urlPath = req.url === '/' ? '/index.html' : req.url.split('?')[0];
    try {
      const body = readFileSync(join(root, urlPath));
      const type = urlPath.endsWith('.json')
        ? 'application/json'
        : urlPath.endsWith('.html')
          ? 'text/html'
          : 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': type });
      res.end(body);
    } catch {
      res.writeHead(404);
      res.end('not found');
    }
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}/` });
    });
  });
}

async function registerFreshAccount(page) {
  await expect(page.locator('#account-overlay')).toBeVisible({ timeout: 10000 });
  await page.locator('#account-tab-register').click();
  const user = `boot_${Date.now()}`;
  await page.locator('#account-username').fill(user);
  await page.locator('#account-password').fill('test1234');
  await page.locator('#account-password-confirm').fill('test1234');
  await page.locator('#account-display-input').fill('BootTester');
  await page.locator('#account-submit').click();

  const confirm = page.locator('#confirm-overlay');
  if (await confirm.isVisible({ timeout: 5000 }).catch(() => false)) {
    await page.locator('#confirm-yes').click();
  }

  await expect(page.locator('#account-overlay')).toBeHidden({ timeout: 15000 });
  await expect(page.locator('#player-name-custom')).toHaveText('BootTester');

  const version = page.locator('#version-update-overlay');
  if (await version.isVisible({ timeout: 2000 }).catch(() => false)) {
    await page.locator('#btn-version-update-refresh').click();
    await expect(version).toBeHidden({ timeout: 5000 });
  }
}

test('logged-in reload does not crash boot and restores session', async ({ page }) => {
  test.setTimeout(120000);
  const pageErrors = [];
  page.on('pageerror', (err) => pageErrors.push(err.message));

  const { server, baseUrl } = await startStaticServer();
  try {
    await page.goto(baseUrl);
    await expect(page.locator('#loading-overlay')).toBeVisible();
    await registerFreshAccount(page);
    expect(pageErrors).toEqual([]);

    await page.reload();
    await page.waitForTimeout(4000);

    expect(pageErrors.filter((m) => m.includes('inCombat'))).toEqual([]);
    await expect(page.locator('#account-overlay')).toBeHidden({ timeout: 15000 });
    await expect(page.locator('#player-name-custom')).toHaveText('BootTester');
  } finally {
    server.close();
  }
});
