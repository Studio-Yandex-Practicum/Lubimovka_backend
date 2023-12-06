from rest_framework import serializers

from apps.afisha.models import Reading
from apps.library.serializers import RoleSerializer


class EventReadingSerializer(serializers.ModelSerializer):
    """Reading serializer for afisha page."""

    team = RoleSerializer(source="event_team", many=True)

    class Meta:
        model = Reading
        fields = (
            "id",
            "custom_type",
            "name",
            "description",
            "team",
        )
