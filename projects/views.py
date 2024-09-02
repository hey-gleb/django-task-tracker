from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Project
from projects.pagination import QueryPageNumberPagination
from projects.permissions import IsManager
from projects.serializers import ProjectSerializer, AddMembersSerializer, CustomRegisterSerializer
from tasks.models import TimeLog


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsManager, IsAuthenticated]
    pagination_class = QueryPageNumberPagination

    def perform_create(self, serializer):
        project = serializer.save(user=self.request.user)
        project.members.add(self.request.user)


    # TODO verify different managers see different projects
    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class AddMembersView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = AddMembersSerializer
    permission_classes = [IsAuthenticated]  # Add permissions as needed

    def get_object(self):
        project_id = self.kwargs['pk']
        return Project.objects.get(pk=project_id)

# TODO move to a separate app
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class ProjectTimeStatsView(APIView):
    # TODO add manager verification
    # TODO add endpoint to get data by users
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        now = timezone.now()
        start_data = now - timedelta(days=30)

        try:
            project = Project.objects.get(id=kwargs.get('pk'))
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=404)

        # if not project.user != self.request.user:
        #     return Response({"detail": "You do not have permission to view this project."}, status=403)

        total_time = TimeLog.objects.filter(
            task__project=project,
            created_at__gte=start_data
        ).aggregate(total_hours_spent=Sum('hours_spent'))

        return Response({
            "project": project.title,
            "total_hours_spent": total_time['total_hours_spent'] or 0
        })
