from django.urls import path
from . import views


urlpatterns = [
    path('run/<int:pk>/', views.run_code, name='run_code'),
    path('submit/<int:pk>/', views.submit_code, name='submit_code'),
    # Add other URL patterns for the submissions app here
]
