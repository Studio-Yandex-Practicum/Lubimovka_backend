from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.library.models import ParticipationApplicationFestival


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationApplicationFestival
        exclude = [
            "draft",
        ]

    def validate(self, data):
        """Raise model errors"""
        instance = ParticipationApplicationFestival(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.args[0])
        return data
