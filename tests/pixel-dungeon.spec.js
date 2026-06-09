const path = require('path');
const { pathToFileURL } = require('url');
const { expect, test } = require('@playwright/test');

test.use({ viewport: { width: 390, height: 844 } });

async function completeBootAndRegister(page) {
  await expect(page.locator('#loading-overlay')).toBeVisible();
  await expect(page.locator('#account-overlay')).toBeVisible({ timeout: 10000 });

  const user = `text_${Date.now()}`;
  await page.locator('#account-tab-register').click();
  await page.locator('#account-username').fill(user);
  await page.locator('#account-password').fill('test1234');
  await page.locator('#account-password-confirm').fill('test1234');
  await page.locator('#account-display-input').fill('TextTester');
  await page.locator('#account-submit').click();

  const confirm = page.locator('#confirm-overlay');
  await expect(confirm).toBeVisible({ timeout: 5000 });
  await page.locator('#confirm-yes').click();

  await expect(page.locator('#account-overlay')).toBeHidden({ timeout: 15000 });
}

async function enterManualDungeon(page) {
  await page.locator('#btn-dungeon').click();
  await expect(page.locator('#dungeon-overlay')).toBeVisible();
  await page.locator('.dungeon-level-btn:not(.locked)').first().click();
  await expect(page.locator('#difficulty-overlay')).toBeVisible();
  await page.locator('.difficulty-btn.normal-diff').click();
  const droneOverlay = page.locator('#drone-dungeon-overlay');
  if (await droneOverlay.isVisible({ timeout: 2000 }).catch(() => false)) {
    await page.locator('#drone-dungeon-no').click();
  }
  await expect(page.locator('#map .cell')).toHaveCount(49, { timeout: 15000 });
}

test('dungeon map uses text glyphs instead of pixel tiles', async ({ page }) => {
  test.setTimeout(120000);
  await page.addInitScript(() => {
    localStorage.clear();
  });

  await page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href);
  await completeBootAndRegister(page);
  await enterManualDungeon(page);

  const layout = await page.evaluate(() => {
    const cells = Array.from(document.querySelectorAll('#map .cell'));
    const player = cells.find((el) => el.textContent.trim() === '@');
    const withPixel = cells.filter((el) => el.querySelector('.cell-pixel'));
    const textCells = cells.filter((el) => el.textContent.trim().length > 0);
    return {
      cellCount: cells.length,
      hasPlayer: !!player,
      pixelTileCount: withPixel.length,
      textCellCount: textCells.length,
      sampleText: cells.map((el) => el.textContent.trim()).filter(Boolean).slice(0, 8),
    };
  });

  expect(layout.cellCount).toBe(49);
  expect(layout.hasPlayer).toBe(true);
  expect(layout.pixelTileCount).toBe(0);
  expect(layout.textCellCount).toBeGreaterThan(1);
});
