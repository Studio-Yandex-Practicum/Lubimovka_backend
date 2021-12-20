from rest_framework import serializers

from apps.library.models import MasterClass, TeamMember
from apps.library.utilities import team_collector


class EventMasterClassSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        return team_collector(TeamMember, {"masterclass": obj, "role__slug": "host"})

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
