from django.urls import path

from . import views


app_name = 'apis_landing'


urlpatterns = [ # api/landing/
     path('main-image/',
          views.MainImageAPIVIew.as_view(),
          name='main-1'),
     path('main-image/<int:pk>/',
          views.MainImageAPIVIew.as_view(),
          name='main-2'),
     path('highlights/',
          views.HighlightsAPIView.as_view(),
          name='highlights-1'),
     path('highlights/<int:pk>/',
          views.HighlightsAPIView.as_view(),
          name='highlights-2'),
     path('highlights/public/',
          views.PublicHighlightsAPIView.as_view(),
          name='highlights-3'),
     path('news/',
          views.NewsAPIView.as_view(),
          name='news-1'),
     path('news/<int:pk>/',
          views.NewsAPIView.as_view(),
          name='news-2')
]