from rest_framework import serializers

from apps.library.models import Play
from apps.library.serializers import PerformancePlayAuthorSerializer


class PerformancePlaySerializer(serializers.ModelSerializer):
    """Сериализатор Пьесы для вложения в сериализатор Спектакля"""

    authors = PerformancePlayAuthorSerializer(many=True)

    class Meta:
        fields = (
            "name",
            "authors",
            "city",
            "year",
            "url_download",
            "url_reading",
        )
        model = Play
