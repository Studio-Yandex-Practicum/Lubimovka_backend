import logging

from anymail.exceptions import AnymailConfigurationError, AnymailError
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from googleapiclient.errors import HttpError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.views import APIView
from yadisk.exceptions import YaDiskError

from apps.core.models import Setting
from apps.library.models import ParticipationApplicationFestival
from apps.library.models.participation_application import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION
from apps.library.permissions import SettingsPlayReceptionPermission
from apps.library.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
from apps.library.services.email import send_application_email
from apps.library.services.spreadsheets import GoogleSpreadsheets
from apps.library.services.yandex_disk_export import yandex_disk_export

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
            try:
                yandex_disk_export(instance)
            except YaDiskError as error:
                logger.critical(error, exc_info=True)

            try:
                export_success = gs.export(instance=instance, domain=domain)
                if export_success:
                    instance.exported_to_google = True
                    instance.save()
            except (ValueError, HttpError) as error:
                logger.critical(error, exc_info=True)

            try:
                send_success = send_application_email(instance)
                if send_success:
                    instance.sent_to_email = True
                    instance.save()
            except (
                AnymailConfigurationError,
                AnymailError,
                ValueError,
            ) as error:
                msg = (
                    f"Не удалось отправить заявку на участие в фестивали id = {instance.id} "
                    f"на почту {Setting.get_setting('email_on_acceptance_of_plays_page')}."
                )
                logger.critical(msg, error, exc_info=True)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
