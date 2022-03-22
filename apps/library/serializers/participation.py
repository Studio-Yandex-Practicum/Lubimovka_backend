from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.library.models import ParticipationApplicationFestival
from apps.library.models.participation_application import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION


class ParticipationSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(
        min_value=1900,
        max_value=timezone.now().year,
        label="Год написания",
    )
    birth_year = serializers.IntegerField(
        min_value=1900,
        max_value=timezone.now().year,
        label="Год рождения",
    )
    url_file_in_storage = serializers.URLField(read_only=True)

    class Meta:
        model = ParticipationApplicationFestival
        exclude = [
            "verified",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=ParticipationApplicationFestival.objects.all(),
                fields=UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION,
            )
        ]
