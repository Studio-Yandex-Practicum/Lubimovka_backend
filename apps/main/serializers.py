from rest_framework import serializers

from apps.core.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class SettingsSerializer(serializers.Serializer):
    settings = serializers.ListField(
        child=serializers.CharField(max_length=100, min_length=3)
    )
