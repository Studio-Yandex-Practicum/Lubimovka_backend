from rest_framework import serializers

from apps.info.models import PressRelease


class PressReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressRelease
        fields = (
            "id",
            "title",
            "text",
        )


class ImageYearPressReleaseSerializer(serializers.Serializer):
    image = serializers.ImageField(default=None)
    years = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True,
    )
    press_releases = PressReleaseSerializer(
        default=None,
        many=True,
    )
