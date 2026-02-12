#!/usr/bin/env python
"""Quick test to verify overdue detection is working"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_todo.settings')
django.setup()

from tasks.models import Task
from django.utils import timezone
from datetime import datetime

# Get all tasks
tasks = Task.objects.all()

print("\n=== OVERDUE DETECTION TEST ===")
now = timezone.now()
today = now.date()
print(f"Current time: {now}")
print(f"Current date: {today}\n")

for task in tasks:
    task.is_overdue = False
    if task.due_date and task.status != 'completed':
        if task.due_time:
            try:
                task_deadline = timezone.make_aware(
                    datetime.combine(task.due_date, task.due_time)
                )
                task.is_overdue = now > task_deadline
                print(f"Task: {task.title}")
                print(f"  Due: {task_deadline}")
                print(f"  Now: {now}")
                print(f"  IS_OVERDUE: {task.is_overdue}")
                print(f"  Status: {task.status}")
                print()
            except Exception as e:
                print(f"Error with task {task.title}: {e}")
        else:
            task.is_overdue = today > task.due_date
            if task.is_overdue:
                print(f"Task: {task.title}")
                print(f"  Due Date: {task.due_date}")
                print(f"  Today: {today}")
                print(f"  IS_OVERDUE: {task.is_overdue}")
                print()
