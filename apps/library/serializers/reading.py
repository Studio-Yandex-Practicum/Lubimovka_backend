from rest_framework import serializers

from apps.library.models import Reading, TeamMember
from apps.library.utilities import team_collector_with_plural_slug


class EventReadingSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project = serializers.SlugRelatedField(slug_field="title", read_only=True)

    def get_team(self, obj):
        return team_collector_with_plural_slug(
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
