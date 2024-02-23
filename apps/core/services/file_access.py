"""Сервис контроля доступа к файлам для приложени django-private-storage."""
from pathlib import Path

from django.conf import settings
from private_storage.models import PrivateFile

from apps.library.models.play import Play


def has_download_permission(private_file: PrivateFile) -> bool:
    user = private_file.request.user
    if user.is_authenticated and user.is_staff:
        return True

    relative_path = Path(private_file.full_path).relative_to(settings.PRIVATE_STORAGE_ROOT)
    return Play.objects.filter(url_download=relative_path, published=True).exists()
