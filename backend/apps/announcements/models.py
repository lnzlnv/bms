from django.db import models

from apis.game_schedule.services import get_formatted_date


def announcement_image_upload_path(instance, filename):
    folder_name = 'announcements'
    new_filename = '{}/{}'.format(
        folder_name,
        filename
    )
    return '{}/{}'.format(folder_name, new_filename)

class Announcement(models.Model):
    publish_date = models.DateTimeField()

    image = models.ImageField(
        upload_to=announcement_image_upload_path
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    announcements = models.Manager()

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        date = get_formatted_date(date=self.publish_date)
        return 'Publish in {}'.format(
            date.strftime("%B %d, %Y")
        )