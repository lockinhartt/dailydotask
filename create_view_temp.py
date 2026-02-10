@login_required
def create_task_view(request):
    """Dedicated view for creating new tasks."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            
            # Apply AI predictions
            task.ai_suggested_priority = predict_priority(task.title, task.description)
            task.ai_category = categorize_task(task.title, task.description)
            difficulty = estimate_difficulty(task.title, task.description)
            task.ai_difficulty = difficulty['level']
            task.ai_difficulty_score = difficulty['score']
            task.ai_difficulty_reasons = ', '.join(difficulty['reasons'])
            
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('index')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/create_task.html', {'form': form})
