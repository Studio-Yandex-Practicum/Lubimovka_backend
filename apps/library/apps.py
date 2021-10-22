from django.apps import AppConfig
from django.db.models.signals import m2m_changed

from .signals import images_in_block_changed


class LibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.library"
    verbose_name = "Библиотека"

    def ready(self):
        print("here")
        from .models import Performance

        m2m_changed.connect(
            images_in_block_changed,
            sender=Performance.images_in_block.through,
            dispatch_uid="my_unique_identifier",
        )
