from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/tasks/', views.tasks_api, name='tasks_api'),
    path('api/tasks/<int:pk>/', views.task_api, name='task_api'),
]
