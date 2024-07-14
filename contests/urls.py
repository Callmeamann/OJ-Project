from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path('contests/host/', views.host_contest, name='host_contest'),
    path('', views.contests_list, name='contests_list'),
]
