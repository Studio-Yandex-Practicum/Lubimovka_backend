from rest_framework import serializers

from apps.afisha.models import Reading
from apps.library.serializers import RoleSerializer


class EventReadingSerializer(serializers.ModelSerializer):
    """Reading serializer for afisha page."""

    team = RoleSerializer(source="event_team", many=True)
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, required=False, source="project")

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
