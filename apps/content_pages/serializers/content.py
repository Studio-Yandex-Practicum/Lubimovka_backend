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
    ImagesBlockSerializer,
    ImageSerializer,
    LinkSerializer,
    PerformancesBlockSerializer,
    PersonsBlockSerializer,
    PlaysBlockSerializer,
    VideosBlockSerializer,
    VideoSerializer,
)


class ContentObjectRelatedField(serializers.RelatedField):
    """
    Custom related field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        """Serialize content objects to a simple representation."""
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
            # FYI try to uncomment the line after the comment and see
            # serialized result.
            # It looks great but we can't use serialization like that:
            # blocks with array of elements has to have static fields.

            # serializer = VideoSerializer(value.items, many=True)
            serializer = VideosBlockSerializer(value)
        else:
            raise Exception("Unexpected type of content object")
        return serializer.data


class BaseContentSerializer(serializers.Serializer):
    content_type = serializers.SlugRelatedField(
        slug_field="model",
        read_only=True,
    )
    content_item = ContentObjectRelatedField(
        source="item",
        read_only=True,
    )
