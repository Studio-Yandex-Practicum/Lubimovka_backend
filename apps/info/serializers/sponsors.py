from rest_framework import serializers

from apps.info.models import Sponsor
from apps.info.serializers import PersonsSerializer


class SponsorSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()

    class Meta:
        model = Sponsor
        fields = ("id", "person", "position")
