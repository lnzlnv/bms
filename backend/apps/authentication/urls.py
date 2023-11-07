from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'authentication'

urlpatterns = [
    path('sign-in/', views.LoginPageView.as_view(), name='sign-in'),
    path('redirect-based-on-role/',
         views.RedirectBasedOnUserRoleView.as_view(),
         name="redirect-based-on-role"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/activation-request/<str:username>/',
         views.AccountActivationRequest.as_view(),
         name='activation-request')
]
