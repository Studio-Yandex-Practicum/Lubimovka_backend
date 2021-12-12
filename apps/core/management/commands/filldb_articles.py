from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.articles.tests.factories.blog_factory import BlogFactory
from apps.articles.tests.factories.news_factory import NewsFactory
from apps.articles.tests.factories.project_factory import ProjectFactory


def notification(command, objects, text):
    command.stdout.write(command.style.SUCCESS(f"{len(objects)} {text} успешно созданы."))


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными и сейчас доступны:" " - Блоги" " - Новости" " - Проекты"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            blog_items = BlogFactory.complex_create(5)
            notification(self, blog_items, "блогов")
            news_items = NewsFactory.complex_create(5)
            notification(self, news_items, "новостей")
            projects_item = ProjectFactory.complex_create(5)
            notification(self, projects_item, "проектов")
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
