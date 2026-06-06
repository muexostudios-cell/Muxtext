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
- 進度儲存於瀏覽器 `localStorage`

## 本地開發

```bash
python3 -m http.server 8000
```

開啟 http://localhost:8000/ 或 http://localhost:8000/index.html

## 專案結構

| 檔案 | 說明 |
|------|------|
| `index.html` | 遊戲主程式（唯一需要修改的遊戲原始碼） |
| `.github/workflows/deploy-pages.yml` | 自動部署至 GitHub Pages |

## 部署

推送到 `main` 分支後，GitHub Actions 會自動將網站發布到 GitHub Pages。

首次使用請在 GitHub 倉庫 **Settings → Pages** 中將來源設為 **GitHub Actions**。

## 授權

見倉庫授權條款。
