# 國小低年級段考自動出卷助手與 GitHub Pages 全自動部署實施計畫

本計畫目標是實作**「方案 B (全自動)」**，將考卷自動部署到您的 GitHub 儲存庫 `teajsps-ux/jsps-tools`。
同時，為了解決手機或平板施測時要求 Google 帳戶登入的問題，本方案會將考卷發佈於 GitHub Pages：`https://teajsps-ux.github.io/jsps-tools/`。

為此，我們需要調整網頁架構，在主入口新增「低年級互動考卷」卡片（圖 1），並建立分科目的二級入口網站（圖 2），最後使 Python 出卷腳本完全自動化。

---

## 🏗 新增與調整的網頁架構

預計在您的 `jsps-tools` 本地儲存庫中建立以下結構：
```text
g:\我的雲端硬碟\Antigravity-2-workspace\jsps-tools\
├── index.html                           ← [修改] 主入口網站，新增「低年級互動考卷」卡片
└── tools\
    └── gr12-exams\
        ├── index.html                   ← [新建] 二級分科目入口網站 (圖 2)
        ├── guoyu\                       ← 國語考卷上傳位置 (例如 KH115-L03-A.html)
        ├── math\                        ← 數學考卷上傳位置
        └── life\                        ← 生活考卷上傳位置
```

---

## 🛠️ 實施步驟說明

### 1. 修改主入口 `index.html` (圖 1)
在「自製互動教具」區塊中新增一個卡片：
* **卡片名稱**：`低年級互動考卷`
* **連結**：`./tools/gr12-exams/`
* **樣式**：使用 `c-rose` (玫瑰紅漸層) 或 `c-indigo` (靛藍色)，包含專屬 icon (如 📝 或 ✍️) 與說明文字。

### 2. 建立分科目二級入口 `tools/gr12-exams/index.html` (圖 2)
參考 `tools/html-lessons/index.html` 的精美卡片風格，設計二級入口：
* **頂部**：帶有「← 回首頁」按鈕、精美標題與副標題。
* **分類區**：分開呈現「國語科」、「數學科」、「生活科」三大區塊。
* **內容呈現**：
  > [!TIP]
  > 我們將讓這個二級入口網頁能夠動態載入一個 `exams_list.json` 檔案。
  > 這樣一來，每次 Python 出卷腳本產生新考卷時，只要自動更新 `exams_list.json`，網頁就會自動重新整理，列出最新的考卷，不需要每次手動改 HTML！
  * 每個考卷連結旁會提供 `[A版連結]`、`[B版連結]`，以及 `[下載 QR Code]` 的連結，方便老師列印或展示在教室大螢幕上讓學生掃描。

### 3. 升級 Python 出卷腳本 (`build_exam.py`)
升級後的 Python 腳本將具備以下「全自動」功能：
1. **科目識別與自動分類**：根據設定的科目（如 `subject = 'guoyu'`），自動將產生的 A/B 版 HTML 輸出至對應資料夾（例如 `tools/gr12-exams/guoyu/`）。
2. **自動產生 QR Code**：
   * 根據 GitHub Pages 網址格式：`https://teajsps-ux.github.io/jsps-tools/tools/gr12-exams/<subject>/<filename>`
   * 呼叫免費 QR Code API（`https://api.qrserver.com/v1/create-qr-code/`）下載考卷對應的 QR Code PNG 檔，並直接存在考卷旁。
3. **自動更新 `exams_list.json`**：將新考卷的資訊（標題、路徑、發佈日期）寫入清單檔，供二級入口網頁讀取。
4. **自動推送到 GitHub (Git Auto-Push)**：
   * 自動在儲存庫目錄下執行：
     ```bash
     git add .
     git commit -m "Auto-deploy exam: <考卷名稱>"
     git push origin main
     ```
   * 這樣您只要在電腦跑一次 Python 腳本，考卷就會直接上傳到 GitHub，並在數十秒後生效，學生掃 QR code 即可直接在平板施測！

---

## 📋 待確認項目

> [!IMPORTANT]
> 為了讓 `build_exam.py` 能順利推送到您的 GitHub，請確認以下事項：
> 1. 本地電腦的 Git 已經設定好憑證（之前執行過 `git push` 不需要重複登入即可推上去）。
> 2. `exams_list.json` 是否包含科目分類（國語、數學、生活）？

---

## 🚀 驗證計畫

### 自動化測試
* 執行更新後的 `build_exam.py` 腳本，確認是否能在 `tools/gr12-exams/guoyu/` 正確產生 A/B 版 HTML 與對應的 QR Code PNG。
* 確認 Git 命令是否順利執行，且無權限報錯。

### 手動驗證
* 開啟瀏覽器測試 `index.html` 與新建立的 `tools/gr12-exams/index.html`。
* 檢查二級入口網站是否能正確讀取並顯示 `exams_list.json` 中的考卷卡片。
