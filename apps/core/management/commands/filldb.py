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
from apps.library.tests.factories import (
    AuthorFactory,
    MasterClassFactory,
    ParticipationApplicationFestivalFactory,
    PerformanceFactory,
    ProgramFactory,
    ReadingFactory,
)


def notification(command, objects, text):
    command.stdout.write(
        command.style.SUCCESS(f"{len(objects)} {text} успешно создано.")
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
        " - Программы"
        " - Авторы"
        " - Ссылки на сторонние ресурсы"
        " - Пьесы"
        " - Достижения"
        " - Ссылки на социальные сети"
        " - Другие пьесы"
        " - Спектакли"
        " - Отзывы на спектакли"
        " - Медиа отзывы на спектакли"
        " - Мастер-классы"
        " - Читки"
        " - Члены команды читок, спектаклей и мастер-классов"
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

            programtypes = ProgramFactory.create_batch(3)
            notification(self, programtypes, "программ")

            users_editors = []
            users_admins = []
            authors = []
            perfomances = []
            for index in range(1, 6):
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
                authors.append(AuthorFactory.complex_create())
                perfomances.append(PerformanceFactory.complex_create())

            notification(self, users_editors, "редакторов")
            notification(self, users_admins, "админов")
            notification(
                self,
                authors,
                "{}, {}, {}, {}, {}, {}".format(
                    "авторов",
                    "пьес",
                    "достижений",
                    "ссылок на социальные сети",
                    "ссылок на сторонние ресурсы",
                    "других пьес",
                ),
            )
            notification(
                self, perfomances, "спектаклей, отзывов и медиа отзывов"
            )

            masterclasses = MasterClassFactory.create_batch(10)
            notification(self, masterclasses, "мастер-классов")

            readings = ReadingFactory.create_batch(10)
            notification(self, readings, "читок")

            participations = (
                ParticipationApplicationFestivalFactory.create_batch(5)
            )
            notification(self, participations, "заявок на участие в фестивале")

        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполения БД"))
