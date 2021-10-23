from rest_framework import serializers

from apps.library.models import Author


class AuthorsInPlayInPerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Автора для вложения в сериализатор Пьесы,
    который, в свою очередь, вложен в сериализатор Спектакля"""

    name = serializers.ReadOnlyField(source="person.full_name")

    class Meta:
        model = Author
        fields = ("name",)
