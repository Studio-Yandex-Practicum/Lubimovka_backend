from rest_framework import serializers

from apps.library.serializers import PlaySerializer as LibraryPlaySerializer

from ..models import ImagesBlock, PerformancesBlock, PersonsBlock, PlaysBlock, VideosBlock
from ..serializers import (
    ContentImagesBlockItemSerializer,
    ExtendedPersonSerializer,
    OrderedVideoSerializer,
    PerformanceSerializer,
)


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
    items = ContentImagesBlockItemSerializer(
        many=True,
        read_only=True,
        source="block_items",
    )

    class Meta:
        model = ImagesBlock
        fields = (
            "title",
            "items",
        )


class PerformancesBlockSerializer(serializers.ModelSerializer):
    items = SlugRelatedSerializerField(
        many=True,
        read_only=True,
        source="ordered_performances",
        slug_field="item",
        serializer_class=PerformanceSerializer,
    )

    class Meta:
        model = PerformancesBlock
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
