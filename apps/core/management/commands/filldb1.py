from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.articles.tests.blog_factory import BlogFactory
from apps.content_pages.tests.factories import ImageForContentFactory
from apps.library.tests.factories import PlayFactory, ProgramFactory


def notification(command, objects, text):
    command.stdout.write(
        command.style.SUCCESS(f"{len(objects)} {text} успешно созданы.")
    )


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            images = ImageForContentFactory.create_batch(5)
            notification(self, images, "картинок")
            programms = ProgramFactory.create_batch(3)
            notification(self, programms, "программ")
            plays = PlayFactory.create_batch(5)
            notification(self, plays, "пьес")
            blogs = []
            blog_items = BlogFactory.complex_create(5)
            blogs.extend(blog_items)
            notification(self, blogs, "блогов")
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
