from rest_framework import serializers

from apps.afisha.models import Event
from apps.content_pages.models import EventsBlock, ImagesBlock, PersonsBlock, PlaysBlock, VideosBlock
from apps.content_pages.serializers import (
    ExtendedPersonSerializer,
    OrderedImageSerializer,
    OrderedPlaySerializer,
    OrderedVideoSerializer,
)
from apps.library.serializers.performance import EventPerformanceSerializer


class EventInBlockSerializer(serializers.ModelSerializer):
    """Returns Performance in EventsBlock."""

    event_body = EventPerformanceSerializer(
        source="common_event.target_model",
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "type",
            "event_body",
            "date_time",
            "paid",
            "url",
        )


class EventsBlockSerializer(serializers.ModelSerializer):
    items = EventInBlockSerializer(
        many=True,
    )

    class Meta:
        model = EventsBlock
        fields = (
            "title",
            "items",
        )


class VideosBlockSerializer(serializers.ModelSerializer):
    items = OrderedVideoSerializer(
        many=True,
        source="ordered_videos",
    )

    class Meta:
        model = VideosBlock
        fields = (
            "title",
            "items",
        )


class ImagesBlockSerializer(serializers.ModelSerializer):
    items = OrderedImageSerializer(
        many=True,
        source="ordered_images",
    )

    class Meta:
        model = ImagesBlock
        fields = (
            "title",
            "items",
        )


class PersonsBlockSerializer(serializers.ModelSerializer):
    items = ExtendedPersonSerializer(
        source="extended_persons",
        many=True,
    )

    class Meta:
        model = PersonsBlock
        fields = (
            "title",
            "items",
        )


class PlaysBlockSerializer(serializers.ModelSerializer):
    items = OrderedPlaySerializer(
        source="ordered_plays",
        many=True,
    )

    class Meta:
        model = PlaysBlock
        fields = (
            "title",
            "items",
        )
