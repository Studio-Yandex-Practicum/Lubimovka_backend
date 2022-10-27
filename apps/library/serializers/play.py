from rest_framework import serializers

from apps.core.utils import get_domain
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
    url_download = serializers.SerializerMethodField()

    def get_url_download(self, obj) -> str:
        if obj.url_download_from:
            return obj.url_download_from
        else:
            return get_domain(self.context["request"]) + obj.url_download.url

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


class AuthorPlaySerializer(PlaySerializer):
    """Сериализатор Пьесы из промежуточной модели м2м Автор-Пьеса.

    Используется для сортировки выдачи пьес.
    """

    def to_representation(self, obj):
        return super().to_representation(obj.play)


class AuthorOtherPlaySerializer(AuthorPlaySerializer):
    """Сериализатор Пьесы из промежуточной модели м2м Автор-Пьеса.

    Используется для сортировки выдачи других пьес (не пьес Любимовки).
    """

    class Meta:
        fields = (
            "id",
            "name",
            "authors",
            "url_download",
        )
        model = Play
