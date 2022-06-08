import logging
import random
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.afisha.factories import MasterClassFactory, PerformanceFactory, ReadingFactory
from apps.afisha.factories.events import EventFactory
from apps.core.factories import PersonFactory
from apps.core.models import Setting
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
from apps.info.models import FestivalTeamMember
from apps.library.factories import AuthorFactory, OtherPlayFactory, PlayFactory, ProgramTypeFactory
from apps.library.utilities import get_video_links
from apps.main.factories import BannerFactory as MainBannerFactory
from apps.users.factories import (
    AdminUserFactory,
    EditorUserFactory,
    JournalistUserFactory,
    ObserverUserFactory,
    SuperUserFactory,
)

logger = logging.getLogger()
logger.disabled = True


def create_plays(command):
    links = get_video_links()
    for link in links:
        url_reading = random.choice([None, link])
        PlayFactory.create(url_reading=url_reading)
    return links  # needs for notification, because count of Plays is equal to links


def add_pr_director(command):
    member = FestivalTeamMember.objects.filter(team="fest").first()
    if member:
        name = member.person.full_name
        member.is_pr_director = True
        member.save()
        Setting.objects.filter(settings_key="pr_director_name").update(text=name)
        command.stdout.write(command.style.SUCCESS("ПР директор успешно создан"))
    else:
        command.stdout.write(command.style.ERROR("Нет члена команды Фестиваль"))


def notification(command, objects, text):
    if len(objects) > 1:
        command.stdout.write(command.style.SUCCESS(f"{len(objects)} {text} успешно создано."))
    else:
        command.stdout.write(command.style.SUCCESS(f"{len(objects)} {text} успешно создан."))


def process_message(command, text):
    command.stdout.write()
    command.stdout.write(command.style.SUCCESS(text))
    command.stdout.write()


class Command(BaseCommand):
    help = (
        "Заполняет БД тестовыми данными. Сейчас доступны:"
        " - Пользователь-суперадмин"
        " - Пользователи-админы"
        " - Пользователи-редакторы"
        " - Пользователи-журналисты"
        " - Пользователи-наблюдатели"
        " - Персоны"
        " - Персоны с фотографией"
        " - Персоны с фотографией, городом проживания и email"
        " - Фестивали"
        " - Пресс-релизы"
        " - Волонтёры"
        " - Команда фестиваля"
        " - PR директор"
        " - Попечители"
        " - Партнёры"
        " - Генеральные партнёры"
        " - Отборщики"
        " - Площадки"
        " - Программы"
        " - Авторы"
        " - Пьесы"
        " - Другие пьесы"
        " - Спектакли"
        " - Мастер-классы"
        " - Читки"
        " - События со спектаклем"
        " - События"
        " - Заявки на участие"
        " - Баннеры главной страницы"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            # users creation
            process_message(self, "Создаю тестовых пользователей...")

            SuperUserFactory.create()
            self.stdout.write(self.style.SUCCESS("Суперадмин успешно создан."))

            users_admins = AdminUserFactory.create_batch(5)
            notification(self, users_admins, "админов")

            users_editors = EditorUserFactory.create_batch(5)
            notification(self, users_editors, "редакторов")

            users_journalists = JournalistUserFactory.create_batch(5)
            notification(self, users_journalists, "журналистов")

            users_observers = ObserverUserFactory.create_batch(2)
            notification(self, users_observers, "наблюдателя")

            # Core factories
            process_message(self, "Создаю общие ресурсы приложений...")

            persons_base = PersonFactory.create_batch(30)
            notification(self, persons_base, "базовых персон")

            persons_with_image = PersonFactory.create_batch(30, add_real_image=True)
            notification(self, persons_with_image, "персон с фото")

            persons_with_image_email_city = PersonFactory.create_batch(
                30,
                add_real_image=True,
                add_email=True,
                add_city=True,
            )
            notification(self, persons_with_image_email_city, "персон с фото, городом, email")

            # Info factories
            process_message(self, "Создаю информацию на сайт...")

            festivals = FestivalFactory.create_batch(20)
            notification(self, festivals, "фестивалей")

            press_releases = PressReleaseFactory.create_batch(10)
            notification(self, press_releases, "пресс-релизов")

            volunteers = VolunteerFactory.create_batch(50)
            notification(self, volunteers, "волонтёров")

            teams = FestivalTeamFactory.create_batch(10)
            notification(self, teams, "членов команд")

            add_pr_director(self)

            sponsors = SponsorFactory.create_batch(10)
            notification(self, sponsors, "попечителей")

            partners = PartnerFactory.create_batch(30)
            notification(self, partners, "партнёров")

            in_footer_partners = PartnerFactory.create_batch(
                5,
                add_real_image=True,
                type="general",
                in_footer_partner=True,
            )
            notification(self, in_footer_partners, "генеральных партнёров")

            selectors = SelectorFactory.create_batch(30)
            notification(self, selectors, "отборщиков")

            places = PlaceFactory.create_batch(3)
            notification(self, places, "площадки")

            # Library factories
            process_message(self, "Создаю данные для Библиотеки...")

            programtypes = ProgramTypeFactory.create_batch(3)
            notification(self, programtypes, "программы")

            authors = AuthorFactory.complex_create(15)
            notification(self, authors, "авторов")

            # count of plays depends on 'free' youtube video links, it could be from 50 (at first filldb call) to 0
            plays = create_plays(self)
            notification(self, plays, "пьес")

            other_plays = OtherPlayFactory.create_batch(5)
            notification(self, other_plays, "других пьес")

            # Afisha factories
            process_message(self, "Создаю данные для Афиши...")

            perfomances = PerformanceFactory.complex_create(6)
            notification(self, perfomances, "спектаклей")

            masterclasses = MasterClassFactory.create_batch(10)
            notification(self, masterclasses, "мастер-классов")

            readings = ReadingFactory.create_batch(10)
            notification(self, readings, "читок")

            events_of_performances = EventFactory.create_batch(5, performance=True)
            notification(self, events_of_performances, "событий спектакля")

            events = EventFactory.create_batch(10)
            notification(self, events, "событий")

            # Other factories
            process_message(self, "Создаю баннеры и заявки на участие...")

            participations = ParticipationApplicationFestivalFactory.create_batch(5)
            notification(self, participations, "заявок на участие в фестивале")

            main_banners = MainBannerFactory.create_batch(3, add_real_image=True)
            notification(self, main_banners, "баннера на главную страницу (с картинкой)")

            process_message(self, "Создание тестовых данных завершено!")

        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполнения БД"))


logger.disabled = False
