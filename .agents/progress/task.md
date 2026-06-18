# 實作任務清單

- [x] 建立資料夾結構 (guoyu, math, life)
- [x] 修改主入口網頁 `jsps-tools/index.html`，新增「低年級互動考卷」卡片
- [x] 建立 `jsps-tools/tools/gr12-exams/exams_list.json` 初始化檔案
- [x] 建立二級分類入口網頁 `jsps-tools/tools/gr12-exams/index.html` (讀取 json 動態呈現)
- [x] 升級 `build_exam.py` 腳本：
  - [x] 支援科目子目錄寫入
  - [x] 自動呼叫 API 下載 QR Code PNG
  - [x] 自動更新 `exams_list.json` 清單
  - [x] 自動執行 Git commit 與 push
- [x] 測試與驗證：執行 Python 出卷腳本並檢查網頁與 Git 推送結果
