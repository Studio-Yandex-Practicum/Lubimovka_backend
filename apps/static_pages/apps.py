from django.apps import AppConfig


class StaticPagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.static_pages"
    verbose_name = 'Страницы: "Что мы делаем", "Идеология", "История".'
