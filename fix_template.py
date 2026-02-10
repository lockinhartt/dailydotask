import re

#Read the file
with open('c:\\Users\\Janna\\dailydotask\\templates\\tasks\\task_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the problematic line
old_line = 'const estimatedDuration = {{ task.estimated_duration|default: "null" }}; // in minutes'
new_line = 'const estimatedDuration = {% if task.estimated_duration %}{{ task.estimated_duration }}{% else %}null{% endif %}; // in minutes'

content = content.replace(old_line, new_line)

# Write back
with open('c:\\Users\\Janna\\dailydotask\\templates\\tasks\\task_detail.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
