from rest_framework import serializers

from apps.library.models import Play
from apps.library.serializers import AuthorsInPlayInPerformanceSerializer


class PlayInPerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Пьесы для вложения в сериализатор Спектакля"""

    authors = AuthorsInPlayInPerformanceSerializer(many=True)

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
