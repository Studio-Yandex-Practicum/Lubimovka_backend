from rest_framework import serializers

from apps.library.models import Reading
from apps.library.utilities_team_data import team_data


class EventReadingSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        return team_data(obj, {"team_members__reading": obj, "slug__in": ["director", "dramatist"]})

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
