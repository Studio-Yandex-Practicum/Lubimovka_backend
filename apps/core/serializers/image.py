from rest_framework import serializers

from apps.core.models import Image


class ImagesInBlockInPerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Изображения для вложения в сериализатор Спектакля"""

    class Meta:
        model = Image
        fields = [
            "image",
        ]
