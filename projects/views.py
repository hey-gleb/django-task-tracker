from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView


from projects.models import Project
from projects.permissions import IsManager
from projects.serializers import ProjectSerializer, AddMembersSerializer, CustomRegisterSerializer


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsManager, IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save(user=self.request.user)
        project.members.add(self.request.user)


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
