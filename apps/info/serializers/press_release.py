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
