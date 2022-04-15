import logging

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.views import APIView

from apps.library.models import ParticipationApplicationFestival
from apps.library.models.participation_application import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION
from apps.library.permissions import SettingsPlayReceptionPermission
from apps.library.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
from apps.library.services.spreadsheets import GoogleSpreadsheets
from apps.library.utilities import participation_services

logger = logging.getLogger("django")

gs = GoogleSpreadsheets()


class ParticipationViewSet(APIView):
    permission_classes = [SettingsPlayReceptionPermission]

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
            exclude = ["verified", "festival_year"]
            validators = [
                UniqueTogetherValidator(
                    queryset=ParticipationApplicationFestival.objects.all(),
                    fields=UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION,
                )
            ]

    @extend_schema(
        responses={
            201: ParticipationSerializer,
            400: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
            403: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
        }
    )
    def post(self, request):
        serializer = self.ParticipationSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            domain = self.request.build_absolute_uri()

            participation_services(instance, domain, gs, logger)

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
