from django.urls import path

from projects.views import ProjectList, ProjectDetail

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<int:pk>', ProjectDetail.as_view(), name='project-detail')
]