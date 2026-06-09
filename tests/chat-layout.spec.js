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

  test('mobile embedded chat fits viewport and scrolls messages', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await dismissBootOverlays(page);

    await page.evaluate(() => document.getElementById('btn-chat').click());
    await expect(page.locator('#chat-embedded')).toHaveClass(/show/);

    const panelBox = await page.locator('#chat-embedded #chat-panel').boundingBox();
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

    await page.evaluate(() => document.getElementById('btn-chat').click());
    await expect(page.locator('#chat-embedded')).not.toHaveClass(/show/);
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
      const panel = document.querySelector('#chat-embedded #chat-panel');
      const input = document.getElementById('chat-input-row');
      const tabBar = document.getElementById('tab-bar');
      const pr = panel.getBoundingClientRect();
      const ir = input.getBoundingClientRect();
      const tr = tabBar.getBoundingClientRect();
      return {
        textScale: getComputedStyle(document.documentElement).getPropertyValue('--chat-text-scale').trim(),
        panelH: getComputedStyle(document.documentElement).getPropertyValue('--chat-panel-h').trim(),
        panelFits: pr.bottom <= window.innerHeight + 2,
        inputInPanel: ir.bottom <= pr.bottom + 1,
        tabBelowChat: tr.top >= pr.bottom - 2,
        chatRootFont: getComputedStyle(document.getElementById('chat-embedded')).fontSize,
      };
    });

    expect(layout.textScale).toBe('2');
    expect(parseInt(layout.panelH, 10)).toBeGreaterThan(400);
    expect(layout.panelFits).toBe(true);
    expect(layout.inputInPanel).toBe(true);
    expect(layout.tabBelowChat).toBe(true);
    expect(parseFloat(layout.chatRootFont)).toBeGreaterThan(20);
  });

  test('mobile chat stays open when viewport resizes', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await dismissBootOverlays(page);

    await page.evaluate(() => document.getElementById('btn-chat').click());
    await expect(page.locator('#chat-embedded')).toHaveClass(/show/);

    await page.setViewportSize({ width: 390, height: 680 });
    await page.evaluate(() => {
      window.dispatchEvent(new Event('resize'));
      if (window.visualViewport) window.visualViewport.dispatchEvent(new Event('resize'));
    });

    await expect(page.locator('#chat-embedded')).toHaveClass(/show/);
  });

  test('mobile tab bar stays below chat panel', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await dismissBootOverlays(page);

    await page.evaluate(() => document.getElementById('btn-chat').click());
    await expect(page.locator('#chat-embedded')).toHaveClass(/show/);

    const layout = await page.evaluate(() => {
      const tabBar = document.getElementById('tab-bar');
      const chat = document.getElementById('chat-embedded');
      const input = document.getElementById('chat-input-row');
      const main = document.getElementById('game-main');
      const tabRect = tabBar.getBoundingClientRect();
      const chatRect = chat.getBoundingClientRect();
      const inputRect = input.getBoundingClientRect();
      const mainRect = main.getBoundingClientRect();
      const tabIndex = Array.from(main.children).indexOf(tabBar);
      const chatIndex = Array.from(main.children).indexOf(chat);
      return {
        tabBelowChat: tabRect.top >= chatRect.bottom - 2,
        tabNearBottom: tabRect.bottom >= mainRect.bottom - 4,
        inputAboveTab: inputRect.bottom <= tabRect.top + 2,
        tabIsLast: tabIndex === main.children.length - 1,
        tabAfterChat: chatIndex >= 0 && tabIndex > chatIndex,
      };
    });

    expect(layout.tabAfterChat).toBe(true);
    expect(layout.tabIsLast).toBe(true);
    expect(layout.tabBelowChat).toBe(true);
    expect(layout.tabNearBottom).toBe(true);
    expect(layout.inputAboveTab).toBe(true);
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
