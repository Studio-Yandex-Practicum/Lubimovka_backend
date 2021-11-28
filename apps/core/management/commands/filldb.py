from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.core.tests.factories import ImageFactory, PersonFactory
from apps.info.tests.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    PartnerFactory,
    SponsorFactory,
    VolunteerFactory,
)


def notification(command, objects, text):
    command.stdout.write(
        command.style.SUCCESS(f"{len(objects)} {text} успешно созданы.")
    )


class Command(BaseCommand):
    help = (
        "Заполняет базу данных тестовыми данными и сейчас доступны:"
        " - Персоны"
        " - Персоны с фотографией"
        " - Персоны с фотографией, городом проживания и email"
        " - Партнёры"
        " - Волонтёры"
        " - Попечители"
        " - Команды фестиваля"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            persons_base = PersonFactory.create_batch(30)
            persons_with_image = []
            persons_with_image_email_city = []
            for _ in range(50):
                persons_with_image.append(PersonFactory.create(add_image=True))
                persons_with_image_email_city.append(
                    PersonFactory(
                        add_image=True,
                        add_email=True,
                        add_city=True,
                    )
                )
            notification(self, persons_base, "базовых персон")
            notification(self, persons_with_image, "персоны с фото")
            notification(
                self,
                persons_with_image_email_city,
                "персон с фото, городом, email",
            )
            partners = PartnerFactory.create_batch(30)
            notification(self, partners, "партнёров")

            sponsors = SponsorFactory.create_batch(50)
            notification(self, sponsors, "попечителей")

            volunteers = VolunteerFactory.create_batch(50)
            notification(self, volunteers, "волонтёров")

            teams = FestivalTeamFactory.create_batch(70)
            notification(self, teams, "членов команд")

            images = ImageFactory.create_batch(5)
            notification(self, images, "картинки")

            festivals = FestivalFactory.create_batch(10)
            notification(self, festivals, "фестивалей")

        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполения БД"))
