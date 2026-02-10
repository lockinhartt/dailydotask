from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required except estimated_duration
        required_fields = ['title', 'description', 'priority', 'status', 'due_date', 'due_time']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
        
        # Set estimated_duration as optional
        if 'estimated_duration' in self.fields:
            self.fields['estimated_duration'].required = False
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date', 'due_time', 'estimated_duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Task description', 'required': True}),
            'priority': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'due_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated duration in minutes', 'min': 1}),
        }


class ProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    
    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
        }

