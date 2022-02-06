from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.afisha.tests.factories import EventFactory
from apps.content_pages.tests.factories import ImageForContentFactory, VideoFactory
from apps.core.tests.factories import ImageFactory, PersonFactory, UserFactory
from apps.info.tests.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    PartnerFactory,
    PlaceFactory,
    PressReleaseFactory,
    SponsorFactory,
    VolunteerFactory,
)
from apps.library.tests.factories import (
    AuthorFactory,
    MasterClassFactory,
    ParticipationApplicationFestivalFactory,
    PerformanceFactory,
    PlayFactory,
    ProgramFactory,
    ReadingFactory,
)
from apps.main.tests.factories import BannerFactory as MainBannerFactory


def notification(command, objects, text):
    command.stdout.write(command.style.SUCCESS(f"{len(objects)} {text} успешно создано."))


class Command(BaseCommand):
    help = (
        "Заполняет БД тестовыми данными. Сейчас доступны:"
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
        " - Видео (ссылки с описанием)"
        " - Пользователи-админы"
        " - Пользователи-редакторы"
        " - Программы"
        " - Авторы"
        " - Пьесы"
        " - Спектакли"
        " - Мастер-классы"
        " - Читки"
        " - Баннеры главной страницы"
        " - Места"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            persons_base = PersonFactory.create_batch(30)
            persons_with_image = []
            persons_with_image_email_city = []
            for _ in range(50):
                persons_with_image.append(PersonFactory.create(add_real_image=True))
                persons_with_image_email_city.append(
                    PersonFactory(
                        add_real_image=True,
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

            teams = FestivalTeamFactory.create_batch(70)
            notification(self, teams, "членов команд")

            images = ImageFactory.create_batch(5)
            notification(self, images, "картинки")

            festivals = FestivalFactory.create_batch(10)
            notification(self, festivals, "фестивалей")

            volunteers = VolunteerFactory.create_batch(50)
            notification(self, volunteers, "волонтёров")

            press_releases = PressReleaseFactory.create_batch(10)
            notification(self, press_releases, "пресс-релизов")

            images_for_content = ImageForContentFactory.create_batch(10)
            notification(self, images_for_content, "контент-изображений")

            videos_url = VideoFactory.create_batch(5)
            notification(self, videos_url, "видео")

            users_editors = []
            users_admins = []
            for index in range(1, 6):
                users_editors.append(UserFactory.create(username=f"editor_{index}", add_role_editor=True))
                users_admins.append(UserFactory.create(username=f"admin_{index}", add_role_admin=True))
            notification(self, users_editors, "редакторов")
            notification(self, users_admins, "админов")

            # <Library factories>

            programtypes = ProgramFactory.create_batch(3)
            notification(self, programtypes, "программ")

            plays = PlayFactory.create_batch(10)
            notification(self, plays, "пьес")

            perfomances = [PerformanceFactory.complex_create() for _ in range(6)]
            notification(self, perfomances, "спектаклей")

            authors = [AuthorFactory.complex_create() for _ in range(15)]
            notification(self, authors, "авторов")

            masterclasses = MasterClassFactory.create_batch(10)
            notification(self, masterclasses, "мастер-классов")

            readings = ReadingFactory.create_batch(10)
            notification(self, readings, "читок")

            participations = ParticipationApplicationFestivalFactory.create_batch(5)
            notification(self, participations, "заявок на участие в фестивале")

            main_banners = MainBannerFactory.create_batch(3, add_real_image=True)
            notification(self, main_banners, "баннеров на главной страницу (с картинкой)")

            places = PlaceFactory.create_batch(3)
            notification(self, places, "мест")

            events = EventFactory.create_batch(10)
            notification(self, events, "событий")

        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
