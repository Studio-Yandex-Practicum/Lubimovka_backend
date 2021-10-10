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

from .image import ImagesBlockSerializer, ImageSerializer
from .link import LinkSerializer
from .performance import PerformancesBlockSerializer
from .person import PersonsBlockSerializer
from .play import PlaysBlockSerializer
from .video import VideosBlockSerializer, VideoSerializer


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize content objects to a simple representation.
        """

        if isinstance(value, Image):
            serializer = ImageSerializer(value)
        elif isinstance(value, ImagesBlock):
            serializer = ImagesBlockSerializer(value)
        elif isinstance(value, Link):
            serializer = LinkSerializer(value)
        elif isinstance(value, PerformancesBlock):
            serializer = PerformancesBlockSerializer(value)
        elif isinstance(value, PersonsBlock):
            serializer = PersonsBlockSerializer(value)
        elif isinstance(value, PlaysBlock):
            serializer = PlaysBlockSerializer(value)
        elif isinstance(value, Video):
            serializer = VideoSerializer(value)
        elif isinstance(value, VideosBlock):
            serializer = VideosBlockSerializer(value)
        else:
            raise Exception("Unexpected type of content object")
        return serializer.data


class BaseContentSerializer(serializers.Serializer):
    order = serializers.IntegerField()
    content_type = serializers.SlugRelatedField(
        source="content_item.content_type",
        slug_field="model",
        read_only=True,
    )
    content_item = ContentObjectRelatedField(
        source="content_item.item",
        read_only=True,
    )
