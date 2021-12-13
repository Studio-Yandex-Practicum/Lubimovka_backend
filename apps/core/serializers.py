from rest_framework import serializers

from apps.core.models import Image, Person, Role


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор Изображения."""

    class Meta:
        model = Image
        fields = ("image",)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            "name",
            "slug",
        )


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = (
            "created",
            "modified",
        )
