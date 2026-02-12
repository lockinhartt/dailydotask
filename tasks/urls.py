from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_task_view, name='create_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('pending/', views.filtered_tasks, {'filter_type': 'pending'}, name='tasks_pending'),
    path('in-progress/', views.filtered_tasks, {'filter_type': 'in_progress'}, name='tasks_in_progress'),
    path('completed/', views.filtered_tasks, {'filter_type': 'completed'}, name='tasks_completed'),
    path('overdue/', views.filtered_tasks, {'filter_type': 'overdue'}, name='tasks_overdue'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('update-status/<int:pk>/', views.update_task_status, name='update_status'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('toggle/<int:pk>/', views.toggle_status, name='toggle_status'),
    path('start-timer/<int:pk>/', views.start_timer, name='start_timer'),
    path('stop-timer/<int:pk>/', views.stop_timer, name='stop_timer'),
    path('profile/', views.profile_view, name='profile'),
    # Archive functionality
    path('archive/', views.archive_list, name='archive_list'),
    path('restore/<int:pk>/', views.restore_task, name='restore_task'),
    path('delete-permanent/<int:pk>/', views.permanent_delete, name='permanent_delete'),
]
