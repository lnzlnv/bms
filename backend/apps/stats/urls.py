from django.urls import path

from . import views


app_name = 'stats'

urlpatterns = [
    path('stats/players/',
         views.PlayerStatsPageView.as_view(),
         name='player'),
    path('stats/teams/',
         views.TeamStatsPageView.as_view(),
         name='team'),
    path('stats/<str:player>/',
         views.SinglePlayerStats.as_view(),
         name='single-player'),
]
