@login_required
def filtered_tasks(request, filter_type='all'):
    """View displaying filtered tasks based on status."""
    from django.utils import timezone
    from datetime import datetime
    
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()
    
    # Calculate stats
    now = timezone.now()
    today = now.date()
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='pending').count()
    completed_today = tasks.filter(status='completed', updated_at__date=today).count()
    
    # Add overdue status and filter tasks
    tasks_with_status = []
    for task in tasks:
        task.is_overdue = False
        if task.due_date and task.status != 'completed':
            if task.due_time:
                task_deadline = timezone.make_aware(
                    datetime.combine(task.due_date, task.due_time)
                )
                task.is_overdue = now > task_deadline
            else:
                task.is_overdue = today > task.due_date
        
        # Filter by type
        include_task = False
        if filter_type == 'all':
            include_task = True
        elif filter_type == 'pending':
            include_task = task.status == 'pending'
        elif filter_type == 'in_progress':
            include_task = task.status == 'in_progress'
        elif filter_type == 'completed':
            include_task = task.status == 'completed'
        elif filter_type == 'overdue':
            include_task = task.is_overdue
        
        if include_task:
            tasks_with_status.append(task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            
            task.ai_suggested_priority = predict_priority(task.title, task.description)
            task.ai_category = categorize_task(task.title, task.description)
            difficulty = estimate_difficulty(task.title, task.description)
            task.ai_difficulty = difficulty['level']
            task.ai_difficulty_score = difficulty['score']
            task.ai_difficulty_reasons = ', '.join(difficulty['reasons'])
            
            task.save()
            if filter_type == 'all':
                return redirect('index')
            else:
                return redirect('tasks_' + filter_type)
    
    context = {
        'tasks': tasks_with_status,
        'form': form,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_today': completed_today,
        'current_filter': filter_type,
    }
    return render(request, 'tasks/index.html', context)
