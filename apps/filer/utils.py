from pathlib import Path

from django.utils.text import get_valid_filename

from apps.core.utils import slugify


def folder_slug(instance, filename):
    filename_path = Path(filename)
    return Path(
        slugify(instance.logical_folder.name),
        slugify(get_valid_filename(filename_path.stem)) + filename_path.suffix
    )
