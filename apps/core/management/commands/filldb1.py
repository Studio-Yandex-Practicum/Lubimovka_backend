from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.articles.tests.factories import BlogFactory
from apps.content_pages.tests.factories import ImageForContentFactory
from apps.library.tests.factories import PlayFactory, ProgramFactory


def notification(command, objects, text):
    command.stdout.write(
        command.style.SUCCESS(f"{len(objects)} {text} успешно созданы.")
    )


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            images_content = ImageForContentFactory.create_batch(5)
            notification(self, images_content, "изображений для контента")
            programs = ProgramFactory.create_batch(3)
            notification(self, programs, "программ")
            plays = PlayFactory.create_batch(10)
            notification(self, plays, "пьес")
            blogs = []
            for _ in range(2):
                blogs.append(BlogFactory.complex_create())
            notification(self, blogs, "блогов")
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
