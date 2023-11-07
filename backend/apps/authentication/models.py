from datetime import datetime
import pytz

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLES = [
        ('O', 'Officiating'),
        ('A', 'Administration'),
        ('S', 'Statistician'),
        ('SS', 'Lead Statistician'),
        ('SA', 'Super Administration')
    ]

    STATUS = [
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('P', 'Pending')
    ]

    email = models.EmailField(
        _('email'),
        null=True,
        blank=True,
        unique=True
    )

    address = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    contact_number = models.IntegerField(
        null=True,
        blank=True,
    )

    user_role = models.CharField(
        choices=ROLES,
        max_length=10
    )

    status = models.CharField(
        choices=STATUS,
        max_length=10,
        default='P'
    )

    expiration_date = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )

    is_updated = models.BooleanField(
        default=False
    )

    password_raw = models.CharField(
        default='',
        blank=True
    )

    has_activation_request = models.BooleanField(
        default=False
    )

    # users = models.Manager()

    @property
    def is_officiating(self):
        return self.user_role == 'O'

    @property
    def is_administration(self):
        return self.user_role == 'A'

    @property
    def is_statistician(self):
        return self.user_role == 'S'

    @property
    def is_super_administration(self):
        return self.user_role == 'SA'

    @property
    def is_approved(self):
        return self.status == 'A'

    @property
    def is_super_statistician(self):
        return self.user_role == 'SS'

    @property
    def has_admin_privileges(self):
        return self.is_administration or self.is_super_administration

    @property
    def has_statistician_privileges(self):
        return self.is_super_statistician or self.is_statistician

    @property
    def is_expired(self):
        if self.expiration_date is None:
            return False

        now = datetime.now()
        tz = pytz.timezone('Asia/Manila')
        naive_datetime = datetime(now.year, now.month, now.day)
        now = tz.localize(naive_datetime)

        return self.expiration_date < now