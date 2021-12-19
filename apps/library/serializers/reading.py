from rest_framework import serializers

from apps.library.models import Reading, TeamMember
from apps.library.utilities import team_collector


class EventReadingSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        return team_collector(
            TeamMember,
            {"reading": obj, "role__slug__in": ["director", "dramatist"]},
        )

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
