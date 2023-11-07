from django.urls import path

from . import views


app_name = 'api_user_profile'

urlpatterns = [
    path('update/user-<int:pk>/',
         views.UpdateProfileAPIView.as_view(),
         name='update')
]
