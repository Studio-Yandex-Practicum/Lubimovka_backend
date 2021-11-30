from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.main"
    verbose_name = "Настройки главной страницы"
