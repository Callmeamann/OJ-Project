from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', include('homepage.urls')),
    path('home/', include('homepage.urls')),  # homepage app
    path('problems/', include('problems.urls')),
    path('submissions/', include('submissions.urls')),
    path('contests/', include('contests.urls')),
    path('community/', include('community.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)