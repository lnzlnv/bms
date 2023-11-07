from django.urls import path

from . import views


app_name = 'api_standings'

urlpatterns = [  # api/public/standings/
    path('all/<int:season>/',
         views.TeamStandingsAPIView.as_view(),
         name='all'),
    path('all/players/<int:season>/<str:division>/',
         views.PlayerStandingsAPIView.as_view(),
         name='players'),
    path('single-player/<int:pk>/',
         views.SinglePlayerStats.as_view(),
         name='single-player')
]
