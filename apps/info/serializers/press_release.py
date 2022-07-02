from rest_framework import serializers

from apps.info.models import PressRelease


class PressReleaseSerializer(serializers.ModelSerializer):
    """Сериализатор для станицы fo-press."""

    class Meta:
        model = PressRelease
        fields = (
            "text",
            "press_release_image",
        )


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())
