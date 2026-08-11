
from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
#Django ka built-in registration form import kar rahe hain.
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    #ModelForm model ki information se form ki validation automatically build karta hai.
    #Model defines the rule; ModelForm brings that rule into the form.
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
"""
Q. ModelForm ka advantage

Normal form me hume manually fields define karni pad sakti hain:

title = forms.CharField(...)
description = forms.CharField(...)

Lekin ModelForm me:

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [...]

Django model ko dekhkar form fields aur unki basic validation automatically generate kar deta hai.
"""

#/////////////////////////////////////////
"""
Q. UserCreationForm inherit kyun kiya?
class RegisterForm(UserCreationForm):

Kyuki Django ne pehle se user registration ka bahut saara logic bana rakha hai.

Jaise:

password1/password2
passwords match karna
password validation
password ko securely hash karke save karna
user creation

Hume ye sab manually implement nahi karna pada.
"""