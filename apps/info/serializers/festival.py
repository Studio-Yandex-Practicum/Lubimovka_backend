from rest_framework import serializers

from apps.info.models import Festival, InfoLink


class InfoLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoLink
        fields = ("title", "link")


class FestivalSerializer(serializers.ModelSerializer):
    plays_links = InfoLinkSerializer(many=True)
    additional_links = InfoLinkSerializer(many=True)

    class Meta:
        model = Festival
        depth = 1
        fields = (
            "id",
            "start_date",
            "end_date",
            "description",
            "plays_count",
            "selected_plays_count",
            "selectors_count",
            "selectors_page_link",
            "volunteers_count",
            "events_count",
            "cities_count",
            "video_link",
            "blog_entries",
            "festival_image",
            "images",
            "plays_links",
            "additional_links",
        )
        read_only_fields = ("year",)


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())
