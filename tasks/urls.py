from django.urls import path

from tasks.views import TaskList, TaskDetail, TimeLogList

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list-create'),
    path('tasks/<uuid:pk>', TaskDetail.as_view(), name='task-detail'),
    path('tasks/<uuid:pk>/time', TimeLogList.as_view(), name='time-log-list'),
]
