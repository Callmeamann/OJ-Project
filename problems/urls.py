from django.urls import path
from . import views


urlpatterns = [
    path('problems/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('problems/<int:pk>/run/', views.run_code_transfer, name='run_code_transfer'),
    path('problems/<int:pk>/submit/', views.submit_code_transfer, name='submit_code_tansfer'),
    path('problems/', views.problems_list, name='problems_list'),
    path('problems/add/', views.add_problem_view, name='add_problem'),
    path('review_problems/', views.review_problems, name='review_problems'),
    path('approve_problem/<int:pk>/', views.approve_problem_view, name='approve_problem'),
    path('discard-problem/<int:pk>/', views.discard_problem_view, name='discard_problem'),
]