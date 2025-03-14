# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Task, Profile

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'status', 'due_date']
#         widgets = {
#             'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['avatar']

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }