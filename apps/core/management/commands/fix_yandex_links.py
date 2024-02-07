import logging
import re

import yadisk
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.feedback import services
from apps.feedback.models.participation_application import ParticipationApplicationFestival
from apps.feedback.services.yandex_disk_export import publish_file

FILENAME_RE = re.compile(r"&filename=(.+?)&")
FAILED_TO_PUBLISH = "Cannot get public URL for application #{pk}"
GENERAL_FAILURE = "An error has occured while trying to fix yandex disk link in the database for application #{pk}"
SUCCESS = (
    "Link for application #{pk} was successfully updated from {old_url} to {new_url}; "
    "{rows} row(s) affected in the google table"
)

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Исправляет для файлов заявок временные ссылки Яндекс.Диск на постоянные при помощи публикации файлов"

    def handle(self, *args, **options):
        yndx = yadisk.YaDisk(token=settings.YNDX_DISK_TOKEN)
        gs = services.GoogleSpreadsheets()
        for application in ParticipationApplicationFestival.objects.filter(
            url_file_in_storage__contains="downloader.disk.yandex.ru"
        ):
            try:
                old_url = application.url_file_in_storage
                name = FILENAME_RE.search(old_url).groups()[0]
                if not name:
                    continue
                year = application.festival_year
                path = f"{year}/{name}"
                new_url = publish_file(yndx, path)
                if not new_url:
                    self.stdout.write(msg=FAILED_TO_PUBLISH.format(pk=application.pk), style_func=self.style.WARNING)
                    logger.warning(msg=FAILED_TO_PUBLISH.format(pk=application.pk))
                    continue
                application.url_file_in_storage = new_url
                rows_changed = gs.find_and_replace(old_url, f'=HYPERLINK("{new_url}" ; "{new_url}")')
                application.save()
                self.stdout.write(
                    msg=SUCCESS.format(pk=application.pk, old_url=old_url, new_url=new_url, rows=rows_changed),
                    style_func=self.style.SUCCESS,
                )
                logger.debug(msg=SUCCESS.format(pk=application.pk, old_url=old_url, new_url=new_url, rows=rows_changed))
            except Exception:
                self.stdout.write(msg=GENERAL_FAILURE.format(pk=application.pk), style_func=self.style.ERROR)
                logger.exception(msg=GENERAL_FAILURE.format(pk=application.pk))
        self.stdout.write(msg="Команда завершила работу", style_func=self.style.NOTICE)
