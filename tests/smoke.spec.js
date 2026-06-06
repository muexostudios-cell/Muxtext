const path = require('path');
const { pathToFileURL } = require('url');
const { expect, test } = require('@playwright/test');

test.use({ viewport: { width: 390, height: 844 } });

async function expectControlsWithinViewport(page, selectors) {
  const overflowing = await page.evaluate((selectorsToCheck) => {
    return selectorsToCheck.flatMap((selector) => {
      return Array.from(document.querySelectorAll(selector))
        .filter((el) => {
          const style = window.getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0;
        })
        .filter((el) => {
          const rect = el.getBoundingClientRect();
          return rect.left < -1 || rect.right > window.innerWidth + 1;
        })
        .map((el) => selector + (el.id ? `#${el.id}` : ''));
    });
  }, selectors);

  expect(overflowing).toEqual([]);
}

test('starts a manual dungeon run and renders the map', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.clear();
    localStorage.setItem('td_player_name', 'SmokeTester');
  });

  await page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href);

  await expect(page).toHaveTitle(/MUX text-rpg/);
  await expect(page.locator('#player-name-custom')).toHaveText('SmokeTester');
  await expectControlsWithinViewport(page, [
    '#btn-settings',
    '#quick-btns button',
    '#tab-bar button',
    '#action-bar button',
  ]);

  await page.locator('#btn-dungeon').click();
  await expect(page.locator('#dungeon-overlay')).toBeVisible();

  await page.locator('.dungeon-level-btn:not(.locked)').first().click();
  await expect(page.locator('#difficulty-overlay')).toBeVisible();

  await page.locator('.difficulty-btn.normal-diff').click();
  await expect(page.locator('#drone-dungeon-overlay')).toBeVisible();

  await page.locator('#drone-dungeon-no').click();
  await expect(page.locator('#map .cell')).toHaveCount(49);
  await expect(page.locator('#map-container')).toBeVisible();
  await expectControlsWithinViewport(page, ['#action-bar button', '#tab-bar button']);
});
