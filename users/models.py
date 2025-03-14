from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import requests
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    avatar = models.ImageField(upload_to='avatars/', default='default.jpg')
    role = models.CharField(
        max_length=10,
        choices=[('ADMIN', 'Admin'), ('USER', 'User')],
        default='USER'
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_overdue_tasks_count(self):
        from tasks.models import Task
        return Task.objects.filter(
            user=self.user,
            status__in=['pending', 'in_progress'],
            created__lt=timezone.now()
        ).count()

    def save(self, *args, **kwargs):
        # Lưu profile trước
        super().save(*args, **kwargs)

        # Tạo thư mục media/avatars nếu chưa tồn tại
        if not os.path.exists('media/avatars'):
            os.makedirs('media/avatars')

        # Nếu không có avatar hoặc sử dụng avatar mặc định
        if not self.avatar or self.avatar.name == 'default.jpg':
            try:
                response = requests.get('https://avatar-placeholder.iran.liara.run/')
                if response.status_code == 200:
                    avatar_name = f'avatar_{self.user.username}.jpg'
                    avatar_path = f'media/avatars/{avatar_name}'
                    
                    # Lưu avatar từ API
                    avatar_response = requests.get(response.url)
                    with open(avatar_path, 'wb') as f:
                        f.write(avatar_response.content)
                    
                    # Cập nhật đường dẫn avatar
                    self.avatar = f'avatars/{avatar_name}'
                    super().save(update_fields=['avatar'])

                    # Resize ảnh sau khi đã lưu thành công
                    if os.path.exists(avatar_path):
                        img = Image.open(avatar_path)
                        if img.height > 300 or img.width > 300:
                            output_size = (300, 300)
                            img.thumbnail(output_size)
                            img.save(avatar_path)
            except Exception as e:
                print(f"Error creating avatar: {e}")
                # Nếu có lỗi, giữ nguyên avatar mặc định
                pass
        else:
            # Nếu có avatar được upload, resize nó
            try:
                img_path = self.avatar.path
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        img.save(img_path)
            except Exception as e:
                print(f"Error resizing avatar: {e}")
                pass