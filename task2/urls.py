from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TaskListAPIView.as_view(), name='all'),
    path('<int:task_id>/', views.TaskGetUpdateView.as_view(), name='get_update'),
]
