param(
    [switch]$NoCommit,
    [switch]$NoPush,
    [datetime]$Date = (Get-Date)
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$sourceDir = Join-Path $repoRoot 'tools\mandarin-flashcard\backgrounds\solar-terms'
$target = Join-Path $PSScriptRoot 'bg.png'
$logDir = Join-Path $env:LOCALAPPDATA 'jsps-tools'
$logPath = Join-Path $logDir 'homework-matrix-weekly-bg.log'
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

function Write-RunLog([string]$Message) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Add-Content -LiteralPath $logPath -Encoding UTF8 -Value "[$stamp] $Message"
}

$terms = @(
    @{ Date='01-05'; Slug='xiaohan'; File='solar-01-xiaohan.png' },
    @{ Date='01-20'; Slug='dahan'; File='solar-02-dahan.png' },
    @{ Date='02-04'; Slug='lichun'; File='solar-03-lichun.png' },
    @{ Date='02-19'; Slug='yushui'; File='solar-04-yushui.png' },
    @{ Date='03-05'; Slug='jingzhe'; File='solar-05-jingzhe.png' },
    @{ Date='03-20'; Slug='chunfen'; File='solar-06-chunfen.png' },
    @{ Date='04-05'; Slug='qingming'; File='solar-07-qingming.png' },
    @{ Date='04-20'; Slug='guyu'; File='solar-08-guyu.png' },
    @{ Date='05-05'; Slug='lixia'; File='solar-09-lixia.png' },
    @{ Date='05-21'; Slug='xiaoman'; File='solar-10-xiaoman.png' },
    @{ Date='06-05'; Slug='mangzhong'; File='solar-11-mangzhong.png' },
    @{ Date='06-21'; Slug='xiazhi'; File='solar-12-xiazhi.png' },
    @{ Date='07-07'; Slug='xiaoshu'; File='solar-13-xiaoshu.png' },
    @{ Date='07-23'; Slug='dashu'; File='solar-14-dashu.png' },
    @{ Date='08-07'; Slug='liqiu'; File='solar-15-liqiu.png' },
    @{ Date='08-23'; Slug='chushu'; File='solar-16-chushu.png' },
    @{ Date='09-07'; Slug='bailu'; File='solar-17-bailu.png' },
    @{ Date='09-23'; Slug='qiufen'; File='solar-18-qiufen.png' },
    @{ Date='10-08'; Slug='hanlu'; File='solar-19-hanlu.png' },
    @{ Date='10-23'; Slug='shuangjiang'; File='solar-20-shuangjiang.png' },
    @{ Date='11-07'; Slug='lidong'; File='solar-21-lidong.png' },
    @{ Date='11-22'; Slug='xiaoxue'; File='solar-22-xiaoxue.png' },
    @{ Date='12-07'; Slug='daxue'; File='solar-23-daxue.png' },
    @{ Date='12-21'; Slug='dongzhi'; File='solar-24-dongzhi.png' }
)

$todayKey = $Date.ToString('MM-dd')
$term = $terms | Where-Object { $_.Date -le $todayKey } | Select-Object -Last 1
if (-not $term) { $term = $terms[-1] }

$source = Join-Path $sourceDir $term.File
if (-not (Test-Path -LiteralPath $source)) {
    throw "Missing solar-term image: $source"
}

$beforeHash = if (Test-Path -LiteralPath $target) { (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash } else { '' }
Copy-Item -LiteralPath $source -Destination $target -Force
$afterHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash

Write-RunLog "Selected $($term.Slug) $($term.File); changed=$($beforeHash -ne $afterHash)"

if ($beforeHash -eq $afterHash) {
    Write-Output "No change: homework-matrix/bg.png already uses $($term.Slug)."
    return
}

Write-Output "Updated homework-matrix/bg.png to $($term.Slug) ($($term.File))."

if ($NoCommit) {
    Write-Output 'NoCommit set; leaving file changed without commit.'
    return
}

Push-Location $repoRoot
try {
    git add tools/homework-matrix/bg.png
    git commit -m "Update homework matrix background for $($term.Slug)"
    if (-not $NoPush) {
        git push origin main
    }
} finally {
    Pop-Location
}