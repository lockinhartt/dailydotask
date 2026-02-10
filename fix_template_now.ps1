# Fix template syntax in index.html
$file = "templates\tasks\index.html"
$content = Get-Content $file -Raw -Encoding UTF8

# Replace all instances of current_filter== with current_filter ==
$content = $content -replace "current_filter=='all'", "current_filter == 'all'"
$content = $content -replace "current_filter=='pending'", "current_filter == 'pending'"
$content = $content -replace "current_filter=='in_progress'", "current_filter == 'in_progress'"
$content = $content -replace "current_filter=='completed'", "current_filter == 'completed'"
$content = $content -replace "current_filter=='overdue'", "current_filter == 'overdue'"

# Also fix the split endif tag
$content = $content -replace "selected{%\r?\n\s+endif %}>", "selected{% endif %}>"

# Write back
Set-Content $file $content -Encoding UTF8 -NoNewline

Write-Host "✅ Template fixed successfully!"
