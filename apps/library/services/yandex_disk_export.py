from pathlib import Path

import yadisk
from django.conf import settings


def yandex_disk_export(instance):
    yndx = yadisk.YaDisk(token=settings.YNDX_DISK_TOKEN)
    cwd = str(settings.ROOT_DIR)
    name = Path(str(instance.file)).name
    year = str(Path(str(instance.file)).parent).split("\\")[-1]
    to_dir = f"{year}/{name}"
    from_dir = cwd.replace("\\", "/") + "/media/" + str(instance.file)
    try:
        yndx.mkdir(f"/{year}")
    except yadisk.exceptions.PathExistsError:
        pass
    yndx.upload(from_dir, to_dir)
    if yndx.exists(to_dir):
        download_link = yndx.get_download_link(to_dir)
        instance.file.delete()
        instance.url_file_in_storage = download_link
        instance.saved_to_storage = True
        instance.save()
