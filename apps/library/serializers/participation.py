from rest_framework import serializers

from apps.library.models import ParticipationApplicationFestival


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationApplicationFestival
        exclude = [
            "verified",
        ]
