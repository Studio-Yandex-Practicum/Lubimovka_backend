from rest_framework import serializers

from apps.library.models import Author, Play


class AuthorForPlaySerializer(serializers.ModelSerializer):
    """Сериализатор полного имени Автора."""

    name = serializers.ReadOnlyField(source="person.full_name")

    class Meta:
        model = Author
        fields = ("name", "slug")


class PlaySerializer(serializers.ModelSerializer):
    """Сериализатор Пьесы."""

    authors = AuthorForPlaySerializer(many=True)
    city = serializers.CharField(required=False, max_length=200, label="Город")
    year = serializers.IntegerField(required=False, min_value=0, max_value=32767, label="Год написания пьесы")
    url_reading = serializers.URLField(required=False)

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


class AuthorPlaySerializer(serializers.Serializer):
    """Сериализатор Пьесы из промежуточной модели м2м Автор-Пьеса.

    Используется для сортировки выдачи пьес.
    """

    id = serializers.IntegerField(source="play.id")
    name = serializers.CharField(source="play.name")
    authors = AuthorForPlaySerializer(source="play.authors", many=True)
    city = serializers.CharField(source="play.city", required=False, max_length=200, label="Город")
    year = serializers.IntegerField(
        source="play.year", required=False, min_value=0, max_value=32767, label="Год написания пьесы"
    )
    url_download = serializers.URLField(source="play.url_download")
    url_reading = serializers.URLField(source="play.url_reading", required=False)


class AuthorOtherPlaySerializer(serializers.Serializer):
    """Сериализатор Пьесы из промежуточной модели м2м Автор-Пьеса.

    Используется для сортировки выдачи других пьес (не пьес Любимовки).
    """

    id = serializers.IntegerField(source="play.id")
    name = serializers.CharField(source="play.name")
    authors = AuthorForPlaySerializer(source="play.authors", many=True)
    url_download = serializers.URLField(source="play.url_download")
