from rest_framework import serializers

from apps.afisha.serializers import EventSerializer
from apps.articles.serializers import (
    BlogItemListSerializer,
    NewsItemSerializer,
)
from apps.info.serializers.place import PlaceSerializer
from apps.library.serializers import PlaySerializer
from apps.main.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        exclude = (
            "created",
            "modified",
        )


class MainSerializer(serializers.Serializer):
    first_screen_title = serializers.CharField(required=False)
    first_screen_url_title = serializers.CharField(required=False)
    first_screen_url = serializers.URLField(required=False)
    blog_title = serializers.CharField(required=False)
    blog_items = BlogItemListSerializer(many=True, required=False)
    news_title = serializers.CharField(required=False)
    news_items = NewsItemSerializer(many=True, required=False)
    event_title = serializers.CharField(required=False)
    event_items = EventSerializer(many=True, required=False)
    banner_items = BannerSerializer(many=True, required=False)
    short_list_title = serializers.CharField(required=False)
    short_list_items = PlaySerializer(many=True, required=False)
    place_items = PlaceSerializer(many=True, required=False)
    video_archive_url = serializers.URLField(required=False)
    video_archive_photo = serializers.ImageField(required=False)
