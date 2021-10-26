from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.library.models import ParticipationApplicationFestival


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationApplicationFestival
        exclude = [
            "verified",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=ParticipationApplicationFestival.objects.all(),
                fields=[
                    "first_name",
                    "last_name",
                    "birthday",
                    "city",
                    "phone_number",
                    "email",
                    "title",
                    "year",
                ],
            )
        ]
