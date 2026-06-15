$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = Join-Path $env:USERPROFILE ".openai.env"

if (-not (Test-Path $envFile)) {
  Write-Host "找不到 $envFile"
  Write-Host "請先建立這個檔案，裡面放 OPENAI_API_KEY 這一行。"
  exit 1
}

Set-Location $scriptDir
node .\local-quiz-csv-server.mjs
