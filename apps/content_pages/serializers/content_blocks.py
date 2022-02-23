from rest_framework import serializers

from apps.afisha.models import Event
from apps.afisha.serializers.event import EventRegularSerializer
from apps.content_pages.models import EventsBlock, ImagesBlock, PersonsBlock, PlaysBlock, VideosBlock
from apps.content_pages.serializers import ExtendedPersonSerializer, OrderedImageSerializer, OrderedVideoSerializer
from apps.library.serializers import PlaySerializer as LibraryPlaySerializer
from apps.library.serializers.performance import EventPerformanceSerializer


class SlugRelatedSerializerField(serializers.SlugRelatedField):
    """The field works exactly as SlugRelatedField but returns full object serialized with 'serializer_class'."""

    def __init__(self, serializer_class=None, **kwargs):
        assert serializer_class is not None, "The 'serializer_class' argument is required."
        self.serializer_class = serializer_class
        super().__init__(**kwargs)

    def to_representation(self, obj):
        item = getattr(obj, self.slug_field)
        serializer = self.serializer_class(item, context=self.context)
        return serializer.data


class EventInBlockSerializer(EventRegularSerializer):
    """Returns Performance in EventsBlock."""

    event_body = EventPerformanceSerializer(source="common_event.target_model")

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
        read_only=True,
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
        read_only=True,
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
        read_only=True,
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
        read_only=True,
    )

    class Meta:
        model = PersonsBlock
        fields = (
            "title",
            "items",
        )


class PlaysBlockSerializer(serializers.ModelSerializer):
    items = SlugRelatedSerializerField(
        many=True,
        read_only=True,
        source="ordered_plays",
        slug_field="item",
        serializer_class=LibraryPlaySerializer,
    )

    class Meta:
        model = PlaysBlock
        fields = (
            "title",
            "items",
        )
