from django.urls import path

from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('account/', views.acoount_view, name='account'),
    path('login/', views.LoginView.as_view(template_name='app_users/login.html'), name='login'),
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('logout/', views.user_logout, name='logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)