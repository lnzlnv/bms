from django.urls import path

from . import views


app_name = 'api_super_statistician'


urlpatterns = [
    path('games-approval-options/',
            views.GameStatsApprovalOptions.as_view(),
                name='approval-options'),
    path('games-stats-approval/division/',
            views.GamesStatsForApprovalAPIView.as_view(),
                name='stats-approval'),
    path('games-stats-approval/<int:pk>/',
            views.GamesStatsForApprovalAPIView.as_view(),
                name='stats-approval-2'),
    path('games-stats-approval/team-stat-<int:team_stat>/<int:pk>/',
            views.GamesStatsForApprovalAPIView.as_view(),
                name='stats-approval-2'),
    path('games-stats-approval/<str:type>/<int:pk>/',
            views.GamesStatsForApprovalAPIView.as_view(),
                name='stats-approval-2'),
    path('games-stats-approval/approve/<int:pk>/',
            views.GamesStatsForApprovalAPIView.as_view(),
                name='stats-approval-3'),
    path('generate-full-time-analysis/<int:game>/',
            views.GenerateFullTimeAnalysisAPIView.as_view(),
                name='full-time-analysis')
]