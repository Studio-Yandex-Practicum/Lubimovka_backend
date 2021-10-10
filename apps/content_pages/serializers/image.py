from rest_framework import serializers

from apps.content_pages.models import Image, ImagesBlock, OrderedImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "title",
            "file",
        ]


class OrderedImageSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = OrderedImage
        fields = [
            "order",
            "image",
        ]


class ImagesBlockSerializer(serializers.ModelSerializer):
    images = OrderedImageSerializer(
        many=True,
        read_only=True,
        source="ordered_images",
    )

    class Meta:
        model = ImagesBlock
        fields = [
            "title",
            "images",
        ]
