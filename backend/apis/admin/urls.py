from django.urls import path

from . import views


app_name = 'api-administration'

urlpatterns = [
    path('user-request/',
            views.UserRequestAPIView.as_view(),
                name='user-request'),
    path('user-request/<int:pk>/',
            views.UserRequestAPIView.as_view(),
                name='update-status'),
    path('seasons/',
            views.SeasonAPIView.as_view(),
                name='season-1'),
    path('seasons/<int:pk>/',
            views.SeasonAPIView.as_view(),
                name='season-2'),
]