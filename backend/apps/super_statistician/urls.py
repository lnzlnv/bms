from django.urls import path

from . import views


app_name = 'super_statistician'

urlpatterns = [
    path('game-stats-approval/',
            views.GameStatsApprovalView.as_view(),
                name='stats-approval'),
    path('game-stats-reports/<slug:game_slug>/',
            views.GameStatsReports.as_view(),
                name='stats-reports')
]