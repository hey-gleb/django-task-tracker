from django.urls import path

from projects.views import ProjectList, ProjectDetail, AddMembersView

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<uuid:pk>', ProjectDetail.as_view(), name='project-detail'),
    path('projects/<uuid:pk>/members/', AddMembersView.as_view(), name='add-members')
]