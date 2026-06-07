const path = require('path');
const { pathToFileURL } = require('url');
const { expect, test } = require('@playwright/test');

async function dismissBootOverlays(page) {
  await page.evaluate(() => {
    ['account-overlay', 'loading-overlay', 'version-update-overlay', 'network-overlay'].forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.style.display = 'none';
    });
    window.dispatchEvent(new Event('resize'));
  });
}

test.describe('chat layout', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(pathToFileURL(path.join(__dirname, '..', 'index.html')).href, { waitUntil: 'load' });
    await page.waitForTimeout(500);
    await dismissBootOverlays(page);
  });

  test('mobile overlay fits viewport and scrolls messages', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await dismissBootOverlays(page);

    await page.evaluate(() => document.getElementById('btn-chat').click());
    await expect(page.locator('#chat-overlay')).toHaveClass(/open/);
    await expect(page.locator('#chat-overlay')).toBeVisible();

    const panelBox = await page.locator('#chat-overlay #chat-panel').boundingBox();
    expect(panelBox).toBeTruthy();
    expect(panelBox.y + panelBox.height).toBeLessThanOrEqual(844 + 2);

    const metrics = await page.evaluate(() => ({
      panelH: getComputedStyle(document.documentElement).getPropertyValue('--chat-panel-h').trim(),
      vh: getComputedStyle(document.documentElement).getPropertyValue('--chat-vh').trim(),
    }));
    expect(parseInt(metrics.panelH, 10)).toBeGreaterThan(200);
    expect(metrics.vh).toMatch(/px$/);

    const scrollable = await page.evaluate(() => {
      const el = document.getElementById('chat-messages');
      for (let i = 0; i < 30; i += 1) {
        const div = document.createElement('div');
        div.className = 'chat-msg';
        div.textContent = `line ${i} `.repeat(8);
        el.appendChild(div);
      }
      return el.scrollHeight > el.clientHeight;
    });
    expect(scrollable).toBe(true);

    await page.evaluate(() => document.getElementById('btn-close-chat').click());
    await expect(page.locator('#chat-overlay')).toBeHidden();
  });

  test('large text size keeps chat controls visible', async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem(
        'td_settings',
        JSON.stringify({
          uiScale: 1,
          textSize: 2,
          autoHerb: { enabled: false, threshold: 30, herbId: 'herb_low' },
        }),
      );
    });
    await page.reload({ waitUntil: 'load' });
    await page.waitForTimeout(500);
    await dismissBootOverlays(page);
    await page.setViewportSize({ width: 390, height: 844 });
    await dismissBootOverlays(page);

    await page.evaluate(() => document.getElementById('btn-chat').click());

    const layout = await page.evaluate(() => {
      const panel = document.querySelector('#chat-overlay #chat-panel');
      const input = document.getElementById('chat-input-row');
      const close = document.getElementById('btn-close-chat');
      const pr = panel.getBoundingClientRect();
      const ir = input.getBoundingClientRect();
      const cr = close.getBoundingClientRect();
      return {
        textScale: getComputedStyle(document.documentElement).getPropertyValue('--chat-text-scale').trim(),
        panelH: getComputedStyle(document.documentElement).getPropertyValue('--chat-panel-h').trim(),
        panelFits: pr.bottom <= window.innerHeight + 2,
        inputInPanel: ir.bottom <= pr.bottom + 1,
        closeInPanel: cr.bottom <= pr.bottom + 1,
        chatRootFont: getComputedStyle(document.getElementById('chat-overlay')).fontSize,
      };
    });

    expect(layout.textScale).toBe('2');
    expect(parseInt(layout.panelH, 10)).toBeGreaterThan(400);
    expect(layout.panelFits).toBe(true);
    expect(layout.inputInPanel).toBe(true);
    expect(layout.closeInPanel).toBe(true);
    expect(parseFloat(layout.chatRootFont)).toBeGreaterThan(20);
  });

  test('desktop shows chat in panel sidebar', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 900 });
    await dismissBootOverlays(page);

    await page.evaluate(() => document.getElementById('btn-chat').click());
    await expect(page.locator('#game')).toHaveClass(/desktop-layout/);
    await expect(page.locator('#panel-sidebar #chat-embedded')).toHaveClass(/show/);
    await expect(page.locator('#chat-overlay')).toBeHidden();

    const sidebarBox = await page.locator('#panel-sidebar').boundingBox();
    const panelBox = await page.locator('#panel-sidebar #chat-panel').boundingBox();
    expect(sidebarBox).toBeTruthy();
    expect(panelBox).toBeTruthy();
    expect(panelBox.x).toBeGreaterThanOrEqual(sidebarBox.x - 1);
    const widthOk = await page.evaluate(() => {
      const sidebar = document.getElementById('panel-sidebar');
      const panel = document.querySelector('#panel-sidebar #chat-panel');
      return panel.offsetWidth <= sidebar.offsetWidth;
    });
    expect(widthOk).toBe(true);
  });
});
