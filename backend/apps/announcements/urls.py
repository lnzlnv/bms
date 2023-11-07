from django.urls import path

from . import views


app_name = 'announcements'

urlpatterns = [
    path('announcements/create/',
            views.AnnouncementsCreateView.as_view(),
                name='create'),
    path('announcements/',
            views.AllAnnouncementsView.as_view(),
                name='all')
]