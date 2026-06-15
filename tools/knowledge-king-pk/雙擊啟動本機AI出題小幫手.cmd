@echo off
chcp 65001 > nul
title 知識王 AI 出題本機小幫手
echo ========================================================
echo   正在啟動「知識王 PK 賽」AI 出題本機小幫手...
echo   請保持此視窗開啟，不要關閉它喔！
echo ========================================================
echo.

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "start-local-quiz-helper.ps1"

echo.
echo 提示：連線可能中斷或發生錯誤，請按任意鍵關閉視窗。
pause
