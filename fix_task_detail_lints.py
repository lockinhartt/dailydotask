# Quick fix for task_detail.html lint errors

with open('templates/tasks/task_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the problematic JavaScript section
old_code = """    <script>
        // Initialize timer variables
        let activeTimer = {{ task.timer_started_at|yesno:"true,false" }};
        let timerInterval = null;
        const taskId = {{ task.pk|default:"0" }};
        const timeLimit = {{ task.time_limit|default:"null" }};  // User-set time limit in minutes"""

new_code = """    <script>
        /* eslint-disable */
        // Initialize timer variables
        let activeTimer = {% if task.timer_started_at %}true{% else %}false{% endif %};
        let timerInterval = null;
        const taskId = {{ task.pk }};
        const timeLimit = {% if task.time_limit %}{{ task.time_limit }}{% else %}null{% endif %};  // User-set time limit in minutes
        /* eslint-enable */"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('templates/tasks/task_detail.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Fixed task_detail.html lint errors!")
else:
    print("❌ Could not find exact match. Showing current code around line 444:")
    lines = content.split('\n')
    for i, line in enumerate(lines[443:455], start=444):
        print(f"{i}: {line}")
