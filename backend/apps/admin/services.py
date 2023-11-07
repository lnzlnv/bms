from django.http import HttpResponseRedirect
from django.urls import reverse


def redirect_user_without_permission(
    is_allowed: bool,
    default,  # function
):
    if is_allowed:
        return default

    return HttpResponseRedirect(
        reverse('administration:access-not-granted')
    )
