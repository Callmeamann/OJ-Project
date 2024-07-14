
from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('community/<int:pk>/', views.community_detail, name='community_detail'),
    path('community/<int:pk>/follow/', views.follow_community, name='follow_community'),
    path('community/<int:pk>/unfollow/', views.unfollow_community, name='unfollow_community'),

    path('community/<int:pk>/create_post/', views.create_post, name='create_post'),
    path('post/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('community/create/', views.create_community, name='create_community'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),

    # other paths...
]
