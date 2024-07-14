# community/admin.py
from django.contrib import admin
from .models import Community, Post, Comment

# Registering Community model
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'created_by')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'created_by')

# Registering Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'community', 'created_at', 'created_by')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'community', 'created_by')

# Registering Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'created_at', 'created_by')
    search_fields = ('content',)
    list_filter = ('created_at', 'post', 'created_by')


