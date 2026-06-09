const path = require('path');
const { pathToFileURL } = require('url');
const { expect, test } = require('@playwright/test');

test.use({ viewport: { width: 390, height: 844 } });

async function completeBootAndRegister(page) {
  await expect(page.locator('#loading-overlay')).toBeVisible();
  await expect(page.locator('#account-overlay')).toBeVisible({ timeout: 10000 });

  const user = `pixel_${Date.now()}`;
  await page.locator('#account-tab-register').click();
  await page.locator('#account-username').fill(user);
  await page.locator('#account-password').fill('test1234');
  await page.locator('#account-password-confirm').fill('test1234');
  await page.locator('#account-display-input').fill('PixelTester');
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

test('dungeon map uses pixel cyber tiles and player glyph', async ({ page }) => {
  test.setTimeout(120000);
  await page.addInitScript(() => {
    localStorage.clear();
  });

  await page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href);
  await completeBootAndRegister(page);
  await enterManualDungeon(page);

  const layout = await page.evaluate(() => {
    const cells = Array.from(document.querySelectorAll('#map .cell'));
    const withTile = cells.filter((el) => el.querySelector('.cell-pixel img.pixel-icon'));
    const player = cells.find((el) => el.textContent.includes('@'));
    const mobWrap = cells.find((el) => el.querySelector('.cell-mob .pixel-icon-wrap, .cell-mob .pixel-icon'));
    const mapTray = getComputedStyle(document.getElementById('map'));
    const cell = getComputedStyle(cells[0]);
    const parseLum = (css) => {
      const m = css.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      if (!m) return 0;
      const [r, g, b] = m.slice(1, 4).map(Number);
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };
    const mapEl = document.getElementById('map');
    const sampleCell = cells[0];
    return {
      tileCount: withTile.length,
      hasPlayer: !!player,
      hasMobIcon: !!mobWrap,
      hasVisitedTiles: cells.some((el) => el.classList.contains('tile-visited') || el.classList.contains('visited')),
      hasMonsterTiles: cells.some((el) => el.classList.contains('tile-monster')),
      mapGapNotPixelated: getComputedStyle(mapEl).backgroundImage === 'none',
      cellClipped: getComputedStyle(sampleCell).overflow === 'hidden',
      mapHasCyberBg: getComputedStyle(document.getElementById('map-container')).backgroundImage !== 'none',
      cellBorderLum: parseLum(cell.borderTopColor),
      mapTrayBorderLum: parseLum(mapTray.borderTopColor),
    };
  });

  expect(layout.tileCount).toBeGreaterThan(40);
  expect(layout.hasPlayer).toBe(true);
  expect(layout.hasVisitedTiles).toBe(true);
  expect(layout.mapGapNotPixelated).toBe(true);
  expect(layout.cellClipped).toBe(true);
  expect(layout.mapHasCyberBg).toBe(true);
  expect(layout.cellBorderLum).toBeGreaterThan(layout.mapTrayBorderLum);
});
