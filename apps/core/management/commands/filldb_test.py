from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.core.tests.factories import ImageFactory, PersonFactory
from apps.info.tests.factories import FestivalFactory
from apps.library.tests.factories import PlayFactory, ProgramFactory


def notification(command, objects, text):
    command.stdout.write(command.style.SUCCESS(f"{len(objects)} {text} успешно создано."))


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными."

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            persons_base = PersonFactory.create_batch(10)
            notification(self, persons_base, "базовых персон")

            persons_with_image = PersonFactory.create_batch(10, add_real_image=True)
            notification(self, persons_with_image, "персоны с фото")

            persons_with_image_email_city = PersonFactory.create_batch(
                10,
                add_real_image=True,
                add_email=True,
                add_city=True,
            )
            notification(self, persons_with_image_email_city, "персон с фото, городом, email")

            images = ImageFactory.create_batch(5)
            notification(self, images, "картинки")

            festivals = FestivalFactory.create_batch(10)
            notification(self, festivals, "фестивалей")

            programtypes = ProgramFactory.create_batch(3)
            notification(self, programtypes, "программ")

            plays = PlayFactory.create_batch(10)
            notification(self, plays, "пьес")

        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
