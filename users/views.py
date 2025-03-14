from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import requests
from django.core.files.base import ContentFile
import os

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản đã được tạo cho {username}! Bạn có thể đăng nhập.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        messages.success(request, 'Bạn đã đăng xuất thành công!')
        logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Thông tin của bạn đã được cập nhật!')
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)


@require_POST
def update_avatar(request):
    try:
        if 'avatar' in request.FILES:
            # Xử lý upload ảnh từ máy tính
            avatar_file = request.FILES['avatar']
            request.user.user_profile.avatar.save(
                f'avatar_{request.user.username}_{os.path.splitext(avatar_file.name)[1]}',
                avatar_file,
                save=True
            )
        elif 'avatar_url' in request.POST:
            # Xử lý avatar từ API
            avatar_url = request.POST.get('avatar_url')
            response = requests.get(avatar_url)
            if response.status_code == 200:
                request.user.user_profile.avatar.save(
                    f'avatar_{request.user.username}.png',
                    ContentFile(response.content),
                    save=True
                )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)