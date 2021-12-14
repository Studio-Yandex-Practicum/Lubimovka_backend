from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.content_pages.tests.factories import ImageForContentFactory
from apps.core.tests.factories import ImageFactory, PersonFactory, UserFactory
from apps.info.tests.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    PartnerFactory,
    PressReleaseFactory,
    SponsorFactory,
    VolunteerFactory,
)


def notification(command, objects, text):
    command.stdout.write(command.style.SUCCESS(f"{len(objects)} {text} успешно созданы."))


class Command(BaseCommand):
    help = (
        "Заполняет базу данных тестовыми данными и сейчас доступны:"
        " - Персоны"
        " - Персоны с фотографией"
        " - Персоны с фотографией, городом проживания и email"
        " - Партнёры"
        " - Партнёры для футера"
        " - Попечители"
        " - Волонтёры"
        " - Команды фестиваля"
        " - Картинки"
        " - Фестивали"
        " - Пресс-релизы"
        " - Изображения для новостей/блогов/проектов"
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
            notification(self, persons_base, "базовых персон")
            notification(self, persons_with_image, "персоны с фото")
            notification(
                self,
                persons_with_image_email_city,
                "персон с фото, городом, email",
            )
            partners = PartnerFactory.create_batch(30)
            notification(self, partners, "партнёров")

            in_footer_partners = PartnerFactory.create_batch(
                5,
                type="general",
                in_footer_partner=True,
            )
            notification(self, in_footer_partners, "партнёров в футере")

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

            press_releases = PressReleaseFactory.create_batch(10)
            notification(self, press_releases, "пресс-релизов")

            images_for_content = ImageForContentFactory.create_batch(10)
            notification(self, images_for_content, "контент-изображений")

            users_editors = []
            users_admins = []
            for index in range(1, 6):
                users_editors.append(UserFactory.create(username=f"editor_{index}", add_role_editor=True))
                users_admins.append(UserFactory.create(username=f"admin_{index}", add_role_admin=True))
            notification(self, users_editors, "редакторов")
            notification(self, users_admins, "админов")
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
