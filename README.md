# jsps-tools

老師自製班級教學工具集。用 Claude Code + Google Drive + GitHub Pages + Firebase 打造。

## 工具清單

打開首頁：**[🎒 教學工具箱總入口](https://teajsps-ux.github.io/jsps-tools/)**（卡片牆，點圖進工具）

| 工具 | 說明 | 直接打開 |
|------|------|---------|
| 📺 下課跑馬燈播報員 | 給國小小朋友看的大字跑馬燈,有注音、會朗讀、森林動態背景 | **[▶ 開啟](./tools/marquee-reader/)** |
| 🎵 注音節拍遊戲 | 跟著音樂節拍認讀注音卡,五回合閃動挑戰,派對氣氛炒熱全班 | **[▶ 開啟](./tools/say-the-word/)** |
| ☁️ 班級互動文字雲 V2 | 學生即時輸入關鍵字,變成彩色文字雲飛上螢幕(需 Firebase) | **[▶ 開啟](./tools/wordcloud/)** |
| 🔎 Word Search 找字遊戲 | 老師出題、座號登入、競速/時限雙模式、本機排行榜、芫荽注音字型 | **[▶ 開啟](./tools/word-search/)** |
| 📋 作業清點矩陣 | 全班作業狀態看板,支援日期分檔、缺交/未訂正大看板與 Firebase 即時同步 | **[▶ 開啟](./tools/homework-matrix/)** |
| 📖 我是國語背書高手 | 翰林 114 一上詞語/成語題庫,翻牌測驗、答錯複習、朗讀、匯入匯出與宮格對戰 | **[▶ 開啟](./tools/mandarin-flashcard/)** |

> 📱 以上連結在手機、平板、電腦、教室電視都能直接用。建議存成瀏覽器書籤或 iPad 桌面捷徑。

## 架構

- 📋 GDrive 工作桌 → 寫程式碼
- 🐙 GitHub Pages → 公開網頁
- 🔥 Firebase → 學生互動資料
- 📘 Obsidian → 工作筆記

詳見 `CLAUDE.md`。
