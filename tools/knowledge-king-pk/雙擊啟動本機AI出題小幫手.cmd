@echo off
chcp 65001 > nul
title 知識王 AI 出題本機小幫手 - 診斷與啟動
echo ========================================================
echo   正在診斷並啟動「知識王 PK 賽」AI 本機小幫手...
echo ========================================================
echo.

cd /d "%~dp0"

:: 1. 檢查 Node.js 是否安裝
where node >nul 2>nul
if %errorlevel% neq 0 (
  echo ❌ [錯誤] 您的電腦尚未安裝 Node.js！
  echo    本機 AI 功能需要安裝 Node.js 軟體才能運作。
  echo    請點選以下連結下載並安裝（建議安裝 LTS 穩定版）：
  echo    👉 https://nodejs.org/
  echo.
  goto end
)

:: 2. 顯示 Node.js 版本
echo 🟢 [診斷] 偵測到 Node.js，版本為：
node -v
echo.

:: 3. 檢查 .openai.env 設定檔
if not exist "%USERPROFILE%\.openai.env" (
  echo ❌ [錯誤] 找不到 API 金鑰設定檔！
  echo    請在個人資料夾「%USERPROFILE%」下
  echo    建立一個名為「.openai.env」的純文字檔，
  echo    並在第一行輸入您的金鑰：OPENAI_API_KEY=您的金鑰值
  echo.
  goto end
)
echo 🟢 [診斷] 偵測到 API 金鑰設定檔。
echo.

:: 4. 啟動伺服器
echo 🚀 正在啟動小幫手伺服器...
echo --------------------------------------------------------
powershell -NoProfile -ExecutionPolicy Bypass -File "start-local-quiz-helper.ps1"

:end
echo.
echo --------------------------------------------------------
echo 提示：小幫手已結束或啟動失敗。
echo 請查看上方錯誤訊息，或拍照/截圖此視窗回傳給設計人員。
echo 按任意鍵關閉此視窗...
pause > nul
