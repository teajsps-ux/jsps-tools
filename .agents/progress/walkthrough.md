# 低年級段考出卷自動化與 GitHub Pages 部署 — 成果說明

我們已成功實作 **「方案 B (全自動)」**！現在所有的低年級互動考卷都會自動發佈到您的 GitHub Pages 網站（`https://teajsps-ux.github.io/jsps-tools/`），解決了行動裝置施測時要求 Google 帳戶登入的問題。

同時，我們也打造了**二級分科目入口網站**，將不同科目的考卷分流，並使 Python 出卷腳本完全自動化。

---

## 🎨 1. 主入口網站新增「低年級互動考卷」卡片 (圖 1)
* **位置**：`jsps-tools/index.html` 中的「自製互動教具」區塊。
* **卡片內容**：新增了帶有 📝 圖示的「低年級互動考卷」玫瑰紅色卡片，點擊後即可進入二級入口網站。

---

## 📚 2. 二級分科目入口網站 (圖 2)
* **位置**：[tools/gr12-exams/index.html](file:///g:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/Antigravity-2-workspace/jsps-tools/tools/gr12-exams/index.html)
* **功能特色**：
  1. **分欄展示**：區分為「國語科 📚」、「數學科 📐」與「生活科 🌱」三大欄位。
  2. **動態載入**：網頁會自動讀取 [exams_list.json](file:///g:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/Antigravity-2-workspace/jsps-tools/tools/gr12-exams/exams_list.json)，出卷後無須手動修改網頁即可自動更新。
  3. **施測彈窗**：點擊卡片中的「📱 顯示施測 QR Code」，會以精美的毛玻璃彈窗同時顯示 A 版與 B 版考卷的 QR Code。老師可直接投影在教室螢幕上供學生掃描，或者點選 A/B 版按鈕直接開啟考卷。

---

## 🔄 3. 升級版 Python 出卷腳本 (`build_exam.py`)
* **位置**：[build_exam.py](file:///G:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/codex-skills/gr12-exam-generator/build_exam.py)
* **自動化工作流**：
  1. **科目識別**：根據腳本最上方的 `SUBJECT` 變數（可設為 `guoyu`、`math`、`life`），自動將考卷 HTML 儲存到對應資料夾。
  2. **自動下載 QR Code**：根據部署後的 GitHub Pages 網址，自動透過 API 下載 300x300px 的 QR Code PNG 圖片，並存在考卷 HTML 旁。
  3. **自動更新清單**：自動將考卷標題、路徑與 QR Code 資訊寫入 `exams_list.json`。
  4. **自動 Git 推送**：在儲存庫目錄下執行 `git add`、`git commit` 與 `git push`。

---

## 🚀 4. 如何新增考卷？
未來出卷時，您只需要：
1. 開啟 [build_exam.py](file:///G:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/codex-skills/gr12-exam-generator/build_exam.py)。
2. 修改腳本最上方的設定變數（第 16~19 行）：
   ```python
   SUBJECT = 'guoyu'               # 科目分類：'guoyu' (國語), 'math' (數學), 'life' (生活)
   EXAM_ID = 'KH115-L03'           # 考卷識別碼 (例如第 03 課)
   EXAM_TITLE = '一年七班 國語第03課 我的家' # 考卷標題
   DATE = '2026-06-18'             # 發布日期
   ```
3. 執行 Python 腳本：
   ```powershell
   python "G:\我的雲端硬碟\codex-skills\gr12-exam-generator\build_exam.py"
   ```
4. 跑完後，您的考卷與 QR Code 就已自動上傳到 GitHub。大約 30 秒至 1 分鐘後，您即可重新整理 `jsps-tools/tools/gr12-exams/` 入口網站，並在對應科目中看到它！
