from django.urls import path

from . import views


app_name = 'user_profile'

urlpatterns = [
    path('update/<str:username>/',
         views.UpdateUserProfileView.as_view(),
         name='update')
]
