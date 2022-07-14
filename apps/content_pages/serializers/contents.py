from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema_field
from rest_framework import serializers

from apps.content_pages.models import (
    ContentUnitRichText,
    EventsBlock,
    ImagesBlock,
    Link,
    PersonsBlock,
    PlaysBlock,
    VideosBlock,
)
from apps.content_pages.serializers import (
    ContentUnitRichTextSerializer,
    EventsBlockSerializer,
    ImagesBlockSerializer,
    LinkSerializer,
    PersonsBlockSerializer,
    PlaysBlockSerializer,
    VideosBlockSerializer,
)

CONTENT_OBJECT_SERIALIZER_PAIRS = {
    ContentUnitRichText: ContentUnitRichTextSerializer,
    EventsBlock: EventsBlockSerializer,
    ImagesBlock: ImagesBlockSerializer,
    Link: LinkSerializer,
    PersonsBlock: PersonsBlockSerializer,
    PlaysBlock: PlaysBlockSerializer,
    VideosBlock: VideosBlockSerializer,
}


@extend_schema_field(
    PolymorphicProxySerializer(
        component_name="Content_object",
        serializers=CONTENT_OBJECT_SERIALIZER_PAIRS.values(),
        resource_type_field_name=None,
    )
)
class ContentObjectRelatedField(serializers.RelatedField):
    """Custom related field to use for the "content_object" generic relationship."""

    def to_representation(self, obj):
        """Serialize content objects to a simple representation."""
        # to think: if amount of types of objects increases may be easier to
        # get serializer_class by name (for example look for
        # SerializerMethodField sources)
        content_item_serializers = CONTENT_OBJECT_SERIALIZER_PAIRS

        content_item_class = obj._meta.model
        serializer_class = content_item_serializers.get(content_item_class, None)

        if not serializer_class:
            raise Exception("Unexpected type of content object block.")

        serializer = serializer_class(obj, context=self.context)
        return serializer.data


class BaseContentSerializer(serializers.Serializer):
    """Content (Item/Block) Serializer.

    1. "content_type" returns type of content item
    2. "content_item" recognized type of item and serialize it
    """

    content_type = serializers.SlugRelatedField(
        slug_field="model",
        read_only=True,
    )
    content_item = ContentObjectRelatedField(
        source="item",
        read_only=True,
    )


class BaseContentPageSerializer(serializers.Serializer):
    """Add `contents` field to any serializer."""

    contents = BaseContentSerializer(
        many=True,
        read_only=True,
    )
