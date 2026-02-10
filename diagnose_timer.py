# Quick diagnostic for timer button issues

with open('templates/tasks/task_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for common issues
issues = []

# 1. Check for broken template tags
if '{ {' in content or '} }' in content:
    issues.append("❌ Found broken template tags with spaces")
else:
    issues.append("✅ Template tags look good")

# 2. Check if toggleTimer function exists
if 'function toggleTimer()' in content:
    issues.append("✅ toggleTimer function exists")
else:
    issues.append("❌ toggleTimer function not found")

# 3. Check if startTimer function exists  
if 'function startTimer()' in content:
    issues.append("✅ startTimer function exists")
else:
    issues.append("❌ startTimer function not found")

# 4. Check button onclick
if 'onclick="toggleTimer()"' in content:
    issues.append("✅ Button has onclick handler")
else:
    issues.append("❌ Button onclick missing")

# 5. Check for syntax errors in timeLimit line
if 'const timeLimit = {% if task.time_limit %}{{ task.time_limit }}{% else %}null{% endif %}' in content:
    issues.append("✅ timeLimit variable syntax correct")
else:
    issues.append("❌ timeLimit variable has syntax issue")

print("\n".join(issues))
