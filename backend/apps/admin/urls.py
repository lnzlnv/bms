from django.urls import path

from . import views

app_name = 'administration'

urlpatterns = [
    path('access-not-granted/',
            views.AccessNotGrantedView.as_view(),
                name='access-not-granted'),
    path('seasons/create/',
            views.CreateSeasonView.as_view(),
                name='create-season'),
    path('seasons/',
            views.AllSeasonView.as_view(),
                name='all-season')
]