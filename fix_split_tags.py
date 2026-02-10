with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the split endif tag on line 925-926
content = content.replace(
    '{% if current_filter == \'in_progress\' %}selected{% endif\n                        %}>',
    '{% if current_filter == \'in_progress\' %}selected{% endif %}>'
)

# Also fix the split endif on line 918-919 just in case
content = content.replace(
    '{% if not current_filter or current_filter == \'all\' %}selected{%\n                        endif %}>',
    '{% if not current_filter or current_filter == \'all\' %}selected{% endif %}>'
)

with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all split template tags!")
