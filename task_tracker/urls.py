from django.contrib import admin
from django.urls import path, include

PUBLIC_API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(PUBLIC_API_PREFIX, include('projects.urls')),
    path(PUBLIC_API_PREFIX, include('tasks.urls')),

    path(PUBLIC_API_PREFIX + 'auth/', include('dj_rest_auth.urls')),
    path(PUBLIC_API_PREFIX + 'auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
#     TODO add swagger documentation
]
