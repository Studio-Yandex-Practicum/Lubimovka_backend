from rest_framework import serializers

from apps.core.models import Image, MarkdownModel


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор Изображения"""

    class Meta:
        model = Image
        fields = [
            "image",
        ]


class MarkdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkdownModel
        exclude = ("created", "modified")
