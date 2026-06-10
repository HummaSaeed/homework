"""URLs for homework management app."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('homeworks/', views.HomeworkListView.as_view(), name='homework_list'),
    path('homeworks/<int:pk>/', views.HomeworkDetailView.as_view(), name='homework_detail'),
    path('homeworks/create/', views.HomeworkCreateView.as_view(), name='homework_create'),
    path('homeworks/<int:homework_id>/submit/', views.SubmissionCreateView.as_view(), name='submission_create'),
]
