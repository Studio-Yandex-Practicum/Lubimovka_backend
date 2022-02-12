from rest_framework import serializers

from apps.core.models import Person, Setting
from apps.info.models import PressRelease


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """A ModelSerializer that takes an additional `fields` argument that controls which fields should be displayed."""

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ManagerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class PressReleaseSerializer(serializers.ModelSerializer):
    """Сериализатор для станицы fo-press."""

    image = serializers.ImageField(source="festival.press_release_image")
    photo_gallery_link = serializers.SerializerMethodField()
    name_manager = serializers.SerializerMethodField()
    pr_manager = serializers.SerializerMethodField()

    def get_name_manager(self, obj):
        """Получаем данные о менеджере в дательном падеже."""
        text = Setting.objects.filter(settings_key="press_release_data").values("text").first()
        return ManagerDataSerializer(text).data

    def get_pr_manager(self, obj):
        """Получаем аватар и почту менеджера."""
        item = Person.objects.get(festivalteam__is_pr_manager=True)
        return ManagerSerializer(
            item,
            fields=(
                "image",
                "email",
            ),
        ).data

    def get_photo_gallery_link(self, obj):
        """Получаем ссылку на галерею в facebook."""
        items = Setting.objects.filter(settings_key="photo_gallery_facebook").values("url").first()
        return PhotoGalleryLinkSerializer(items).data

    class Meta:
        model = PressRelease
        fields = (
            "id",
            "image",
            "title",
            "text",
            "photo_gallery_link",
            "name_manager",
            "pr_manager",
        )


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())


class PhotoGalleryLinkSerializer(serializers.Serializer):
    url = serializers.URLField()


class ManagerDataSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100)
