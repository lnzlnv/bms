from django.urls import path

from . import views


app_name = 'api_public_schedules'

urlpatterns = [
    path('all/', views.PublicSchedulesAPIView.as_view(), name='all')
]
