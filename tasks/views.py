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
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
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
    from datetime import datetime, timedelta
    
    tasks = Task.objects.filter(user=request.user, is_archived=False)
    form = TaskForm()
    
    # Calculate stats
    now = timezone.now()
    today = now.date()
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='pending').count()
    completed_today = tasks.filter(status='completed', updated_at__date=today).count()
    
    # Add overdue status to each task
    tasks_with_status = []
    for task in tasks:
        task.is_overdue = False
        if task.due_date and task.status != 'completed':
            if task.due_time:
                # Combine date and time for comparison
                try:
                    task_deadline = timezone.make_aware(
                        datetime.combine(task.due_date, task.due_time)
                    )
                    task.is_overdue = now > task_deadline
                    # Debug output
                    if task.is_overdue:
                        print(f"[INDEX] Task '{task.title}' is OVERDUE: deadline={task_deadline}, now={now}")
                except Exception as e:
                    # If timezone conversion fails, use naive comparison
                    task_deadline_naive = datetime.combine(task.due_date, task.due_time)
                    task.is_overdue = timezone.localtime(now).replace(tzinfo=None) > task_deadline_naive
                    if task.is_overdue:
                        print(f"[INDEX] Task '{task.title}' is OVERDUE (naive): deadline={task_deadline_naive}, error={e}")
            else:
                # Only date set, compare dates (task is overdue if today is AFTER due date)
                task.is_overdue = today > task.due_date
                if task.is_overdue:
                    print(f"[INDEX] Task '{task.title}' is OVERDUE: due_date={task.due_date}, today={today}")
        tasks_with_status.append(task)
    
    context = {
        'tasks': tasks_with_status,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_today': completed_today,
    }
    return render(request, 'tasks\index.html', context)


@login_required
def create_task_view(request):
    """Dedicated page for creating a new task."""
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
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('index')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def update_task(request, pk):
    """Update a task."""
    from django.http import JsonResponse
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'GET':
        # Return task data as JSON for modal
        return JsonResponse({
            'id': task.pk,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else '',
            'due_time': task.due_time.isoformat() if task.due_time else '',
            'estimated_duration': task.estimated_duration or '',
            'time_limit': task.time_limit or '',
        })
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    return redirect('index')


@login_required
def delete_task(request, pk):
    """Archive a task (soft delete)."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.is_archived = True
        task.save()
    return redirect('index')



@login_required
def toggle_status(request, pk):
    """Cycle task status through all states."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Cycle: pending -> in_progress -> completed -> pending
    if task.status == 'pending':
        task.status = 'in_progress'
    elif task.status == 'in_progress':
        task.status = 'completed'
    else:
        task.status = 'pending'
    
    task.save()
    return redirect('index')
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
                # Combine date and time for comparison
                try:
                    task_deadline = timezone.make_aware(
                        datetime.combine(task.due_date, task.due_time)
                    )
                    task.is_overdue = now > task_deadline
                    # Debug output
                    if task.is_overdue:
                        print(f"Task '{task.title}' is OVERDUE: deadline={task_deadline}, now={now}")
                except Exception as e:
                    # If timezone conversion fails, use naive comparison
                    task_deadline_naive = datetime.combine(task.due_date, task.due_time)
                    task.is_overdue = timezone.localtime(now).replace(tzinfo=None) > task_deadline_naive
                    if task.is_overdue:
                        print(f"Task '{task.title}' is OVERDUE (naive): deadline={task_deadline_naive}")
            else:
                # Only date set, compare dates (task is overdue if today is AFTER due date)
                task.is_overdue = today > task.due_date
                if task.is_overdue:
                    print(f"Task '{task.title}' is OVERDUE: due_date={task.due_date}, today={today}")
        
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
@login_required
def start_timer(request, pk):
    """Start the timer for a task."""
    from django.http import JsonResponse
    from django.utils import timezone
    
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Stop any other running timers for this user
    Task.objects.filter(user=request.user, timer_started_at__isnull=False).update(
        time_spent=models.F('time_spent') + 0,  # Keep existing time
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
            try:
                task_deadline = timezone.make_aware(
                    datetime.combine(task.due_date, task.due_time)
                )
                task.is_overdue = now > task_deadline
                print(f"[DETAIL] Task '{task.title}': due={task_deadline}, now={now}, is_overdue={task.is_overdue}")
            except Exception as e:
                task_deadline_naive = datetime.combine(task.due_date, task.due_time)
                task.is_overdue = timezone.localtime(now).replace(tzinfo=None) > task_deadline_naive
                print(f"[DETAIL] Task '{task.title}' (naive): is_overdue={task.is_overdue}, error={e}")
        else:
            task.is_overdue = today > task.due_date
            print(f"[DETAIL] Task '{task.title}': due_date={task.due_date}, today={today}, is_overdue={task.is_overdue}")
    
    # Check if time spent has exceeded estimated duration
    task.is_duration_exceeded = False
    task.duration_progress = 0
    if task.estimated_duration and task.estimated_duration > 0:
        task.duration_progress = int((task.time_spent / task.estimated_duration) * 100)
        task.is_duration_exceeded = task.time_spent >= task.estimated_duration
        print(f"[DETAIL] Duration check: spent={task.time_spent}m, estimated={task.estimated_duration}m, exceeded={task.is_duration_exceeded}, progress={task.duration_progress}%")
    
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
        return JsonResponse({'error': 'Invalid status provided'}, status=400) # Modified line
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405) # Modified line


@login_required
def archive_list(request):
    """Display all archived tasks for the current user."""
    archived_tasks = Task.objects.filter(user=request.user, is_archived=True).order_by('-updated_at')
    
    context = {
        'archived_tasks': archived_tasks,
        'archived_count': archived_tasks.count(),
    }
    return render(request, 'tasks/archive.html', context)


@login_required
def restore_task(request, pk):
    """Restore an archived task to the active task list."""
    task = get_object_or_404(Task, pk=pk, user=request.user, is_archived=True)
    if request.method == 'POST':
        task.is_archived = False
        task.save()
        messages.success(request, f'Task "{task.title}" has been restored!')
    return redirect('archive_list')


@login_required
def permanent_delete(request, pk):
    """Permanently delete a task from the database."""
    task = get_object_or_404(Task, pk=pk, user=request.user, is_archived=True)
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" has been permanently deleted!')
    return redirect('archive_list')
@login_required
def start_timer(request, pk):
    """Start the timer for a task."""
    from django.http import JsonResponse
    from django.utils import timezone
    from django.db import models
    
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Check if task is overdue - block timer start if past due date
    from datetime import datetime
    if task.due_date and task.status != 'completed':
        now = timezone.now()
        today = now.date()
        is_overdue = False
        
        if task.due_time:
            try:
                task_deadline = timezone.make_aware(
                    datetime.combine(task.due_date, task.due_time)
                )
                is_overdue = now > task_deadline
            except Exception:
                task_deadline_naive = datetime.combine(task.due_date, task.due_time)
                is_overdue = timezone.localtime(now).replace(tzinfo=None) > task_deadline_naive
        else:
            is_overdue = today > task.due_date
        
        if is_overdue:
            due_str = f"{task.due_date}"
            if task.due_time:
                due_str += f" at {task.due_time.strftime('%I:%M %p')}"
            
            return JsonResponse({
                'status': 'error',
                'error': 'task_overdue',
                'message': f'This task is overdue (was due: {due_str}). Please update the due date to continue working.',
                'due_date': str(task.due_date),
                'due_time': task.due_time.isoformat() if task.due_time else None
            }, status=400)
    
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
        # Automatically mark as completed when timer stops
        task.status = 'completed'
        task.save()
        
        return JsonResponse({
            'status': 'stopped',
            'task_id': task.pk,
            'time_spent': task.time_spent,
            'elapsed_minutes': elapsed_minutes,
            'task_status': 'completed'
        })
    
    return JsonResponse({'status': 'not_running', 'task_id': task.pk})


@login_required
def profile_view(request):
    """View and edit user profile."""
    from .forms import ProfileForm
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    
    if request.method == 'POST':
        # Handle password change
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                profile_form = ProfileForm(instance=request.user)
        # Handle profile update
        else:
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile')
            password_form = PasswordChangeForm(request.user)
    else:
        profile_form = ProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'tasks/profile.html', context)

