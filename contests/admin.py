from django.contrib import admin
from users.models import Profile, Role
from .models import Contest

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role__name')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role)

class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'host')
    list_filter = ('start_time', 'end_time')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_time'

admin.site.register(Contest, ContestAdmin)