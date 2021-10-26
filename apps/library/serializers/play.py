from rest_framework import serializers

from apps.library.models import Author, Play


class AuthorForPlaySerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        source="person", slug_field="full_name", read_only=True
    )

    class Meta:
        model = Author
        fields = ["name"]


class PlaySerializer(serializers.ModelSerializer):
    authors = AuthorForPlaySerializer(many=True)

    class Meta:
        model = Play
        fields = ["id", "name", "authors", "city", "year"]
