from django.urls import path

from . import views


app_name = 'api_games_for_approval'

urlpatterns = [
    path('options/',
            views.GamesForAdminApprovalOptionsAPIView.as_view(),
                name='options'),
    path('',
            views.GamesForAdminApprovalAPIView.as_view(),
                name='approval-1'),
    path('<int:pk>/',
        views.GamesForAdminApprovalAPIView.as_view(),
            name='approval-2'),
]