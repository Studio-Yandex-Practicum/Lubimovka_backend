from rest_framework import serializers

from apps.core.utilities import team_collector
from apps.library.models import Reading, TeamMember


class EventReadingSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project = serializers.SlugRelatedField(slug_field="title", read_only=True)

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
            "project",
        )
