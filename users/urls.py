from django.contrib import admin
from . import views, admin_views
from django.urls import path, include

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/user-search/', admin_views.user_search_api, name='user_search_api'),
    path('update-user-role/', admin_views.update_user_role, name='update_user_role'),
    path('update-user-role-view/', admin_views.update_user_role_view, name='update_user_role_view'),
]
