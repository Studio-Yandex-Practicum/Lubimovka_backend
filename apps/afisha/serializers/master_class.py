from rest_framework import serializers

from apps.afisha.models import MasterClass
from apps.library.serializers import RoleSerializer


class EventMasterClassSerializer(serializers.ModelSerializer):
    """Master-class serializer for afisha page."""

    team = RoleSerializer(source="event_team", many=True)

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "team",
        )
