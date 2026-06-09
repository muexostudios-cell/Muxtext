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

test('dungeon map uses plain text cells and player glyph', async ({ page }) => {
  test.setTimeout(120000);
  await page.addInitScript(() => {
    localStorage.clear();
  });

  await page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href);
  await completeBootAndRegister(page);
  await enterManualDungeon(page);

  const layout = await page.evaluate(() => {
    const cells = Array.from(document.querySelectorAll('#map .cell'));
    const player = cells.find((el) => el.textContent.includes('@'));
    const mapEl = document.getElementById('map');
    const pixelNodes = cells.filter((el) =>
      el.querySelector('.cell-pixel, .cell-mob, img.pixel-icon, .pixel-icon-wrap'),
    );
    const cellsWithChildren = cells.filter((el) => el.children.length > 0);
    const tileClassCells = cells.filter((el) =>
      Array.from(el.classList).some((name) => name.startsWith('tile-')),
    );
    const glyphs = cells.map((el) => el.textContent.trim()).filter(Boolean);
    const cell = getComputedStyle(cells[0]);
    return {
      pixelNodeCount: pixelNodes.length,
      childCellCount: cellsWithChildren.length,
      tileClassCount: tileClassCells.length,
      hasPlayer: !!player,
      hasVisitedTiles: cells.some((el) => el.classList.contains('tile-visited') || el.classList.contains('visited')),
      hasDungeonGlyphs: glyphs.length > 0,
      hasEnemyPortrait: !!document.getElementById('enemy-portrait'),
      mapIsGrid: getComputedStyle(mapEl).display === 'grid',
      mapGapNotPixelated: getComputedStyle(mapEl).backgroundImage === 'none',
      cellUsesTextLayout: cell.display === 'flex',
    };
  });

  expect(layout.pixelNodeCount).toBe(0);
  expect(layout.childCellCount).toBe(0);
  expect(layout.tileClassCount).toBe(0);
  expect(layout.hasPlayer).toBe(true);
  expect(layout.hasDungeonGlyphs).toBe(true);
  expect(layout.hasVisitedTiles).toBe(true);
  expect(layout.hasEnemyPortrait).toBe(false);
  expect(layout.mapIsGrid).toBe(true);
  expect(layout.mapGapNotPixelated).toBe(true);
  expect(layout.cellUsesTextLayout).toBe(true);
});
