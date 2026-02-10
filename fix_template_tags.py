import re

# Read the file
with open('templates/tasks/task_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken template tag - replace all instances with spaces
content = content.replace('{ { task.time_limit } }', '{{ task.time_limit }}')
content = content.replace('{ {', '{{')
content = content.replace('} }', '}}')

# Write back
with open('templates/tasks/task_detail.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed template syntax errors!")
