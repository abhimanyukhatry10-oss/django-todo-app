
from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed',"priority","due_date",]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task description',
                'rows': 4
            }),

            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            "priority": forms.Select(attrs={
                "class": "form-select"
            }),
            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']