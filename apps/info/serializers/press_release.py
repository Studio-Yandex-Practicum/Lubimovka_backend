from rest_framework import serializers

from apps.core.models import Person
from apps.core.serializers import PersonSerializer
from apps.info.models import PressRelease


class PressReleaseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="festival.press_release_image")
    pr_manager = serializers.SerializerMethodField()

    def get_pr_manager(self, obj):
        item = Person.objects.filter(festivalteam__is_pr_manager=True)
        if not item:
            return "Нет PR-менеджера"
        return PersonSerializer(item, many=True).data

    class Meta:
        model = PressRelease
        fields = (
            "id",
            "image",
            "title",
            "text",
            "pr_manager",
        )


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())


class PhotoGalleryLinkSerializer(serializers.Serializer):
    photo_gallery_facebook_link = serializers.URLField()
