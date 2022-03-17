from rest_framework import serializers

from apps.library.models import Reading
from apps.library.serializers.role import RoleSerializer


class EventReadingSerializer(serializers.ModelSerializer):
    """Reading serializer for afisha page."""

    team = RoleSerializer(source="event_team", many=True)
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
