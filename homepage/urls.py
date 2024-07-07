from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Assuming you have a home view
]
