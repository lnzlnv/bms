from django.urls import path

from . import views

app_name = 'api_game_schedule'

urlpatterns = [
    path('game-schedule/options/',
            views.GameScheduleAPIView.as_view(),
                name='options'),
    path('all-game-schedule/<int:season>/<str:division>/',
            views.AllScheduleAPIView.as_view(), 
                name='all'),
    path('game-schedule/delete/<int:pk>/',
            views.DeleteSingleSchedule.as_view(),
                name='delete'),
    path('season-options/',
            views.SeasonsAPIView.as_view(),
                name='season-options'),
    path('game-schedule/edit/<int:pk>/',
            views.EditScheduleAPIView.as_view(),
                name='edit'),
    path('game-schedule/banner/',
            views.ScheduleBannerAPIView.as_view(),
                name='banner'),
    path('game-schedule/banner/<int:season>/<str:division>/',
            views.ScheduleBannerAPIView.as_view(),
                name='banner-all'),
    path('game-schedule/banner/<int:pk>/',
            views.ScheduleBannerAPIView.as_view(),
                name='banner-single'),
    path('game-schedule/banner/options/',
            views.CreateScheduleBannerOptionsAPIView.as_view(),
                name='banner-options'),
]