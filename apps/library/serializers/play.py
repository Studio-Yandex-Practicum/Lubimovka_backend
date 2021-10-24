from rest_framework import serializers

from apps.library.models import Play
from apps.library.serializers import AuthorNameSerializer


class PlaySerializer(serializers.ModelSerializer):
    """Сериализатор Пьесы"""

    authors = AuthorNameSerializer(many=True)

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
