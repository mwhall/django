from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
            path('register/', views.register, name='register'),
            # Add other URLs as needed
            path('profile/', views.profile, name='profile'),  # Profile update URL
            path('update_user_info/', views.update_user_info, name='update_user_info'),
            path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
            path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
            path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
            path("login/", auth_views.LoginView.as_view(template_name="login.html"), name='login'),
            path("logout/", views.logout_to_login, name='logout'),
            #path('', views.home, name='home'),  # User homepage
            path('devices/', views.devices, name='devices'),
            path('new_user_device/', views.new_user_device, name='new_user_device'),
            #path('components/', views.components, name='components'),
            #path('teardowns/', views.teardowns, name='teardowns'),
            #path('hacks/', views.hacks, name='hacks'),
                ]

