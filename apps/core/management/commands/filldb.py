from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.core.tests.factories import ImageFactory, PersonFactory, UserFactory
from apps.info.tests.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    PartnerFactory,
    SponsorFactory,
    VolunteerFactory,
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
        " - Пользователи-админы"
        " - Пользователи-редакторы"
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
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(persons_base)} базовых персон созданы успешно."
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(persons_with_image)} персон с фото созданы успешно."
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(persons_with_image_email_city)} персон с фото, "
                    f"городом, email созданы успешно."
                )
            )
            partners = PartnerFactory.create_batch(30)
            sponsors = SponsorFactory.create_batch(50)
            volunteers = VolunteerFactory.create_batch(50)
            teams = FestivalTeamFactory.create_batch(70)
            images = ImageFactory.create_batch(5)
            festivals = FestivalFactory.create_batch(10)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(partners)} партнёров успешно созданы"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(sponsors)} попечителей успешно созданы"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(volunteers)} волонтёров успешно созданы"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(teams)} членов команд успешно созданы"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(festivals)} фестивалей успешно созданы"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f"{len(images)} картинки успешно созданы")
            )
            users_editors = []
            users_admins = []
            index = 1
            for _ in range(5):
                users_editors.append(
                    UserFactory.create(
                        username=f"editor_{index}", add_role_editor=True
                    )
                )
                users_admins.append(
                    UserFactory.create(
                        username=f"admin_{index}", add_role_admin=True
                    )
                )
                index += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(users_editors)} редакторов созданы успешно."
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(users_admins)} админов созданы успешно."
                )
            )
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполения БД"))
