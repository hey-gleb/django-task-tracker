from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import CustomRegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="Django task tracker",
        default_version="v1",
        description="Django application to track spent time on tasks completion",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

PUBLIC_API_PREFIX = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(PUBLIC_API_PREFIX, include("projects.urls")),
    path(PUBLIC_API_PREFIX, include("tasks.urls")),
    path(PUBLIC_API_PREFIX + "auth/", include("dj_rest_auth.urls")),
    path(PUBLIC_API_PREFIX + "auth/registration/", CustomRegisterView.as_view()),
    # path('accounts/', include('allauth.urls')),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# TODO fix CSRF Failed: CSRF token from POST incorrect.
