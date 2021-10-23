from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.library.models import Participant


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        exclude = [
            "verified",
        ]

    def validate(self, data):
        """Raise model errors"""
        instance = Participant(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.args[0])
        return data
