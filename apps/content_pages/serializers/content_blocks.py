from rest_framework import serializers

from apps.content_pages.models import (
    Image,
    ImagesBlock,
    Link,
    PerformancesBlock,
    PersonsBlock,
    PlaysBlock,
    Video,
    VideosBlock,
)
from apps.content_pages.serializers import (
    ImageSerializer,
    LinkSerializer,
    PerformanceSerializer,
    PersonSerializer,
    PlaySerializer,
    VideoSerializer,
)
from apps.library.models import Performance, Person, Play


class OrderedItemSerializerField(serializers.Field):
    """
    A custom field to serialize 'OrderedItem' object.
    It takes 'value' class and finds related serializer. If none of
    serializers found exception raises.
    """

    def to_representation(self, value):

        item_serializers = {
            Image: ImageSerializer,
            Link: LinkSerializer,
            Video: VideoSerializer,
            Performance: PerformanceSerializer,
            Play: PlaySerializer,
            Person: PersonSerializer,
        }

        item_class = value._meta.model
        serializer = item_serializers.get(item_class, None)

        if not serializer:
            raise Exception("Unexpected type of ordered object")

        serializer = serializer(value)
        return serializer.data


class BaseOrderedItemSerializer(serializers.Serializer):
    """OrderedItem object serializer.

    The serializer is independent of model class because OrderedItems
    has to have only two fields:
        - item
        - order
    """

    item = OrderedItemSerializerField()
    order = serializers.IntegerField()


class VideosBlockSerializer(serializers.ModelSerializer):

    items = BaseOrderedItemSerializer(
        many=True,
        read_only=True,
        source="ordered_videos",
    )

    class Meta:
        model = VideosBlock
        fields = [
            "title",
            "items",
        ]


class ImagesBlockSerializer(serializers.ModelSerializer):
    items = BaseOrderedItemSerializer(
        many=True,
        read_only=True,
        source="ordered_images",
    )

    class Meta:
        model = ImagesBlock
        fields = [
            "title",
            "items",
        ]


class PerformancesBlockSerializer(serializers.ModelSerializer):
    items = BaseOrderedItemSerializer(
        many=True,
        read_only=True,
        source="ordered_performances",
    )

    class Meta:
        model = PerformancesBlock
        fields = [
            "title",
            "items",
        ]


class PersonsBlockSerializer(serializers.ModelSerializer):
    items = BaseOrderedItemSerializer(
        many=True,
        read_only=True,
        source="ordered_persons",
    )

    class Meta:
        model = PersonsBlock
        fields = [
            "title",
            "items",
        ]


class PlaysBlockSerializer(serializers.ModelSerializer):
    items = BaseOrderedItemSerializer(
        many=True,
        read_only=True,
        source="ordered_plays",
    )

    class Meta:
        model = PlaysBlock
        fields = [
            "title",
            "items",
        ]
