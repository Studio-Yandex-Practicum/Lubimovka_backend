import logging
from pathlib import Path
from typing import Optional

import yadisk
from django.conf import settings
from yadisk.exceptions import YaDiskError

logger = logging.getLogger("django")


def publish_file(yndx, path):
    if yndx.exists(path):
        yndx.publish(path)
        return yndx.get_meta(path, fields=["public_url"]).public_url


def yandex_disk_export(instance) -> Optional[bool]:
    try:
        yndx = yadisk.YaDisk(token=settings.YNDX_DISK_TOKEN)
        _, year, name = Path(str(instance.file)).parts
        to_dir = f"{year}/{name}"
        from_dir = (settings.MEDIA_ROOT / instance.file.name).as_posix()

        if not yndx.is_dir(year):
            yndx.mkdir(year)
        yndx.upload(from_dir, to_dir)

        return publish_file(yndx, to_dir)
    except (ValueError, YaDiskError):
        msg = f"Не удалось загрузить пьесу {instance.title} от {instance.email} на Яндекс диск."
        logger.critical(msg, exc_info=True)
