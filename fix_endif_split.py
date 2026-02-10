import re

# Read the file
with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing split endif tags on line 918-919...")

# Fix the specific split tag pattern: selected{% \n    endif %}
# This regex looks for patterns like: {%<newline><whitespace>endif<whitespace>%}
content = re.sub(r'\{%\s*\n\s*endif\s*%\}', '{% endif %}', content)

# Also fix patterns like: selected{%<newline>endif %}
content = re.sub(r'selected\{%\s*\n\s*endif\s*%\}', 'selected{% endif %}', content)

# Write back
with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed split endif tags!")

# Touch the file
import os
os.utime('templates/tasks/index.html', None)
print("✅ File touched to force reload!")
