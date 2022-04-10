import logging

from django.conf import settings
from drf_spectacular.utils import extend_schema
from googleapiclient.errors import HttpError
from rest_framework import mixins, viewsets
from yadisk.exceptions import YaDiskError

from apps.core.models import Setting
from apps.core.utils import send_email
from apps.library.permissions import SettingsPlayReceptionPermission
from apps.library.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
from apps.library.serializers.participation import ParticipationSerializer
from apps.library.services.spreadsheets import GoogleSpreadsheets
from apps.library.services.yandex_disk_export import yandex_disk_export

logger = logging.getLogger("django")

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
        domain = settings.DOMAIN_URL

        try:
            from_email = Setting.get_setting("email_send_from")
            to_emails = (Setting.get_setting("email_to_send_participations"),)
            template_id = settings.MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION

            context = {
                "year": instance.year,
                "birth_year": instance.birth_year,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "city": instance.city,
                "phone_number": instance.phone_number.as_international,
                "email": instance.email,
                "title": instance.title,
                "file_path": instance.file.path,
            }
            send_email_success = send_email(from_email, to_emails, template_id, context, attach_file=True)
            if send_email_success:
                instance.sent_to_email = True

            download_link_in_yandex_disk = yandex_disk_export(instance)
            if download_link_in_yandex_disk:
                instance.url_file_in_storage = download_link_in_yandex_disk
                instance.file.delete()
                instance.saved_to_storage = True

            file_url = download_link_in_yandex_disk if download_link_in_yandex_disk else domain + str(instance.file.url)

            export_to_google_sheets_success = gs.export(instance, file_url)
            if export_to_google_sheets_success:
                instance.exported_to_google = True

            instance.save()

        except YaDiskError as error:
            msg = f"Не удалось загрузить пьесу {instance.title} от {instance.email} на Яндекс диск."
            logger.critical(msg, error, exc_info=True)
        except (ValueError, HttpError) as error:
            msg = f"Не удалось выгрузить данные заявки от {instance.email} на Google Sheets."
            logger.critical(msg, error, exc_info=True)
