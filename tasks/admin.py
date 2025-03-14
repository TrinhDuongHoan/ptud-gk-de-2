from django.contrib import admin
from .models import Task  # Chỉ import Task, không import Profile nữa

admin.site.register(Task)