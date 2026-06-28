$content = Get-Content "index.html" -Raw -Encoding UTF8
$content = $content -replace 'speak(\`\\$\{title\}-\$\{text\}\`)', 'speak(title + ''-'' + text)'
$content = $content -replace \"speak\('松下問童子。在松樹下問小童。'\)\", "speak(poem[0].line)"
$content = $content -replace \"speak\('言師採藥去。童子說，老師採藥去了。'\)\", "speak(poem[1].line)"
$content = $content -replace \"speak\('只在此山中。只知道他就在這座山裡。'\)\", "speak(poem[2].line)"
$content = $content -replace \"speak\('雲深不知處。雲霧太深，不知道他在哪裡。'\)\", "speak(poem[3].line)"
$content = $content -replace \"speak\('當時的心情。詩人來找隱居的人，卻只看到松樹、山路和雲霧。他有點失望，但也感受到山裡很安靜、很美。'\)\", "speak('當時的心情。詩人來找隱居的人，卻只看到松樹、山路和雲霧。他有點失望，但也感受到山裡很安靜、很美。')"
$content = $content -replace \"speak\('我們學到。有時候找不到人，不一定是壞事。可以學會耐心等待，也可以欣賞路上的風景。'\)\", "speak('我們學到。有時候找不到人，不一定是壞事。可以學會耐心等待，也可以欣賞路上的風景。')"
Set-Content "index.html" -Value $content -Encoding UTF8