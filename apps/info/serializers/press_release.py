from rest_framework import serializers

from apps.core.models import Setting
from apps.info.models import PressRelease
from apps.info.utils import get_data


class PressReleaseSerializer(serializers.ModelSerializer):
    """Сериализатор для станицы fo-press."""

    image = serializers.ImageField(source="festival.press_release_image")
    pr_manager = serializers.SerializerMethodField()
    photo_gallery_link = serializers.SerializerMethodField()

    def get_pr_manager(self, obj):
        data = Setting.objects.filter(settings_key__startswith="press_release_").values("text", "image", "email")
        result = get_data(data)
        return PRManager_data(result).data

    def get_photo_gallery_link(self, obj):
        item = Setting.objects.filter(settings_key="photo_gallery_facebook").values("url")
        return PhotoGalleryLinkSerializer(item, many=True).data

    class Meta:
        model = PressRelease
        fields = (
            "id",
            "image",
            "title",
            "text",
            "photo_gallery_link",
            "pr_manager",
        )


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())


class PhotoGalleryLinkSerializer(serializers.Serializer):
    # photo_gallery_facebook_link = serializers.URLField()
    url = serializers.URLField()


class PRManager_data(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    image = serializers.ImageField()
