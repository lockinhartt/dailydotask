@login_required
def start_timer(request, pk):
    """Start the timer for a task."""
    from django.http import JsonResponse
    from django.utils import timezone
    from django.db import models
    
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Stop any other running timers for this user
    Task.objects.filter(user=request.user, timer_started_at__isnull=False).exclude(pk=pk).update(
        timer_started_at=None
    )
    
    # Start timer for this task
    task.timer_started_at = timezone.now()
    task.save()
    
    return JsonResponse({
        'status': 'started',
        'task_id': task.pk,
        'started_at': task.timer_started_at.isoformat()
    })


@login_required
def stop_timer(request, pk):
    """Stop the timer for a task and save elapsed time."""
    from django.http import JsonResponse
    from django.utils import timezone
    
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if task.timer_started_at:
        # Calculate elapsed time in minutes
        elapsed = timezone.now() - task.timer_started_at
        elapsed_minutes = int(elapsed.total_seconds() / 60)
        
        # Add to existing time spent
        task.time_spent += elapsed_minutes
        task.timer_started_at = None
        task.save()
        
        return JsonResponse({
            'status': 'stopped',
            'task_id': task.pk,
            'time_spent': task.time_spent,
            'elapsed_minutes': elapsed_minutes
        })
    
    return JsonResponse({'status': 'not_running', 'task_id': task.pk})
