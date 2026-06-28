# 尋隱者不遇 HTML 簡報 — 完工接力記錄

## 專案定位
- 編號：#07（原文課本第 07 頁）
- 唐詩：賈島〈尋隱者不遇〉
- 互動式詩詞教學 HTML 簡報
- 最終部署路徑：`tools/classical-poems/07-xunzhe/`

## 最終檔案結構

```
07-xunzhe/
├── index.html          ← 主簡報（256KB，含所有 JS/CSS/互動）
├── audio/
│   ├── manifest.json   ← 31 個 WAV 對照表
│   ├── generate_audio.py ← VoxCPM2 批次生成腳本（含同音字修正記錄）
│   └── 31 *.wav        ← 16.7 MB（Sulafat 女聲 + Sadaltager 男聲）
├── generated/
│   └── 10 *.png        ← AI 生成場景插圖
├── FIXES.md            ← 語音修正記錄（同音字替換策略）
└── RELAY-RECORD.md     ← 本檔案
```

## 已完成里程碑

1. **HTML 開發**：10 頁完整流程（首頁→4 句教學→對照→心情→3 遊戲→結束）
2. **圖像生成**：10 張 AI 場景插圖（home, line1-4, compare, heart, gameA/B/C）
3. **音檔生成**：31 個 WAV（VoxCPM2 Sulafat/Sadaltager，16.7 MB）
4. **語音修正**
   - 採藥竹簡版→彩要築撿板（`game-c-guide-sulafat.wav`）
   - 樹→豎（`word-songxia.wav` / `line1-plain-sulafat.wav` / `heart-guide-sadaltager.wav`）
   - 心區右側獨立音檔（`heart-right-sulafat.wav`）
5. **播放機制改進**
   - Slides 2-5 自動旁白使用既有 WAV 取代 TTS
   - 三種遊戲完成統一播放全詩朗讀
   - 首次點擊解鎖瀏覽器自動播放限制
   - 防止方向鍵造成音檔重疊
6. **Gallery 整合**
   - `tools/classical-poems/index.html` 新增編號 07 卡片
   - 封面圖 `assets/07-xunzhe-cover.png`
7. **Git 部署**
   - `jsps-tools` repo: commit d4bd6ef (deck) + 7991c94 (gallery)
   - Push 至 GitHub `origin/main`
8. **Firebase 部署**
   - Hosting: https://jsps-tools-sync.web.app 上線

## 已知同音字替換記錄

| WAV 檔案 | 顯示文字 | TTS 輸入（同音字） |
|---|---|---|
| `game-c-guide-sulafat.wav` | 採藥竹簡版 | 彩要築撿板 |
| `word-songxia.wav` | 松下 | 松豎 |
| `line1-plain-sulafat.wav` | 松下 | 松豎 |
| `heart-guide-sadaltager.wav` | 松下 | 松豎 |

## 技術債 / 可優化項目

- [ ] `generate_audio.py` 若需全面重新生成，注意同音字修正部分需手動處理
- [ ] VoxCPM2 環境：`C:\2026_Antigravity_語音\.venv\Scripts\python.exe`
- [ ] 如果 TTS 模型更新，`game-c-guide` 的前五字（彩要築撿）可能需要調整注音輸入
- [ ] `heart-right` 音檔文字：「有時候找不到人，不一定是壞事。可以學會耐心等待，也可以欣賞風景。」（不含「我們學到」前綴）

## 移交說明

- 簡報已在 `jsps-tools` GitHub + Firebase 上線
- 若需修改內容，編輯 `index.html` 後重新 push + deploy 即可
- 若需重製音檔，執行 `generate_audio.py` 後更新 `manifest.json`
