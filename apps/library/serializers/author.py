from rest_framework import serializers

from apps.library.models import Author


class AuthorNameSerializer(serializers.ModelSerializer):
    """Сериализатор полного имени Автора"""

    name = serializers.ReadOnlyField(source="person.full_name")

    class Meta:
        model = Author
        fields = [
            "name",
        ]
