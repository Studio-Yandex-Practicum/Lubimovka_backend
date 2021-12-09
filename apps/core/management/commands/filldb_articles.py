from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.articles.tests.blog_factory import BlogFactory
from apps.articles.tests.news_factory import NewsFactory
from apps.articles.tests.project_factory import ProjectFactory


def notification(command, objects, text):
    command.stdout.write(
        command.style.SUCCESS(f"{len(objects)} {text} успешно созданы.")
    )


class Command(BaseCommand):
    help = (
        "Заполняет базу данных тестовыми данными и сейчас доступны:"
        " - Блоги"
        " - Новости"
        " - Проекты"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            blogs = []
            blog_items = BlogFactory.complex_create(5)
            blogs.extend(blog_items)
            notification(self, blogs, "блогов")
            news = []
            news_items = NewsFactory.complex_create(5)
            news.extend(news_items)
            notification(self, news, "новостей")
            projects = []
            projects_item = ProjectFactory.complex_create(5)
            projects.extend(projects_item)
            notification(self, projects, "проектов")
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
