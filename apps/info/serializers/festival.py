from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.info.models import Festival
from apps.info.models.festival import InfoLink
from apps.info.serializers.selectors import SelectorInFestivalSerializer
from apps.info.serializers.volunteers import VolunteerInFestivalSerializer


class InfoLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoLink
        fields = ("title", "link")


class FestivalSerializer(serializers.ModelSerializer):
    volunteers = serializers.SerializerMethodField()
    selectors = serializers.SerializerMethodField()
    plays_links = InfoLinkSerializer(many=True)
    additional_links = InfoLinkSerializer(many=True)

    @extend_schema_field(VolunteerInFestivalSerializer(many=True))
    def get_volunteers(self, obj):
        serializer = VolunteerInFestivalSerializer
        volunteers = obj.volunteers.all()
        return serializer(volunteers, many=True).data

    @extend_schema_field(SelectorInFestivalSerializer(many=True))
    def get_selectors(self, obj):
        serializer = SelectorInFestivalSerializer
        selectors = obj.selectors.all()
        return serializer(selectors, many=True).data

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
            "selectors",
            "images",
            "plays_links",
            "additional_links",
        )


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())
