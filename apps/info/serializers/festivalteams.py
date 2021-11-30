from rest_framework import serializers

from apps.info.models import FestivalTeam
from apps.info.serializers.person import PersonsSerializer


class FestivalTeamsSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()

    class Meta:
        model = FestivalTeam
        exclude = (
            "created",
            "modified",
        )
