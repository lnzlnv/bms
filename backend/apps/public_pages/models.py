from django.db import models

from apps.authentication.models import User

def season_image_upload_path(instance, filename):
    folder_name = 'seasons'
    new_filename = '{}/{}'.format(
        folder_name,
        filename
    )
    return '{}/{}'.format(folder_name, new_filename)

class Season(models.Model):
    year = models.IntegerField(
        unique=True
    )

    logo = models.ImageField(
        upload_to=season_image_upload_path
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    seasons = models.Manager()

    class Meta:
        ordering = ['-year']

    def __str__(self) -> str:
        return str(self.year)

def schedule_image_upload_path(instance, filename):
    folder_name = 'schedule_image'
    new_filename = '{}/{}'.format(
        instance.get_division_display().lower(), 
        filename
    )
    return '{}/{}'.format(folder_name, new_filename)


class ScheduleBanner(models.Model):
    DIVISIONS = [
        ('J', 'Junior'),
        ('S', 'Senior')
    ]
    
    season = models.ForeignKey(
        Season,
        related_name='schedule_banners',
        on_delete=models.CASCADE,
    )

    creator = models.ForeignKey(
        User,
        related_name='schedule_banners',
        on_delete=models.SET_NULL,
        null=True,
    )

    date = models.DateTimeField()

    image = models.ImageField(
        upload_to=schedule_image_upload_path
    )

    division = models.CharField(
        max_length=100,
        choices=DIVISIONS,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    schedules = models.Manager()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return '{} - {}'.format(
            self.get_division_display(),
            self.date
        )