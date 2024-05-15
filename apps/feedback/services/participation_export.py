import logging

from django.conf import settings

from apps.core.models import Setting
from apps.core.services.send_email import send_email
from apps.feedback import services

logger = logging.getLogger("django")


class ParticipationApplicationExport:
    def _yandex_disk_export(self, instance):
        """Загрузка файла пьесы на Яндекс.Диск."""
        download_link_in_yandex_disk = (
            services.yandex_disk_export(instance) if Setting.get_setting("yandex_upload") else None
        )
        if download_link_in_yandex_disk:
            instance.url_file_in_storage = download_link_in_yandex_disk
            instance.saved_to_storage = True
            instance.save()
        return download_link_in_yandex_disk

    def _manage_local_file(self, instance):
        """Удаление файла на сервере, если его копия есть в облаке."""
        if instance.saved_to_storage:
            instance.file.delete()
            instance.save()

    def _google_sheets_export(self, instance, file_link):
        """Занесение сведений о заявке на участие в Google-таблицу."""
        gs = services.GoogleSpreadsheets()
        export_to_google_sheets_success = gs.export(instance, file_link)
        if export_to_google_sheets_success:
            instance.exported_to_google = True
            instance.save()

    def _get_email_settings(self):
        """Получение настроек, необходимых для отправки почтового уведомления."""
        settings_keys = (
            "email_send_from",
            "submit_play_email",
        )
        return Setting.get_settings(settings_keys=settings_keys)

    def _mail_send_export(self, instance, file_link):
        """Отправка почтового уведомления о новой заявке на участие."""
        try:
            email_settings = self._get_email_settings()
            from_email = email_settings.get("email_send_from")
            to_emails = (email_settings.get("submit_play_email"),)
            template_id = settings.MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION
            context = {
                "year": instance.year,
                "birth_year": instance.birth_year,
                "first_name": instance.first_name,
                "nickname": instance.nickname,
                "last_name": instance.last_name,
                "city": instance.city,
                "phone_number": instance.phone_number.as_international,
                "email": instance.email,
                "title": instance.title,
                "file_link": file_link,
                "file_path": instance.file.path,
            }
            send_email_success = send_email(from_email, to_emails, template_id, context, attach_file=True)
            if send_email_success:
                instance.sent_to_email = True
                instance.save()
            # Отправка подтверждения участнику
            send_email(from_email, (instance.email,), template_id, context, attach_file=True)
        except Exception:
            logger.critical(msg="Ошибка при подготовке сообщения электронной почты", exc_info=True)

    def export_application(self, instance, file_link):
        """Функция, объединяющая экспорт на диск, в таблицу и отправку на почту."""
        yandex_disk_link = self._yandex_disk_export(instance)
        if yandex_disk_link is not None:
            file_link = yandex_disk_link
        self._google_sheets_export(instance, file_link)
        self._mail_send_export(instance, file_link)
        self._manage_local_file(instance)
