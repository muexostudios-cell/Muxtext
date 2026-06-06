# MUX text-rpg · 文字地城

夜之城風格的文字 RPG 網頁遊戲。用瀏覽器開啟即可遊玩，免安裝、免下載。

## 立即遊玩

**線上網址（GitHub Pages）：**

https://muexostudios-cell.github.io/Muxtext/

手機或電腦瀏覽器直接開啟上述網址即可開始遊戲。

## 功能特色

- 單檔網頁遊戲，離線可玩（聊天需網路）
- 探索地城、戰鬥、裝備、合成、天賦系統
- 響應式介面：手機 / 桌面自動適配
- 桌面版三欄版面：日誌 | 主遊戲 | 裝備面板
- 夜之城公共聊天室
- **雲端帳號**：註冊登入後進度可跨裝置同步（端到端加密，需網路）
- 本機快取 + 雲端備份雙重保存

## 本地開發

```bash
python3 -m http.server 8000
```

開啟 http://localhost:8000/ 或 http://localhost:8000/index.html

## 測試

瀏覽器煙霧測試使用 Playwright：

```bash
npm install
npx playwright install chromium
npm test
```

測試會註冊帳號、進入地城並驗證地圖渲染與按鈕不超出視窗。

## 專案結構

| 檔案 | 說明 |
|------|------|
| `index.html` | 遊戲主程式（唯一需要修改的遊戲原始碼） |
| `tests/smoke.spec.js` | Playwright 瀏覽器煙霧測試 |
| `package.json` | 測試腳本與開發依賴 |
| `.github/workflows/deploy-pages.yml` | 自動部署至 GitHub Pages |

## 部署

推送到 `main` 分支後，GitHub Actions 會自動將網站發布到 GitHub Pages。

首次使用請在 GitHub 倉庫 **Settings → Pages** 中將來源設為 **GitHub Actions**。

## 授權

見倉庫授權條款。
