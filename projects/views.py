from rest_framework import generics

from projects.models import Project
from projects.serializers import ProjectSerializer


# TODO rework with ViewSet
class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer