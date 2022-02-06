from rest_framework import serializers

from apps.info.models import PressRelease


class PressReleaseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="festival.press_release_image")

    class Meta:
        model = PressRelease
        fields = ("id", "image", "title", "text")


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())


class PhotoGalleryLinkSerializer(serializers.Serializer):
    photo_gallery_facebook_link = serializers.URLField()
