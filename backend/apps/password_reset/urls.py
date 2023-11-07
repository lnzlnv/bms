from django.urls import path

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .forms import PasswordResetForm


urlpatterns = [
    path('password-reset/',
         PasswordResetView.as_view(
             template_name='password-reset/forgot-password.html',
             form_class=PasswordResetForm
         ),
         name='password-reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='password-reset/done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password-reset/confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password-reset/complete.html'),
         name='password_reset_complete'),
]
