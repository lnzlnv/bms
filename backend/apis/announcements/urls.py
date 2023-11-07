from django.urls import path

from . import views

app_name = 'api_announcement'

urlpatterns = [
    path('announcements/',
            views.AnnouncementsAPIView.as_view(),
                name='api'),
    path('announcements/<int:pk>/',
            views.AnnouncementsAPIView.as_view(),
                name='api-2')
]