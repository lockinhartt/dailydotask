import sys

# Read file
with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences
count_without_space = content.count("current_filter==")
print(f"Found {count_without_space} occurrences of 'current_filter==' without spaces")

# Fix ALL occurrences
content = content.replace("current_filter=='all'", "current_filter == 'all'")
content = content.replace("current_filter=='pending'", "current_filter == 'pending'")
content = content.replace("current_filter=='in_progress'", "current_filter == 'in_progress'")
content = content.replace("current_filter=='completed'", "current_filter == 'completed'")
content = content.replace("current_filter=='overdue'", "current_filter == 'overdue'")

# Verify changes
after_count = content.count("current_filter==")
print(f"After fix: {after_count} occurrences remaining")

# Write back
with open('templates/tasks/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ File fixed and saved!")

# Verify by reading back
with open('templates/tasks/index.html', 'r', encoding='utf-8') as f:
    verify = f.read()
    final_count = verify.count("current_filter==")
    print(f"Verification: {final_count} occurrences of 'current_filter==' found")
    if final_count == 0:
        print("SUCCESS! All syntax errors fixed!")
    else:
        print("WARNING: Some errors may remain")
        sys.exit(1)
