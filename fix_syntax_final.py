import re

# Read the file
with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all instances of current_filter== to have proper spacing
content = content.replace("current_filter=='all'", "current_filter == 'all'")
content = content.replace("current_filter=='pending'", "current_filter == 'pending'")
content = content.replace("current_filter=='in_progress'", "current_filter == 'in_progress'")
content = content.replace("current_filter=='completed'", "current_filter == 'completed'")
content = content.replace("current_filter=='overdue'", "current_filter == 'overdue'")

# Write back
with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template syntax fixed!")
