from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.info.models import Festival
from apps.info.serializers.volunteers import VolunteerInFestivalSerializer


class FestivalLinkSerializer(serializers.Serializer):
    description = serializers.CharField(source="link.description")
    url = serializers.URLField(source="link.url")


class FestivalSerializer(serializers.ModelSerializer):
    volunteers = serializers.SerializerMethodField()
    plays_links = FestivalLinkSerializer(many=True)
    additional_links = FestivalLinkSerializer(many=True)

    @extend_schema_field(VolunteerInFestivalSerializer(many=True))
    def get_volunteers(self, obj):
        serializer = VolunteerInFestivalSerializer
        volunteers = obj.volunteers.all()
        return serializer(volunteers, many=True).data

    class Meta:
        model = Festival
        depth = 1
        fields = (
            "id",
            "start_date",
            "end_date",
            "description",
            "year",
            "plays_count",
            "selected_plays_count",
            "selectors_count",
            "volunteers_count",
            "events_count",
            "cities_count",
            "video_link",
            "blog_entries",
            "press_release_image",
            "volunteers",
            "images",
            "plays_links",
            "additional_links",
        )


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())
