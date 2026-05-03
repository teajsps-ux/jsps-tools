$ErrorActionPreference = "Stop"

$toolDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backgroundDir = Join-Path $toolDir "backgrounds"
$manifestPath = Join-Path $backgroundDir "manifest.json"

$files = Get-ChildItem -LiteralPath $backgroundDir -File -Recurse |
    Where-Object { $_.Extension -match '^\.(jpg|jpeg|png|webp|gif)$' } |
    Sort-Object FullName

$knownNames = @{
    "backgrounds/bgg-snow.jpg" = "雪山衝刺"
    "backgrounds/bg-math-0.jpg" = "溫柔房間"
    "backgrounds/bg-math-1.jpg" = "貓咪格紋"
    "backgrounds/bg-math-2.jpg" = "花束祝福"
    "backgrounds/bg-math-3.jpg" = "夏日校園"
    "backgrounds/bg-math-5.jpg" = "山屋雪地"
    "backgrounds/bg6.jpg" = "海風咖啡"
    "backgrounds/bg7.jpg" = "黑衫守衛"
    "backgrounds/bg8.jpg" = "城市咖啡"
    "backgrounds/bg9.jpg" = "訓練場守護"
    "backgrounds/bg10.jpg" = "白衫辦公"
}

$sharedIndex = 1
$items = foreach ($file in $files) {
    $baseUri = New-Object System.Uri (($toolDir.TrimEnd('\') + '\'))
    $fileUri = New-Object System.Uri $file.FullName
    $relativePath = [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($fileUri).ToString())
    $idBase = $relativePath.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
    $idBase = $idBase.Trim('-')
    $displayName = $knownNames[$relativePath]
    if (-not $displayName) {
        if ($relativePath -like "backgrounds/solar-terms/*") {
            $displayName = "節氣背景 $sharedIndex"
        } else {
            $displayName = "共用背景 $sharedIndex"
        }
        $sharedIndex += 1
    }

    [ordered]@{
        id = "manifest-$idBase"
        name = $displayName
        url = $relativePath
        season = "spring"
    }
}

$json = $items | ConvertTo-Json -Depth 4
if (-not $json) {
    $json = "[]"
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($manifestPath, $json, $utf8NoBom)
Write-Host "Updated $manifestPath with $($items.Count) background images."

