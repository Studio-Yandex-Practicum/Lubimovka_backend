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
from apps.info.utils import get_random_objects_by_queryset
from apps.library.factories import AuthorFactory, OtherPlayFactory, PlayFactory, ProgramTypeFactory
from apps.library.factories.constants import YOUTUBE_VIDEO_LINKS
from apps.library.models import Play
from apps.main.factories import BannerFactory as MainBannerFactory
from apps.users.factories import (
    AdminUserFactory,
    EditorUserFactory,
    JournalistUserFactory,
    ObserverUserFactory,
    SuperUserFactory,
)

logging.getLogger("django").setLevel(logging.WARNING)


class FillDbLogsMixin:
    def log_info(command, text):
        command.stdout.write()
        command.stdout.write(command.style.SUCCESS(text))
        command.stdout.write()

    def log_success_creation(command, obj, obj_verbose_name):
        number = 1
        if isinstance(obj, list):
            number = len(obj)
        text = f"  Успешно создано: {number} {obj_verbose_name}"
        command.stdout.write(command.style.SUCCESS(text))

    def log_error(command, text):
        command.stdout.write(command.style.ERROR(text))


class Command(FillDbLogsMixin, BaseCommand):
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
            self.log_info("Создаю тестовых пользователей...")

            superuser = SuperUserFactory.create()
            self.log_success_creation(superuser, "суперюзер")

            users_admins = AdminUserFactory.create_batch(2)
            self.log_success_creation(users_admins, "админов")

            users_editors = EditorUserFactory.create_batch(2)
            self.log_success_creation(users_editors, "редакторов")

            users_journalists = JournalistUserFactory.create_batch(2)
            self.log_success_creation(users_journalists, "журналистов")

            users_observers = ObserverUserFactory.create_batch(2)
            self.log_success_creation(users_observers, "наблюдателя")

            # Core factories
            self.log_info("Создаю общие ресурсы приложений...")

            persons_base = PersonFactory.create_batch(15)
            self.log_success_creation(persons_base, "базовых персон")

            persons_with_image = PersonFactory.create_batch(15, add_real_image=True)
            self.log_success_creation(persons_with_image, "персон с фото")

            persons_with_image_email_city = PersonFactory.create_batch(
                15,
                add_real_image=True,
                add_email=True,
                add_city=True,
            )
            self.log_success_creation(persons_with_image_email_city, "персон с фото, городом, email")

            # Info factories
            self.log_info("Создаю информацию на сайт...")

            festivals = FestivalFactory.create_batch(15)
            self.log_success_creation(festivals, "фестивалей")

            press_releases = PressReleaseFactory.create_batch(10)
            self.log_success_creation(press_releases, "пресс-релизов")

            volunteers = VolunteerFactory.create_batch(50)
            self.log_success_creation(volunteers, "волонтёров")

            teams = FestivalTeamFactory.create_batch(10)
            self.log_success_creation(teams, "членов команд")

            pr_director_creation_result, member = self.add_pr_director()
            if pr_director_creation_result is False:
                if member is None:
                    self.log_error("PR директор уже существует")
                else:
                    self.log_error("Отсутствуют члены команды для создания PR директор")
            else:
                self.log_success_creation(member, "PR директор")

            sponsors = SponsorFactory.create_batch(10)
            self.log_success_creation(sponsors, "попечителей")

            partners = PartnerFactory.create_batch(30)
            self.log_success_creation(partners, "партнёров")

            in_footer_partners = PartnerFactory.create_batch(
                5,
                add_real_image=True,
                type="general",
                in_footer_partner=True,
            )
            self.log_success_creation(in_footer_partners, "генеральных партнёров")

            selectors = SelectorFactory.create_batch(30)
            self.log_success_creation(selectors, "отборщиков")

            places = PlaceFactory.create_batch(3)
            self.log_success_creation(places, "площадки")

            # Library factories
            self.log_info("Создаю данные для Библиотеки...")

            programtypes = ProgramTypeFactory.create_batch(3)
            self.log_success_creation(programtypes, "программы")

            authors = AuthorFactory.complex_create(25)
            self.log_success_creation(authors, "авторов")

            # count of plays depends on 'free' youtube video links, it could be from 50 (at first filldb call) to 0
            plays = self.create_plays()
            self.log_success_creation(plays, "пьес")

            other_plays = OtherPlayFactory.create_batch(5)
            self.log_success_creation(other_plays, "других пьес")

            # Afisha factories
            self.log_info("Создаю данные для Афиши...")

            perfomances = PerformanceFactory.complex_create(10)
            self.log_success_creation(perfomances, "спектаклей")

            masterclasses = MasterClassFactory.create_batch(10)
            self.log_success_creation(masterclasses, "мастер-классов")

            readings = ReadingFactory.create_batch(10)
            self.log_success_creation(readings, "читок")

            events_of_performances = EventFactory.create_batch(5, performance=True)
            self.log_success_creation(events_of_performances, "событий спектакля")

            events = EventFactory.create_batch(10)
            self.log_success_creation(events, "событий")

            # Other factories
            self.log_info("Создаю баннеры и заявки на участие...")

            participations = ParticipationApplicationFestivalFactory.create_batch(5)
            self.log_success_creation(participations, "заявок на участие в фестивале")

            main_banners = MainBannerFactory.create_batch(3, add_real_image=True)
            self.log_success_creation(main_banners, "баннера на главную страницу (с картинкой)")

            self.log_info("Создание тестовых данных завершено!")

        except CommandError as err:
            self.log_error(f"Ошибка наполнения базы данных:\n{err}")

    def create_plays(command):
        def _get_video_links():
            used_links = Play.objects.filter(other_play=False).values_list("url_reading", flat=True)
            return (link for link in YOUTUBE_VIDEO_LINKS if link not in used_links)

        links = _get_video_links()
        for link in links:
            url_reading = random.choice([None, link])
            PlayFactory.create(url_reading=url_reading)
        return links  # needs for notification, because count of Plays is equal to links

    def add_pr_director(command):
        festival_team_members = FestivalTeamMember.objects.filter(team="fest")
        if festival_team_members.filter(is_pr_director=True).exists():
            return False, None
        member = get_random_objects_by_queryset(festival_team_members)
        if member:
            name = member.person.full_name
            member.is_pr_director = True
            member.save()
            Setting.objects.filter(settings_key="pr_director_name").update(text=name)
            return True, member
        return False, member
