$file = "templates\tasks\index.html"
$content = Get-Content $file -Raw -Encoding UTF8

Write-Host "Fixing split endif tags..." -ForegroundColor Yellow

# Fix the SPECIFIC split endif on line 924-925
$content = $content -replace "(\{%\s*if\s+current_filter\s*==\s*'in_progress'\s*%\}selected\{%\s*endif)\s+(%\}>)", '$1 $2'

# More aggressive: fix ANY split endif tags (across newlines)
$content = $content -replace "(\{%\s*endif)\r?\n\s+(%\}>)", '$1 $2'
$content = $content -replace "(\{%\s*endif)\s{2,}(%\}>)", '$1 $2'

# Write back
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\$file", $content, $utf8NoBom)

Write-Host "✅ Fixed split endif tags!" -ForegroundColor Green

# Show the specific line
Write-Host "`nLine 924-925 content:" -ForegroundColor Cyan
$lines = Get-Content $file
$lines[923..925] | ForEach-Object { Write-Host $_ }
