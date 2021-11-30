from rest_framework import serializers

from apps.afisha.models import Event
from apps.articles.models import NewsItem
from apps.articles.serializers import BlogItemBaseSerializer
from apps.content_pages.serializers import BaseContentPageSerializer
from apps.info.models import Place
from apps.library.models import MasterClass, Performance, Play, Reading
from apps.library.serializers import (
    AuthorForPlaySerializer,
    EventMasterClassSerializer,
    EventPerformanceSerializer,
    EventReadingSerializer,
)
from apps.main.models import Banner


class EventItemsForMainSerializer(serializers.ModelSerializer):
    event_body = serializers.SerializerMethodField()
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")

    def get_event_body(self, obj):
        event_body_serializers = {
            MasterClass: EventMasterClassSerializer,
            Performance: EventPerformanceSerializer,
            Reading: EventReadingSerializer,
        }
        event_body = obj.common_event.target_model
        event_type = type(event_body)
        serializer = event_body_serializers[event_type]
        return serializer(event_body).data

    class Meta:
        model = Event
        fields = [
            "id",
            "type",
            "event_body",
            "date_time",
            "paid",
            "url",
            "place",
        ]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        exclude = (
            "created",
            "modified",
        )


class PlayForMainSerializer(serializers.ModelSerializer):

    authors = AuthorForPlaySerializer(many=True)

    class Meta:
        fields = (
            "id",
            "name",
            "authors",
            "city",
            "year",
            "url_download",
            "url_reading",
        )
        model = Play


class PlaceForMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = ("created", "modified")


class BlogItemListForMainSerializer(BlogItemBaseSerializer):
    pass


class NewsItemForMainSerializer(
    BaseContentPageSerializer, serializers.ModelSerializer
):
    class Meta:
        model = NewsItem
        fields = (
            "id",
            "title",
            "description",
            "image",
            "pub_date",
        )


class MainSerializer(serializers.Serializer):
    first_screen_title = serializers.CharField(required=False)
    first_screen_url_title = serializers.CharField(required=False)
    first_screen_url = serializers.URLField(required=False)
    blog_title = serializers.CharField(required=False)
    blog_items = BlogItemListForMainSerializer(many=True, required=False)
    news_title = serializers.CharField(required=False)
    news_items = NewsItemForMainSerializer(many=True, required=False)
    event_title = serializers.CharField(required=False)
    event_items = EventItemsForMainSerializer(many=True, required=False)
    banner_items = BannerSerializer(many=True, required=False)
    short_list_title = serializers.CharField(required=False)
    short_list_items = PlayForMainSerializer(many=True, required=False)
    place_items = PlaceForMainSerializer(many=True, required=False)
    video_archive_url = serializers.URLField(required=False)
    video_archive_photo = serializers.ImageField(required=False)
