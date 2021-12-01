from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.articles.tests.factories import BlogFactory


def notification(command, objects, text):
    command.stdout.write(
        command.style.SUCCESS(f"{len(objects)} {text} успешно созданы.")
    )


class Command(BaseCommand):
    help = (
        "Заполняет базу данных тестовыми данными и сейчас доступны:" " - Блог"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            blogs = BlogFactory.create_batch(5)
            notification(self, blogs, "блогов")
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполения БД"))
