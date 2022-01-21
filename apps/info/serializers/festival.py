from rest_framework import serializers

from apps.info.models import Festival
from apps.info.serializers.volunteers import VolunteersSerializer


class FestivalSerializer(serializers.ModelSerializer):
    volunteers = serializers.SerializerMethodField()

    def get_volunteers(self, obj):
        serializer = VolunteersSerializer
        volunteers = obj.volunteer.all()
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
        )


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(child=serializers.IntegerField())
