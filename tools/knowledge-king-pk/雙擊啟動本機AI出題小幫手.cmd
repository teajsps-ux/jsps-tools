@echo off
chcp 65001 > nul
title 知識王 AI 出題本機小幫手

echo ========================================================
echo   正在啟動「知識王 PK 賽」AI 出題本機小幫手...
echo   請保持此視窗開啟，不要關閉它喔！
echo ========================================================
echo.

:: 1. 檢查金鑰檔案是否存在
set "ENV_FILE=%USERPROFILE%\.openai.env"
if not exist "%ENV_FILE%" (
  echo [錯誤] 找不到金鑰檔案：%ENV_FILE%
  echo 請先在您的個人資料夾中建立此檔案，並在內部填入您的 OPENAI_API_KEY。
  echo.
  pause
  exit /b
)

:: 2. 進入專案目錄
cd /d "%~dp0"

:: 3. 檢查 Node.js 是否已安裝
where node >nul 2>nul
if %errorlevel% neq 0 (
  echo [錯誤] 偵測不到 Node.js！
  echo 請先至官網下載並安裝 Node.js (https://nodejs.org/) 後，再重新執行此檔案。
  echo.
  pause
  exit /b
)

:: 4. 啟動伺服器
node local-quiz-csv-server.mjs

if %errorlevel% neq 0 (
  echo [錯誤] 伺服器啟動失敗或異常中止！
)
echo.
pause
