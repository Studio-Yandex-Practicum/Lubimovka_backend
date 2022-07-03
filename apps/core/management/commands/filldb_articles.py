import logging
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.articles.factories import BlogItemFactory, NewsItemFactory, ProjectFactory
from apps.core.management.commands.filldb import FillDbLogsMixin

logging.getLogger("django").setLevel(logging.WARNING)


class Command(FillDbLogsMixin, BaseCommand):
    help = "Заполняет базу данных тестовыми данными и сейчас доступны: Блоги, Новости, Проекты"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            self.log_info("Создаю данные для новостей, проектов, блогов...")

            blog_items = BlogItemFactory.complex_create(15)
            self.log_success_creation(blog_items, "блогов")

            news_items = NewsItemFactory.complex_create(15)
            self.log_success_creation(news_items, "новостей")

            projects_item = ProjectFactory.complex_create(5)
            self.log_success_creation(projects_item, "проектов")

            self.log_info("Создание тестовых данных завершено!")

        except CommandError as err:
            self.log_error(f"Ошибка наполнения базы данных:\n{err}")
