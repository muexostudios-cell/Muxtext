const path = require('path');
const { pathToFileURL } = require('url');
const { expect, test } = require('@playwright/test');

test.use({ viewport: { width: 390, height: 844 } });

async function completeBootAndRegister(page) {
  await expect(page.locator('#loading-overlay')).toBeVisible();
  await expect(page.locator('#account-overlay')).toBeVisible({ timeout: 10000 });

  await page.locator('#account-tab-register').click();
  await page.locator('#account-username').fill('move_test');
  await page.locator('#account-password').fill('test1234');
  await page.locator('#account-password-confirm').fill('test1234');
  await page.locator('#account-display-input').fill('MoveTester');
  await page.locator('#account-submit').click();

  const confirm = page.locator('#confirm-overlay');
  await expect(confirm).toBeVisible({ timeout: 5000 });
  await page.locator('#confirm-yes').click();

  await expect(page.locator('#account-overlay')).toBeHidden({ timeout: 15000 });
  await expect(page.locator('#player-name-custom')).toHaveText('MoveTester');
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
  await expect(page.locator('#map .cell')).toHaveCount(49, { timeout: 10000 });
  await expect(page.locator('#map-container')).toBeVisible();
}

async function getPlayerCell(page) {
  return page.evaluate(() => {
    const cells = Array.from(document.querySelectorAll('#map .cell'));
    const at = cells.find((el) => el.textContent === '@');
    if (!at) return null;
    return { r: Number(at.dataset.r), c: Number(at.dataset.c) };
  });
}

async function countPlayerMarkers(page) {
  return page.evaluate(() => {
    return Array.from(document.querySelectorAll('#map .cell')).filter((el) => el.textContent === '@').length;
  });
}

test('dungeon path keeps a single player marker and anchors from current tile', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.clear();
  });

  await page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href);
  await completeBootAndRegister(page);
  await enterManualDungeon(page);

  const start = await getPlayerCell(page);
  expect(start).not.toBeNull();

  await expect.poll(() => countPlayerMarkers(page)).toBe(1);

  const target = await page.evaluate(() => {
    const cells = Array.from(document.querySelectorAll('#map .cell'));
    const startCell = cells.find((el) => el.textContent === '@');
    const sr = Number(startCell.dataset.r);
    const sc = Number(startCell.dataset.c);
    const adjacent = cells.find((el) => {
      const r = Number(el.dataset.r);
      const c = Number(el.dataset.c);
      const ch = el.textContent;
      if (ch === '@') return false;
      return Math.abs(r - sr) + Math.abs(c - sc) === 1;
    });
    if (!adjacent) return null;
    return { r: Number(adjacent.dataset.r), c: Number(adjacent.dataset.c) };
  });
  expect(target).not.toBeNull();

  await page.locator(`#map .cell[data-r="${target.r}"][data-c="${target.c}"]`).click();
  await page.waitForTimeout(700);

  const afterMove = await getPlayerCell(page);
  expect(afterMove).toEqual(target);
  await expect.poll(() => countPlayerMarkers(page)).toBe(1);

  const monster = await page.evaluate(() => {
    const cells = Array.from(document.querySelectorAll('#map .cell.unexplored-monster, #map .cell'));
    const player = cells.find((el) => el.textContent === '@');
    const pr = Number(player.dataset.r);
    const pc = Number(player.dataset.c);
    const hits = Array.from(document.querySelectorAll('#map .cell.unexplored-monster'));
    const hit = hits.find((el) => {
      const r = Number(el.dataset.r);
      const c = Number(el.dataset.c);
      return Math.abs(r - pr) + Math.abs(c - pc) <= 6;
    }) || hits[0];
    if (!hit) return null;
    return { r: Number(hit.dataset.r), c: Number(hit.dataset.c) };
  });

  if (monster) {
    const mr = monster.r;
    const mc = monster.c;

    await page.locator(`#map .cell[data-r="${mr}"][data-c="${mc}"]`).click();
    await expect(page.locator('#battle-screen.active')).toBeVisible({ timeout: 8000 });

    const combatPos = await getPlayerCell(page);
    expect(combatPos).toEqual({ r: mr, c: mc });
    await expect.poll(() => countPlayerMarkers(page)).toBe(1);

    for (let i = 0; i < 40; i += 1) {
      if (!(await page.locator('#battle-screen.active').isVisible())) break;
      const mainBtn = page.locator('#btn-atk-main');
      if (await mainBtn.isEnabled()) await mainBtn.click();
      await page.waitForTimeout(350);
    }

    await expect(page.locator('#battle-screen.active')).toBeHidden({ timeout: 10000 });
    await page.waitForTimeout(1600);

    const clearedChar = await page.locator(`#map .cell[data-r="${mr}"][data-c="${mc}"]`).textContent();
    expect(clearedChar).not.toBe('#');
    expect(clearedChar).not.toBe('!');
    expect(clearedChar).not.toBe('X');

    const afterKill = await getPlayerCell(page);
    expect(afterKill).toEqual({ r: mr, c: mc });
    expect(afterKill).toEqual(combatPos);

    const retarget = await page.evaluate(() => {
      const cells = Array.from(document.querySelectorAll('#map .cell'));
      const player = cells.find((el) => el.textContent === '@');
      const pr = Number(player.dataset.r);
      const pc = Number(player.dataset.c);
      const next = cells.find((el) => {
        const r = Number(el.dataset.r);
        const c = Number(el.dataset.c);
        const ch = el.textContent;
        if (ch === '@' || ch === '#' || ch === 'M') return false;
        return Math.abs(r - pr) + Math.abs(c - pc) === 1;
      });
      if (!next) return null;
      return { r: Number(next.dataset.r), c: Number(next.dataset.c) };
    });

    if (retarget) {
      await page.locator(`#map .cell[data-r="${retarget.r}"][data-c="${retarget.c}"]`).click();
      await page.waitForTimeout(400);
      const anchored = await getPlayerCell(page);
      expect(anchored).toEqual(retarget);
      await expect.poll(() => countPlayerMarkers(page)).toBe(1);
    }
  }
});
