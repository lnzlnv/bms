from rest_framework import serializers

from apps.landing.models import (
    MainImage,
    Highlights,
    News
)
from apis.game_schedule.services import get_image_name


class MainImageSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField(read_only=True)
    desc_1 = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = MainImage
        fields = [
            'id',
            'image',
            'description',
            'desc_1',
            'image_name'
        ]

    def get_image_name(self, instance):
        return get_image_name(image=instance.image.name)
    
    def get_desc_1(self, instance):
        return '{}...'.format(instance.description[0:28])


class HighlightSerializer(serializers.ModelSerializer):
    video_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Highlights
        fields = [
            'id',
            'video',
            'video_name',
            'video_type'
        ]

    def get_video_name(self, instance):
        return get_image_name(image=instance.video.name)
    

class NewsSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = [
            'id',
            'image',
            'image_name'
        ]
    
    def get_image_name(self, instance):
        return get_image_name(image=instance.image.name)