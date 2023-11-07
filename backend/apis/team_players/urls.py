from django.urls import path, include

from . import views

app_name = 'api_team_players'

urlpatterns = [
    path('team/players/', include([
        path('options/<int:pk>/',
             views.TeamPlayersOptions.as_view(),
             name='options'),
    ])),
    path('<int:season>/<int:pk>/players/',
         views.TeamPlayerAPIVIew.as_view(),
         name='endpoint-1'),
    path('season-<int:season>/<int:pk>/players/',
         views.TeamPlayerAPIVIew.as_view(),
         name='endpoint-2'),
    path('<int:team>/player-<int:pk>/',
         views.TeamPlayerAPIVIew.as_view(),
         name='endpoint-4'),
    path('team/players/import/season-<int:season>/team-<int:team>/',
         views.ImportPlayersAPIView.as_view(),
         name='import-players')
]
