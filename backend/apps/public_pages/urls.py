from django.urls import path
from . import views


app_name = 'public_pages'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('about-us/', views.AboutPageView.as_view(), name='about'),
    path('schedules/', views.SchedulePageView.as_view(), name='schedule'),
    path('recaps/', views.RecapsView.as_view(), name='recaps'),
    path('schedules/view/all/',
         views.SchedulesPublicView.as_view(),
         name='all-schedules')
]