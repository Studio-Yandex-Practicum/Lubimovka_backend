import logging
import threading

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.views import APIView

from apps.core.utils import get_domain
from apps.feedback.models import ParticipationApplicationFestival
from apps.feedback.models.participation_application import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION
from apps.feedback.permissions import SettingsPlayReceptionPermission
from apps.feedback.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
from apps.feedback.services.participation_export import ParticipationExport

logger = logging.getLogger("django")


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
        request=ParticipationSerializer,
        responses={
            201: None,
            400: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
            403: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
        },
    )
    def post(self, request):
        serializer = self.ParticipationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()
        file_link = get_domain(request) + str(instance.file.url)

        export = ParticipationExport()
        thread_for_services = threading.Thread(target=export.export_main, args=(instance, file_link))
        thread_for_services.start()
        return Response(status=status.HTTP_201_CREATED)
