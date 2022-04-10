from pathlib import Path
from typing import Optional

import yadisk
from django.conf import settings


def yandex_disk_export(instance) -> Optional[bool]:
    yndx = yadisk.YaDisk(token=settings.YNDX_DISK_TOKEN)
    _, year, name = Path(str(instance.file)).parts
    to_dir = f"{year}/{name}"
    from_dir = Path(settings.MEDIA_ROOT / instance.file.name).as_posix()

    if not yndx.is_dir(year):
        yndx.mkdir(year)
    yndx.upload(from_dir, to_dir)

    if yndx.exists(to_dir):
        download_link = yndx.get_download_link(to_dir)
        Path(instance.file.path).unlink()
        return download_link
