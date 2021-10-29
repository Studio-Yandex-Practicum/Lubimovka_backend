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

    def to_representation(self, obj):
        """Serialize content objects to a simple representation."""

        content_item_serializers = {
            Image: ImageSerializer,
            ImagesBlock: ImagesBlockSerializer,
            Link: LinkSerializer,
            PerformancesBlock: PerformancesBlockSerializer,
            PersonsBlock: PersonsBlockSerializer,
            PlaysBlock: PlaysBlockSerializer,
            Video: VideoSerializer,
            VideosBlock: VideosBlockSerializer,
        }

        content_item_class = obj._meta.model
        serializer = content_item_serializers.get(content_item_class, None)

        if not serializer:
            raise Exception("Unexpected type of content object block.")

        serializer = serializer(obj, context=self.context)
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
