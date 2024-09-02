from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Project
from projects.pagination import QueryPageNumberPagination
from users.permissions import IsManager
from projects.serializers import (
    ProjectSerializer,
    AddMembersSerializer,
    MonthlyStatsSerializer,
)
from tasks.models import TimeLog
from django.utils.timezone import now


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
        project_id = self.kwargs["pk"]
        return Project.objects.get(pk=project_id)



class MonthlyStatsView(APIView):
    def get(self, request, *args, **kwargs):
        # start_date = now().replace(day=1)
        start_date = now() - timedelta(days=30)
        end_date = now()
        # end_date = (start_date + timedelta(days=31)).replace(day=1)

        projects = Project.objects.filter(user=self.request.user)
        aggregated_data = []

        for project in projects:
            project_data = {
                "project_id": project.id,
                "project_title": project.title,
                "total_hours": TimeLog.objects.filter(
                    task__project=project, created_at__range=[start_date, end_date]
                ).aggregate(total_hours=Sum("hours_spent"))["total_hours"]
                or 0,
                "user_stats": [],
            }

            users = User.objects.filter(task__project=project).distinct()
            for user in users:
                user_data = TimeLog.objects.filter(
                    task__project=project,
                    user=user,
                    created_at__range=[start_date, end_date],
                ).aggregate(total_hours=Sum("hours_spent"))

                project_data["user_stats"].append(
                    {
                        "user_id": user.id,
                        "email": user.email,
                        "total_hours": user_data["total_hours"] or 0,
                    }
                )

            aggregated_data.append(project_data)

        serializer = MonthlyStatsSerializer(aggregated_data, many=True)
        return Response(serializer.data)
