from rest_framework import serializers

from apps.core.models import Image


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор Изображения"""

    class Meta:
        model = Image
        fields = [
            "image",
        ]
