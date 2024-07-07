from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', include('homepage.urls')),
    path('home/', include('homepage.urls')),  # homepage app
    path('problems/', include('problems.urls')),
    path('submissions/', include('submissions.urls')),
    # path('contests/', include('contests.urls')),
    # path('community/', include('community.urls')),
]
