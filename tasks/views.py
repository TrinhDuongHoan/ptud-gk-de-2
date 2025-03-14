from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from users.models import Profile  # Import Profile từ users app

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created')
    overdue_count = request.user.user_profile.get_overdue_tasks_count()
    
    context = {
        'tasks': tasks,
        'overdue_count': overdue_count,
    }
    return render(request, 'tasks/task_list.html', context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overdue_count'] = self.request.user.user_profile.get_overdue_tasks_count()  # Thay đổi .profile thành .user_profile
        return context

class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user or self.request.user.is_staff

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        if form.instance.status == 'completed' and not form.instance.finished:
            form.instance.finished = timezone.now()
        return super().form_valid(form)
    
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user or self.request.user.is_staff

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user or self.request.user.is_staff

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create profile for user
            Profile.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)  # Thay đổi .profile thành .user_profile
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.user_profile)  # Thay đổi .profile thành .user_profile
    
    context = {
        'profile_form': profile_form,
        'overdue_count': request.user.user_profile.get_overdue_tasks_count(),  # Thay đổi .profile thành .user_profile
    }
    return render(request, 'accounts/profile.html', context)