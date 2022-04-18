import logging

from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.views import APIView

from apps.core.models import Setting
from apps.core.utils import get_domain, send_email
from apps.library.models import ParticipationApplicationFestival
from apps.library.models.participation_application import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION
from apps.library.permissions import SettingsPlayReceptionPermission
from apps.library.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
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
        request=ParticipationSerializer,
        responses={
            201: None,
            400: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
            403: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
        },
    )
    def post(self, request):
        serializer = self.ParticipationSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            file_link = get_domain(request) + str(instance.file.url)

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
                instance.save()

            download_link_in_yandex_disk = yandex_disk_export(instance)
            if download_link_in_yandex_disk:
                instance.url_file_in_storage = download_link_in_yandex_disk
                instance.file.delete()
                instance.saved_to_storage = True
                instance.save()
                file_link = download_link_in_yandex_disk

            export_to_google_sheets_success = gs.export(instance, file_link)
            if export_to_google_sheets_success:
                instance.exported_to_google = True
                instance.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
