from django.urls import path

from tasks.views import TaskList, TaskDetail

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list-create'),
    path('tasks/<uuid:pk>', TaskDetail.as_view(), name='task-detail'),
]
