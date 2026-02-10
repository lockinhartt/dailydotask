@login_required
def task_detail(request, pk):
    """Detailed view of a single task with all controls."""
    from django.utils import timezone
    from datetime import datetime
    
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Calculate if task is overdue
    now = timezone.now()
    today = now.date()
    task.is_overdue = False
    if task.due_date and task.status != 'completed':
        if task.due_time:
            task_deadline = timezone.make_aware(
                datetime.combine(task.due_date, task.due_time)
            )
            task.is_overdue = now > task_deadline
        else:
            task.is_overdue = today > task.due_date
    
    context = {
        'task': task,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def update_task_status(request, pk):
    """Update task status via AJAX."""
    from django.http import JsonResponse
    
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        new_status = request.POST.get('status')
        
        if new_status in ['pending', 'in_progress', 'completed']:
            task.status = new_status
            task.save()
            
            return JsonResponse({
                'status': 'success',
                'new_status': new_status,
                'display_status': task.get_status_display()
            })
    
    return JsonResponse({'status': 'error'}, status=400)
