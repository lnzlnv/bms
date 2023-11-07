import mimetypes

from django.db import models


def main_image_upload_path(instance, filename):
    folder_name = 'main'
    return '{}/{}'.format(folder_name, filename)


class MainImage(models.Model):
    image = models.ImageField(
        upload_to=main_image_upload_path
    )

    description = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    images = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.image.name
    

def highlights_video_upload_path(instance, filename):
    folder_name = 'highlights'
    return '{}/{}'.format(folder_name, filename)


class Highlights(models.Model):
    video = models.FileField(
        upload_to=highlights_video_upload_path
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    videos = models.Manager()


    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.video.name
    
    @property
    def video_type(self):
        mime_type, _ = mimetypes.guess_type(self.video.path)
        return mime_type
    

def news_image_upload_path(instance, filename):
    folder_name = 'news'
    return '{}/{}'.format(folder_name, filename)


class News(models.Model):
    image = models.ImageField(
        upload_to=news_image_upload_path
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    images = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.image.name