"""
URL configuration for stats_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from football_app.views.player_stat_view import PlayerStatsListCreateView, PlayerStatsDetailView
from football_app.views.team_view import TeamListCreateView, TeamDetailView
from football_app.views.team_stat_view import TeamStatsListCreateView, TeamStatsDetailView
from football_app.views.user_view import UserListCreateView, UserDetailView
from football_app.views.registration_and_login import LoginView, RegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="Football Stats",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('player-stats/', PlayerStatsListCreateView.as_view(), name='player-stats-list-create'),
    path('player-stats/<uuid:pk>/', PlayerStatsDetailView.as_view(), name='player-stats-detail'),
    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<uuid:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('team-stats/', TeamStatsListCreateView.as_view(), name='team-stats-list-create'),
    path('team-stats/<uuid:pk>/', TeamStatsDetailView.as_view(), name='team-stats-detail'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-home'),
]
