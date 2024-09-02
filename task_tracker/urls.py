from django.contrib import admin
from django.urls import path, include

from projects.views import CustomRegisterView

PUBLIC_API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(PUBLIC_API_PREFIX, include('projects.urls')),
    path(PUBLIC_API_PREFIX, include('tasks.urls')),

    path(PUBLIC_API_PREFIX + 'auth/', include('dj_rest_auth.urls')),
    # path(PUBLIC_API_PREFIX + 'auth/registration/', include('dj_rest_auth.registration.urls')),
    path(PUBLIC_API_PREFIX + 'auth/registration/', CustomRegisterView.as_view()),
    path('accounts/', include('allauth.urls')),
#     TODO add swagger documentation
]
