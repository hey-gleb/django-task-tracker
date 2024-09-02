from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from projects.pagination import QueryPageNumberPagination
from tasks.serializers import TaskSerializer, TimeLogSerializer
from tasks.models import Task, TimeLog

# TODO add pagination
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = QueryPageNumberPagination

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        user = self.request.user

        if not project.members.filter(id=user.id).exists():
            raise PermissionDenied("You do not have permission to create tasks in this project.")

        serializer.save(created_by=user)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TimeLogList(generics.ListCreateAPIView):
    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer

    def perform_create(self, serializer):
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(id=task_id)

        # Check if the user is a member of the project
        user = self.request.user
        if not task.project.members.filter(id=user.id).exists():
            raise PermissionDenied("You do not have permission to log time on this task.")

        # Save the time log with the task and user information
        serializer.save(task=task, user=user)

    def get_queryset(self):
        return TimeLog.objects.filter(task=self.kwargs['pk'])
