import os

import yadisk


def yandex_disk_export(yndx, instance):
    cwd = os.getcwd()
    name = str(instance.file).split("/")[-1]
    name = name.replace("\\", "_").replace("/", "_")
    try:
        yndx.mkdir(f"/{str(instance.year)}")
    except yadisk.exceptions.PathExistsError:
        pass
    to_dir = f"/{str(instance.year)}/{name}"
    from_dir = cwd.replace("\\", "/") + "/media/" + str(instance.file)
    try:
        yndx.upload(from_dir, to_dir)
    except yadisk.exceptions.PathExistsError:
        pass
    if yndx.exists(to_dir):
        download_link = yndx.get_download_link(to_dir)
        instance.file.delete()
        instance.url_file_in_storage = download_link
        instance.saved_to_storage = True
        instance.save()
