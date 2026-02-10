import re

# Read the file
with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing ALL spacing issues in template...")

# Fix all instances of current_filter== to current_filter ==
content = re.sub(r"current_filter=='", "current_filter == '", content)
content = re.sub(r"current_filter==\"", 'current_filter == "', content)

# Fix split endif tags - merge them
content = re.sub(r'{%\s*endif\s*\n\s*%}', '{% endif %}', content)

# Write back
with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ALL template errors fixed!")

# Touch the file to update modification time
import os
os.utime('templates/tasks/index.html', None)
print("✅ File modification time updated to force Django reload!")
