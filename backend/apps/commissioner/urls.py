from django.urls import path

from . import views

app_name = 'commissioner'

urlpatterns = [
    path('commissioner/',
            views.CommissionerPageView.as_view(),
                name='landing'),
    path('commissioner/edit/',
            views.CommissionerEditPageView.as_view(),
                name='edit'),
]