from django.urls import path

from . import views

app_name = 'apis_generate_account'

urlpatterns = [
    path('', views.GenerateAccountAPIView.as_view(), name='generate'),
    path('options/',
         views.GenerateAccountOptions.as_view(),
         name='options'
         ),
    path('delete/user-<int:pk>/',
         views.GenerateAccountAPIView.as_view(),
         name='delete'),
    path('send-email/user-<int:pk>/',
         views.SendCredentialsViaEmailAPIView.as_view(),
         name='send-email'),
    path('activation-requests/',
         views.AccountActivationRequestAPIView.as_view(),
         name='activation-request'),
    path('activation-requests/<int:pk>/',
         views.AccountActivationRequestAPIView.as_view(),
         name='activation-request-2')
]
