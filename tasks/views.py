from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from .ml import predict_priority, categorize_task, estimate_difficulty


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'tasks/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def index(request):
    """Main view displaying all tasks for the logged-in user."""
    from django.utils import timezone
    from datetime import timedelta
    
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()
    
    # Calculate stats
    today = timezone.now().date()
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='pending').count()
    completed_today = tasks.filter(status='completed', updated_at__date=today).count()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            
            # Apply AI predictions
            task.ai_suggested_priority = predict_priority(task.title, task.description)
            task.ai_category = categorize_task(task.title, task.description)
            
            # Estimate difficulty using NLP
            difficulty = estimate_difficulty(task.title, task.description)
            task.ai_difficulty = difficulty['level']
            task.ai_difficulty_score = difficulty['score']
            task.ai_difficulty_reasons = ', '.join(difficulty['reasons'])
            
            task.save()
            return redirect('index')
    
    context = {
        'tasks': tasks,
        'form': form,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_today': completed_today,
    }
    return render(request, 'tasks/index.html', context)


@login_required
def update_task(request, pk):
    """Update a task."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    return redirect('index')


@login_required
def delete_task(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('index')


@login_required
def toggle_status(request, pk):
    """Toggle task completion status."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if task.status == 'completed':
        task.status = 'pending'
    else:
        task.status = 'completed'
    
    task.save()
    return redirect('index')
