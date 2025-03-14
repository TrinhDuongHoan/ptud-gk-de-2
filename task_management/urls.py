from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from users.views import logout_view
from users.views import update_avatar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Cập nhật đường dẫn logout để chuyển hướng trực tiếp đến trang login
    path('logout/', logout_view, name='logout'),
    path('update-avatar/', update_avatar, name='update_avatar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)