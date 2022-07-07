import logging
from typing import Any, Optional

from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db.models import IntegerField
from django.db.models.functions import Cast

from apps.afisha.models.performance import Performance
from apps.articles.models import BlogItem, NewsItem, Project
from apps.core.management.commands.filldb import FillDbLogsMixin

logging.getLogger("django").setLevel(logging.WARNING)


def load_using_model_name(Model):
    contentType = ContentType.objects.get_for_model(Model)
    model_logs = (
        LogEntry.objects.annotate(object_id_as_int=Cast("object_id", IntegerField()))
        .filter(object_id_as_int__in=Model.objects.values_list("id"))
        .filter(content_type=contentType)
        .filter(action_flag=ADDITION)
        .values("object_id_as_int", "user_id")
    )
    for log in model_logs:
        model = Model.objects.filter(id=log["object_id_as_int"])
        model.update(creator=log["user_id"])


class Command(FillDbLogsMixin, BaseCommand):
    def log_success_update(command, verbose_name):
        text = f"Успешно обновлено поле создателя для модели {verbose_name}"
        command.stdout.write(command.style.SUCCESS(text))

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self.log_info("Начинаю обновление полей создателя..")

            load_using_model_name(Project)
            self.log_success_update("Проект")

            load_using_model_name(BlogItem)
            self.log_success_update("Блог")

            load_using_model_name(NewsItem)
            self.log_success_update("Новость")

            load_using_model_name(Performance)
            self.log_success_update("Спектакль")

            self.log_info("Обновление данных окончено!")

        except CommandError as err:
            self.log_error(f"Ошибка обновления базы данных:\n{err}")
