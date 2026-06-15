@echo off
title Knowledge King AI Helper

echo ========================================================
echo   Starting Knowledge King AI Helper Server...
echo   Please keep this window open while using the tool.
echo ========================================================
echo.

:: 1. Check if API key file exists
set "ENV_FILE=%USERPROFILE%\.openai.env"
if not exist "%ENV_FILE%" (
  echo [ERROR] Cannot find OpenAI API key file:
  echo %ENV_FILE%
  echo.
  echo Please create a file named ".openai.env" in your user folder,
  echo and add "OPENAI_API_KEY=your_key" inside it.
  echo.
  pause
  exit /b
)

:: 2. Change directory to script folder
cd /d "%~dp0"

:: 3. Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
  echo [ERROR] Node.js is not installed!
  echo Please download and install Node.js from https://nodejs.org/
  echo.
  pause
  exit /b
)

:: 4. Start local server
node local-quiz-csv-server.mjs

if %errorlevel% neq 0 (
  echo [ERROR] Server failed to start or crashed.
)
echo.
pause
