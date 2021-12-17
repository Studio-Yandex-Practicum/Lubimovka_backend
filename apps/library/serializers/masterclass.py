from rest_framework import serializers

from apps.library.models import MasterClass, TeamMember
from apps.library.utilities import team_collector_with_plural_slug


class EventMasterClassSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project = serializers.SlugRelatedField(slug_field="title", read_only=True)

    def get_team(self, obj):
        return team_collector_with_plural_slug(TeamMember, {"masterclass": obj, "role__slug": "host"})

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project",
        )
