from rest_framework import serializers

from apps.content_pages.models import (
    Content,
    ContentPage,
    Image,
    ImagesBlock,
    OrderedImage,
    Text,
)


class BaseModelSerializer(serializers.ModelSerializer):
    object_type = serializers.SerializerMethodField()

    def get_object_type(self, obj):
        return obj.__class__.__name__.lower()


class TextSerializer(BaseModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"


class ImageSerializer(BaseModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class OrderedImageSerializer(BaseModelSerializer):
    class Meta:
        model = OrderedImage
        fields = "__all__"


class ImagesBlockSerializer(BaseModelSerializer):
    images = OrderedImageSerializer(
        many=True,
        read_only=True,
        source="ordered_images",
    )

    class Meta:
        model = ImagesBlock
        fields = "__all__"


class ContentsRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Text):
            serializer = TextSerializer(value)
        elif isinstance(value, Image):
            serializer = ImageSerializer(value)
        elif isinstance(value, ImagesBlock):
            serializer = ImagesBlockSerializer(value)
        else:
            raise Exception("Unexpected type of tagged object")
        return serializer.data


class ContentSerializer(serializers.ModelSerializer):
    content_item = ContentsRelatedField(
        source="item",
        read_only=True,
    )

    class Meta:
        model = Content
        fields = [
            "content_item",
            "order",
        ]


class ContentPageSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = ContentPage
        fields = [
            "title",
            "overview",
            "contents",
        ]
