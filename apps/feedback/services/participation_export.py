import logging

from django.conf import settings

from apps.core.models import Setting
from apps.core.services.send_email import send_email
from apps.feedback.services.spreadsheets import GoogleSpreadsheets
from apps.feedback.services.yandex_disk_export import yandex_disk_export

logger = logging.getLogger("django")
gs = GoogleSpreadsheets()


class ParticipationExport:
    def yandex_disk(self, instance):
        download_link_in_yandex_disk = yandex_disk_export(instance)
        if download_link_in_yandex_disk:
            instance.url_file_in_storage = download_link_in_yandex_disk
            instance.saved_to_storage = True
            instance.file.delete()
            instance.save()
            return download_link_in_yandex_disk

    def google_sheets(self, instance, file_link):
        export_to_google_sheets_success = gs.export(instance, file_link)
        if export_to_google_sheets_success:
            instance.exported_to_google = True
            instance.save()

    def mail_send(self, instance, file_link):
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
            "file_link": file_link,
        }
        send_email_success = send_email(from_email, to_emails, template_id, context)
        if send_email_success:
            instance.sent_to_email = True
            instance.save()
