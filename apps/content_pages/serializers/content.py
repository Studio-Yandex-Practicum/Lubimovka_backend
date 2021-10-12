from rest_framework import serializers

from apps.content_pages.models import (
    ContentPage,
    Image,
    ImagesBlock,
    Link,
    PerformancesBlock,
    PersonsBlock,
    PlaysBlock,
    Video,
    VideosBlock,
)
from apps.content_pages.serializers.content_blocks import (
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
        slug_field="model",
        read_only=True,
    )
    content_item = ContentObjectRelatedField(
        source="item",
        read_only=True,
    )


class ContentPageSerializer(serializers.ModelSerializer):
    contents = BaseContentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ContentPage
        fields = ["contents"]


class ModelWithContentPageSerializer(serializers.ModelSerializer):
    """
    Basic serializer for models with relations on ContentPage.
    The field 'contents' returns 'content_page' related object content and
    makes serialized objects look better.
    """

    contents = BaseContentSerializer(
        source="content_page.contents",
        many=True,
        read_only=True,
    )

    class Meta:
        model = None
        fields = [
            "name",
            "description",
            "image",
            "contents",
        ]
