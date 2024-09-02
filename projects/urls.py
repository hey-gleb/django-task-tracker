from django.urls import path

from projects.views import (
    ProjectList,
    ProjectDetail,
    AddMembersView, MonthlyStatsView,
)

urlpatterns = [
    path("projects/", ProjectList.as_view(), name="project-list"),
    path("projects/<uuid:pk>", ProjectDetail.as_view(), name="project-detail"),
    path("projects/<uuid:pk>/members/", AddMembersView.as_view(), name="add-project-members"),
    path("stats/monthly/", MonthlyStatsView.as_view(), name="project-monthly-stats")
]
