from django.urls import path

from . import views


app_name = 'games_for_admin_approval'

urlpatterns = [
    path('games-stats-for-approval/',
            views.GamesForApprovalView.as_view(),
                name='all'),
    path('games-stats-for-approval/<slug:game>/reports/',
            views.GameStatsReportsView.as_view(),
                name='reports'),
]