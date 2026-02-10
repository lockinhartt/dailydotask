$file = "templates\tasks\index.html"
$content = Get-Content $file -Raw -Encoding UTF8

# Replace ALL instances - be aggressive
$content = $content -replace "current_filter=='all'", "current_filter == 'all'"
$content = $content -replace "current_filter=='pending'", "current_filter == 'pending'"
$content = $content -replace "current_filter=='in_progress'", "current_filter == 'in_progress'"
$content = $content -replace "current_filter=='completed'", "current_filter == 'completed'"
$content = $content -replace "current_filter=='overdue'", "current_filter == 'overdue'"

# Fix split endif tags
$content = $content -replace "selected\{%\s+endif %\}>", "selected{% endif %}>"

# Write back with UTF8 NO BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\$file", $content, $utf8NoBom)

Write-Host "✅ NUCLEAR FIX COMPLETE!" -ForegroundColor Green
Write-Host "Verifying..." -ForegroundColor Yellow

# Verify
$verify = Get-Content $file -Raw
if ($verify -match "current_filter==") {
    Write-Host "❌ ERROR: Still found instances without spaces!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ SUCCESS: All fixed!" -ForegroundColor Green
}
