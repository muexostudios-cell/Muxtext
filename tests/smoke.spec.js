const path = require('path');
const { pathToFileURL } = require('url');
const { expect, test } = require('@playwright/test');

test('starts a manual dungeon run and renders the map', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.clear();
    localStorage.setItem('td_player_name', 'SmokeTester');
  });

  await page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href);

  await expect(page).toHaveTitle(/MUX text-rpg/);
  await expect(page.locator('#player-name-custom')).toHaveText('SmokeTester');

  await page.locator('#btn-dungeon').click();
  await expect(page.locator('#dungeon-overlay')).toBeVisible();

  await page.locator('.dungeon-level-btn:not(.locked)').first().click();
  await expect(page.locator('#difficulty-overlay')).toBeVisible();

  await page.locator('.difficulty-btn.normal-diff').click();
  await expect(page.locator('#drone-dungeon-overlay')).toBeVisible();

  await page.locator('#drone-dungeon-no').click();
  await expect(page.locator('#map .cell')).toHaveCount(49);
  await expect(page.locator('#map-container')).toBeVisible();
});
