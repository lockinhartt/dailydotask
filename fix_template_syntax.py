#!/usr/bin/env python
# Quick script to fix Django template syntax errors

with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all template syntax errors by adding spaces around ==
replacements = [
    ("current_filter=='all'", "current_filter == 'all'"),
    ("current_filter=='pending'", "current_filter == 'pending'"),
    ("current_filter=='in_progress'", "current_filter == 'in_progress'"),
    ("current_filter=='completed'", "current_filter == 'completed'"),
    ("current_filter=='overdue'", "current_filter == 'overdue'"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template syntax fixed!")
print("Fixed all current_filter== instances to have proper spacing")
