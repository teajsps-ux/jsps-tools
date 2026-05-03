$ErrorActionPreference = "Stop"

$toolDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backgroundDir = Join-Path $toolDir "backgrounds"
$manifestPath = Join-Path $backgroundDir "manifest.json"

$files = Get-ChildItem -LiteralPath $backgroundDir -File -Recurse |
    Where-Object { $_.Extension -match '^\.(jpg|jpeg|png|webp|gif)$' } |
    Sort-Object FullName

$items = foreach ($file in $files) {
    $baseUri = New-Object System.Uri (($toolDir.TrimEnd('\') + '\'))
    $fileUri = New-Object System.Uri $file.FullName
    $relativePath = [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($fileUri).ToString())
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $idBase = $relativePath.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
    $idBase = $idBase.Trim('-')

    [ordered]@{
        id = "manifest-$idBase"
        name = $baseName
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
