from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.afisha.factories import EventFactory
from apps.core.factories import ImageFactory, PersonFactory
from apps.feedback.factories import ParticipationApplicationFestivalFactory
from apps.info.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    PartnerFactory,
    PlaceFactory,
    PressReleaseFactory,
    SelectorFactory,
    SponsorFactory,
    VolunteerFactory,
)
from apps.library.factories import (
    AuthorFactory,
    MasterClassFactory,
    OtherPlayFactory,
    PerformanceFactory,
    PlayFactory,
    ProgramTypeFactory,
    ReadingFactory,
)
from apps.main.factories import BannerFactory as MainBannerFactory
from apps.users.factories import AdminUserFactory, EditorUserFactory, JournalistUserFactory, ObserverUserFactory


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
        " - Пользователи-журналисты"
        " - Пользователи-наблюдатели"
        " - Программы"
        " - Авторы"
        " - Пьесы"
        " - Другие пьесы"
        " - Спектакли"
        " - Мастер-классы"
        " - Читки"
        " - Баннеры главной страницы"
        " - Места"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            persons_base = PersonFactory.create_batch(30)
            notification(self, persons_base, "базовых персон")

            persons_with_image = PersonFactory.create_batch(30, add_real_image=True)
            notification(self, persons_with_image, "персоны с фото")

            persons_with_image_email_city = PersonFactory.create_batch(
                30,
                add_real_image=True,
                add_email=True,
                add_city=True,
            )
            notification(self, persons_with_image_email_city, "персон с фото, городом, email")

            partners = PartnerFactory.create_batch(30)
            notification(self, partners, "партнёров")

            in_footer_partners = PartnerFactory.create_batch(
                5,
                add_real_image=True,
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

            selectors = SelectorFactory.create_batch(30)
            notification(self, selectors, "отборщиков")

            press_releases = PressReleaseFactory.create_batch(10)
            notification(self, press_releases, "пресс-релизов")

            users_admins = AdminUserFactory.create_batch(5)
            notification(self, users_admins, "админов")

            users_editors = EditorUserFactory.create_batch(5)
            notification(self, users_editors, "редакторов")

            users_journalists = JournalistUserFactory.create_batch(5)
            notification(self, users_journalists, "журналистов")

            users_observers = ObserverUserFactory.create_batch(2)
            notification(self, users_observers, "наблюдателя")

            # Library factories.

            programtypes = ProgramTypeFactory.create_batch(3)
            notification(self, programtypes, "программ")

            plays = PlayFactory.create_batch(10)
            notification(self, plays, "пьес")

            other_plays = OtherPlayFactory.create_batch(10)
            notification(self, other_plays, "других пьес")

            perfomances = PerformanceFactory.complex_create(6)
            notification(self, perfomances, "спектаклей")

            authors = AuthorFactory.complex_create(15)
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

            events_of_performances = EventFactory.create_batch(5, performance=True)
            notification(self, events_of_performances, "событий спектакля")

            events = EventFactory.create_batch(10)
            notification(self, events, "событий")

        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))
