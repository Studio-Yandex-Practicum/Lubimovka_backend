from rest_framework import serializers

from apps.afisha.models import Event
from apps.articles.models import BlogItem, NewsItem
from apps.info.models import Place
from apps.library.models import Author, MasterClass, Performance, Play, Reading
from apps.library.serializers import (
    MasterClassEventSerializer,
    PerformanceEventSerializer,
    ReadingEventSerializer,
)
from apps.main.models import Banner


class MainBlogItemsForMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogItem
        fields = "__all__"


class NewsItemsForMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = "__all__"


class EventItemsForMainSerializer(serializers.ModelSerializer):
    event_body = serializers.SerializerMethodField()
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")

    def get_event_body(self, obj):
        event_body_serializers = {
            MasterClass: MasterClassEventSerializer,
            Performance: PerformanceEventSerializer,
            Reading: ReadingEventSerializer,
        }
        event_body = obj.common_event.target_model
        return event_body_serializers[type(event_body)](event_body).data

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


class AuthorForPlayForMainSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source="person.full_name")

    class Meta:
        model = Author
        fields = ("name", "id")


class PlayForMainSerializer(serializers.ModelSerializer):

    authors = AuthorForPlayForMainSerializer(many=True)

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
