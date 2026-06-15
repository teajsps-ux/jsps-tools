# 知識王 PK 賽 AI 出題小幫手

這個小幫手讓網頁把圖片或 PDF 教材交給 OpenAI，產生 20 題 CSV 題庫。

API Key 放在：

```text
C:\Users\ketty\.openai.env
```

不要把 API Key 寫進 HTML，也不要 commit 進 GitHub。

## 啟動

從 repo 根目錄執行：

```powershell
powershell -ExecutionPolicy Bypass -File tools\knowledge-king-pk\start-local-quiz-helper.ps1
```

保持 PowerShell 視窗開著，再回到網頁按「AI 轉成 CSV」。

## 輸出格式

小幫手會要求 AI 輸出：

```csv
題目,選項A,選項B,選項C,選項D,正確答案
```

「正確答案」欄位會是完整選項文字，不是 A/B/C/D。
