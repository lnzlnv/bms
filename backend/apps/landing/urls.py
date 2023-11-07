from django.urls import path

from . import views


app_name = 'landing'


urlpatterns = [ # administration/landing/
     path('content/',
          views.LandingContentDetailsView.as_view(),
          name='content'),
     path('main/add-image/',
          views.AddImageView.as_view(),
          name='add-image'),
     path('highlights/add-video/',
          views.HighlightsView.as_view(),
          name='add-highlights'),
     path('news/add-image/',
          views.AddNewsView.as_view(),
          name='add-news')
]