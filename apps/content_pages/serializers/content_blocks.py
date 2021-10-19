from rest_framework import serializers

from apps.content_pages.models import (
    ImagesBlock,
    OrderedImage,
    OrderedPerformance,
    OrderedPerson,
    OrderedPlay,
    OrderedVideo,
    PerformancesBlock,
    PersonsBlock,
    PlaysBlock,
    VideosBlock,
)
from apps.content_pages.serializers import (
    ImageSerializer,
    PerformanceSerializer,
    PersonSerializer,
    PlaySerializer,
    VideoSerializer,
)


class OrderedItemSerializerField(serializers.RelatedField):
    """
    A custom field to serialize 'OrderedItem' object.
    It takes 'value' class and finds related serializer. If none of
    serializers found exception raises.

    OrderedObject has to have item attribute.
    """

    def to_representation(self, value):
        assert hasattr(value, "item"), f"{value} has to have 'item' attribute."

        item_serializers = {
            OrderedImage: ImageSerializer,
            OrderedPerformance: PerformanceSerializer,
            OrderedPerson: PersonSerializer,
            OrderedPlay: PlaySerializer,
            OrderedVideo: VideoSerializer,
        }

        item_class = value._meta.model
        serializer = item_serializers.get(item_class, None)

        if not serializer:
            raise Exception("Unexpected type of ordered object")

        serializer = serializer(value.item)
        return serializer.data


class VideosBlockSerializer(serializers.ModelSerializer):

    items = OrderedItemSerializerField(
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
    items = OrderedItemSerializerField(
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
    items = OrderedItemSerializerField(
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
    items = OrderedItemSerializerField(
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
    items = OrderedItemSerializerField(
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
