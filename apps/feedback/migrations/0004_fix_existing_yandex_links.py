# Generated by Django 3.2.16 on 2023-02-21 20:17
import logging
import re

import yadisk
from django.db import migrations
from django.conf import settings

from apps.feedback.services.yandex_disk_export import publish_file

FILENAME_RE = re.compile(r"&filename=(.+?)&")
FAILED_TO_PUBLISH = "Cannot get public URL for application #{pk}"
GENERAL_FAILURE = "An error has occured while trying to fix yandex disk link for application #{pk}"

logger = logging.getLogger("django")


def fix_links(apps, schema_editor):
    yndx = yadisk.YaDisk(token=settings.YNDX_DISK_TOKEN)
    Application = apps.get_model('feedback', 'ParticipationApplicationFestival')
    for application in Application.objects.filter(url_file_in_storage__contains="downloader.disk.yandex.ru"):
        try:
            name = FILENAME_RE.search(application.url_file_in_storage).groups()[0]
            if not name:
                continue
            year = application.festival_year
            path = f"{year}/{name}"
            url = publish_file(yndx, path)
            if not url:
                logger.warning(msg=FAILED_TO_PUBLISH.format(pk=application.pk))
                continue
            application.url_file_in_storage = url
            application.save()
        except Exception:
            logger.exception(msg=GENERAL_FAILURE.format(pk=application.pk))


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20220720_1135'),
    ]

    operations = [
        migrations.RunPython(fix_links, reverse_code=migrations.RunPython.noop),
    ]
