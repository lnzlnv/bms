from django.urls import path

from . import views


app_name = 'game_schedule'

urlpatterns = [
    path('schedules/create/', 
            views.CreateScheduleView.as_view(),
                name='create'),
    path('schedules/all/',
            views.AllScheduleView.as_view(),
                name='all'),
    path('schedules/banner/create/',
            views.CreateScheduleBannerView.as_view(),
                name='banner'),
    path('schedules/banner/all/',
            views.AllScheduleBannerView.as_view(),
                name='banner-all'),
]