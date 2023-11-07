from django.urls import path

from . import views


app_name = 'api_recaps'

urlpatterns = [
    path('', views.RecapsAPIView.as_view(), name='all')
]