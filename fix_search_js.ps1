$file = "templates\tasks\index.html"
$content = Get-Content $file -Raw -Encoding UTF8

Write-Host "Adding null checks to search JavaScript..." -ForegroundColor Yellow

# Fix lines 1227-1229: add null checks
$old = @"
            const searchTerm = searchInput.value.toLowerCase();
            const priorityFilter = filterPriority.value;
            const sortOption = sortBy.value;
"@

$new = @"
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            const priorityFilter = filterPriority ? filterPriority.value : 'all';
            const sortOption = sortBy ? sortBy.value : 'created';
"@

$content = $content.Replace($old, $new)

# Fix the event listeners (around line 1320-1322)
$oldListeners = @"
        searchInput.addEventListener('input', filterAndSortTasks);
        filterPriority.addEventListener('change', filterAndSortTasks);
        sortBy.addEventListener('change', filterAndSortTasks);
"@

$newListeners = @"
        if (searchInput) searchInput.addEventListener('input', filterAndSortTasks);
        if (filterPriority) filterPriority.addEventListener('change', filterAndSortTasks);
        if (sortBy) sortBy.addEventListener('change', filterAndSortTasks);
"@

$content = $content.Replace($oldListeners, $newListeners)

# Write back
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\$file", $content, $utf8NoBom)

Write-Host "✅ Added null checks to search JavaScript!" -ForegroundColor Green
