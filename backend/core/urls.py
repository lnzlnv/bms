"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include([
        path('', include('apis.admin.urls')),
        path('', include('apis.auth.urls')),
        path('', include('apis.game_schedule.urls')),
        path('', include('apis.teams.urls')),
        path('', include('apis.team_players.urls')),
        path('', include('apis.announcements.urls')),
        path('', include('apis.statisticians.urls')),
        path('', include('apis.super_statistician.urls')),
        path('games-for-admin-approval/',
             include('apis.games_for_admin_approval.urls')),
        path('public/players/', include('apis.public_players.urls')),
        path('public/schedules/', include('apis.public_schedules.urls')),
        path('public/standings/', include('apis.standings.urls')),
        path('recaps/', include('apis.recaps.urls')),
        path('account/generate/', include('apis.generate_account.urls')),
        path('user/profile/', include('apis.user_profile.urls')),
        path('landing/', include('apis.landing.urls'))
    ])),
    path('', include('apps.public_pages.urls')),
    path('', include('apps.authentication.urls')),
    path('', include('apps.commissioner.urls')),
    path('', include('apps.players.urls')),
    path('', include('apps.standings.urls')),
    path('', include('apps.stats.urls')),
    path('', include('apps.teams.urls')),
    path('', include('apps.admin.urls')),
    path('', include('apps.game_schedule.urls')),
    path('', include('apps.team_players.urls')),
    path('', include('apps.announcements.urls')),
    path('', include('apps.statisticians.urls')),
    path('', include('apps.super_statistician.urls')),
    path('administration/', include('apps.games_for_admin_approval.urls')),
    path('administration/generate-account/',
         include('apps.generate_account.urls')),
    path('administration/landing/', include('apps.landing.urls')),
    path('user/profile/', include('apps.user_profile.urls')),
    path('', include('apps.password_reset.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
