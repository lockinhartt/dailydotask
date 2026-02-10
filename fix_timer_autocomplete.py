import re

# Read the file
with open('templates/tasks/task_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the auto-stop logic
old_code = """            // Auto-stop when estimated duration is reached
            if (estimatedDuration !== null) {
                const elapsedMinutes = Math.floor(elapsed / 60);
                if (elapsedMinutes >= estimatedDuration) {
                    // Time limit reached! Auto-stop and complete
                    stopTimer();
                }
            }"""

new_code = """            // Auto-stop when estimated duration is reached
            if (estimatedDuration !== null) {
                const elapsedMinutes = Math.floor(elapsed / 60);
                if (elapsedMinutes >= estimatedDuration) {
                    // Time limit reached! Auto-stop and complete the task
                    stopTimer();
                    
                    // Auto-complete the task
                    updateStatus('completed');
                    
                    // Show alert to user
                    const taskTitle = document.querySelector('.task-title').textContent;
                    alert(`⏱️ Time limit reached! Task has been automatically completed.`);
                    
                    // Reload page to show completed status
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                }
            }"""

# Replace
content = content.replace(old_code, new_code)

# Write back
with open('templates/tasks/task_detail.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated auto-stop timer logic successfully!")
