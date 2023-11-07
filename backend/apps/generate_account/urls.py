from django.urls import path

from . import views


app_name = 'generate_account'

urlpatterns = [
    path('', views.GenerateAccount.as_view(), name='generate'),
    path('not-updated-accounts/',
         views.UnupdatedAccountsView.as_view(),
         name='unupdated'),
]