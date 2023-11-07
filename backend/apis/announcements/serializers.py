from rest_framework import serializers

from apis.game_schedule.services import (
    get_image_name,
    get_formatted_date,
    get_formatted_date_2
)
from apps.announcements.models import Announcement

from .services import get_date_based_on_method

class AnnouncementSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField(read_only=True)
    date_format_1 = serializers.SerializerMethodField(read_only=True)
    date_format_2 = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Announcement
        fields = [
            'id',
            'publish_date',
            'image',
            'image_name',
            'date_format_1',
            'date_format_2',
            'time'
        ]
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.is_update = kwargs['context'].pop('is_update', False)
    
    def get_image_name(self, instance):
        return get_image_name(image=instance.image.name)
    
    def get_date_format_1(self, instance):
        if self.is_update:
            return get_formatted_date_2(date=instance.publish_date)

        return get_formatted_date(date=instance.publish_date)
    
    def get_date_format_2(self, instance):
        date = get_date_based_on_method(
            date=instance.publish_date,
            is_update=self.is_update
        )
        return date.strftime("%B %d, %Y")
    
    def get_time(self, instance):
        date = get_date_based_on_method(
            date=instance.publish_date,
            is_update=self.is_update
        )
        return date.strftime("%I:%M %p")