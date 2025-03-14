from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    CATEGORY_CHOICES = [  # Đổi tên biến thành CATEGORY_CHOICES để rõ ràng hơn
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('study', 'Study'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    finished = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')  # Thêm trường category
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title