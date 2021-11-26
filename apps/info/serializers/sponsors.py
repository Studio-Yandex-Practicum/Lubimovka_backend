from rest_framework import serializers

from apps.info.models import Sponsor
from apps.info.serializers.person import PersonsSerializer


class SponsorSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()

    class Meta:
        model = Sponsor
        exclude = ("created", "modified")


class SponsorsSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()

    class Meta:
        model = Sponsor
        fields = (
            "person",
            "position",
        )
