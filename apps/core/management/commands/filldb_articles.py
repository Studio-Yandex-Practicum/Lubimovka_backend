import logging
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.articles.factories import BlogItemFactory, NewsItemFactory, ProjectFactory
from apps.core.management.commands.filldb import log_error, log_info, log_success

logging.getLogger("django").setLevel(logging.WARNING)


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными и сейчас доступны: Блоги, Новости, Проекты"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            log_info(self, "Создаю данные для новостей, проектов, блогов...")

            blog_items = BlogItemFactory.complex_create(5)
            log_success(self, blog_items, "блогов")

            news_items = NewsItemFactory.complex_create(5)
            log_success(self, news_items, "новостей")

            projects_item = ProjectFactory.complex_create(5)
            log_success(self, projects_item, "проектов")

            log_info(self, "Создание тестовых данных завершено!")
        except CommandError:
            log_error(self, "Ошибка наполнения базы данных")
