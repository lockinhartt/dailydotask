#!/usr/bin/env python
# Fix all broken template tags in task_detail.html

with open('templates/tasks/task_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix any broken template tags with spaces
content = content.replace('{ {', '{{')
content = content.replace('} }', '}}')
content = content.replace('{  {', '{{')
content = content.replace('}  }', '}}')

with open('templates/tasks/task_detail.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all broken template tags!")
