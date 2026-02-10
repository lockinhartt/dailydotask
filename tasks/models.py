from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Model representing a todo task with AI-powered features."""
    
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    estimated_duration = models.IntegerField(null=True, blank=True, help_text="Estimated duration in minutes")
    time_limit = models.IntegerField(null=True, blank=True, help_text="Time limit in minutes - task auto-completes when timer reaches this")
    time_spent = models.IntegerField(default=0, help_text="Actual time spent in minutes")
    timer_started_at = models.DateTimeField(null=True, blank=True, help_text="When the current timer started")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AI-related fields
    ai_suggested_priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, null=True, blank=True)
    ai_category = models.CharField(max_length=100, blank=True)
    
    # AI difficulty estimation
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    ai_difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    ai_difficulty_score = models.FloatField(null=True, blank=True)
    ai_difficulty_reasons = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
