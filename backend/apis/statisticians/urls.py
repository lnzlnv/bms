from django.urls import path

from . import views


app_name = 'api_statisticians'

urlpatterns = [
    path('games/',
            views.GamesAPIView.as_view(),
                name='games'),
    path('all-games/options/',
            views.GamesTodayOptionsAPIView.as_view(),
                name='games-totay-options'),
    path('statistician/officiate-<int:pk>/',
            views.OfficiateGameAPIView.as_view(),
                name='officiate-game'),
    path('statistician/player-<int:pk>/stats/',
            views.OfficiateGameAPIView.as_view(),
                name='stats'),
    path('statistician/<int:game>/<int:team>/stats-<int:pk>/',
            views.OfficiateGameAPIView.as_view(),
                name='update-stats'),
    path('statistician/substitution/<int:game>/<int:team>/',
            views.OfficiateGameAPIView.as_view(),
                name='substitution'),
    path('statistician/quarter/<int:game>/',
            views.GameQuarterAPIView.as_view(),
                name='quarter'),
    path('statistician/generate-analysis/<int:quarter>/<int:game>/',
            views.GenerateTimeAnalysis.as_view(),
                name='generate-analysis')
]