from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }