from rest_framework import serializers

from apps.library.models import Author, Play


class AuthorForPlaySerializer(serializers.ModelSerializer):
    """Сериализатор полного имени Автора"""

    name = serializers.ReadOnlyField(source="person.full_name")

    class Meta:
        model = Author
        fields = ("name",)


class PlaySerializer(serializers.ModelSerializer):
    """Сериализатор Пьесы"""

    authors = AuthorForPlaySerializer(many=True)

    class Meta:
        fields = (
            "id",
            "name",
            "authors",
            "city",
            "year",
            "url_download",
            "url_reading",
        )
        model = Play
