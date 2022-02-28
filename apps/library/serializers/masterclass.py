from rest_framework import serializers

from apps.library.models import MasterClass
from apps.library.serializers.role import RoleSerializer


class EventMasterClassSerializer(serializers.ModelSerializer):
    """Master-class serializer for afisha page."""

    team = RoleSerializer(source="event_team", many=True)
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
