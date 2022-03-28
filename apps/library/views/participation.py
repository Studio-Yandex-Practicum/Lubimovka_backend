import logging

from anymail.exceptions import AnymailConfigurationError, AnymailError
from drf_spectacular.utils import extend_schema
from googleapiclient.errors import HttpError
from rest_framework import mixins, viewsets

from apps.library.permissions import SettingsPlayReceptionPermission
from apps.library.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
from apps.library.serializers.participation import ParticipationSerializer
from apps.library.services.email import send_application_email
from apps.library.services.spreadsheets import GoogleSpreadsheets
from config.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

gs = GoogleSpreadsheets()


@extend_schema(
    responses={
        201: ParticipationSerializer,
        400: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
        403: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
    }
)
class ParticipationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [SettingsPlayReceptionPermission]
    serializer_class = ParticipationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        domain = self.request.build_absolute_uri()
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
            msg = f"Не удалось отправить заявку id = {instance.id} на почту.\n{error}"
            logger.critical(msg, exc_info=True)
