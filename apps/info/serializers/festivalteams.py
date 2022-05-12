from rest_framework import serializers

from apps.info.models import FestivalTeamMember
from apps.info.serializers.person import PersonsSerializer


class FestivalTeamsSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()

    class Meta:
        model = FestivalTeamMember
        exclude = ("created", "modified", "order")
