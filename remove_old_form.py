#!/usr/bin/env python
# Script to remove the old task creation form from index.html

with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove lines 808-848 (the old form)
# Keep everything before line 808 and after line 848
new_lines = lines[:807] + lines[849:]

with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Removed old task creation form!")
print(f"Removed {len(lines) - len(new_lines)} lines")
