from rest_framework import serializers

from apps.info.models import Volunteer
from apps.info.serializers.person import PersonsSerializer


class VolunteersSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()

    class Meta:
        model = Volunteer
        exclude = ("created", "modified")
