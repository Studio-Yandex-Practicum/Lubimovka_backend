import logging

from django.conf import settings

from apps.core.models import Setting
from apps.core.services.send_email import send_email
from apps.feedback import services

logger = logging.getLogger("django")


class ParticipationApplicationExport:
    def __init__(self):
        settings_keys = (
            "email_send_from",
            "email_to_send_participations",
        )
        self.settings = Setting.get_settings(settings_keys=settings_keys)

    def yandex_disk_export(self, instance):
        download_link_in_yandex_disk = services.yandex_disk_export(instance)
        if download_link_in_yandex_disk:
            instance.url_file_in_storage = download_link_in_yandex_disk
            instance.saved_to_storage = True
            instance.file.delete()
            instance.save()
            return download_link_in_yandex_disk

    def google_sheets_export(self, instance, file_link):
        gs = services.GoogleSpreadsheets()
        export_to_google_sheets_success = gs.export(instance, file_link)
        if export_to_google_sheets_success:
            instance.exported_to_google = True
            instance.save()

    def mail_send_export(self, instance, file_link):
        from_email = self.settings.get("email_send_from")
        to_emails = (self.settings.get("email_to_send_participations"),)
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

    def export_application(self, instance, file_link):
        """Функция объединяющая экспорт на диск, в таблицу и отправку на почту."""
        yandex_disk_link = self.yandex_disk_export(instance)
        if yandex_disk_link is not None:
            file_link = yandex_disk_link
        self.google_sheets_export(instance, file_link)
        self.mail_send_export(instance, file_link)
