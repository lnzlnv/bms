from apps.authentication.models import User


def get_unupdated_accounts():
    return User.objects.filter(
        is_updated=False
    )


def get_activation_requests():
    return User.objects.filter(
            has_activation_request=True
        )