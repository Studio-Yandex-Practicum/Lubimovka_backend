from rest_framework import serializers

from apps.info.models import PressRelease


class PressReleaseSerializer(serializers.ModelSerializer):
    """Сериализатор для станицы fo-press."""

    image = serializers.ImageField(source="festival.press_release_image")

    class Meta:
        model = PressRelease
        fields = ("id", "image")


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())
