from datetime import datetime

import pytest
from django.urls import reverse

from apps.afisha.factories import EventFactory, PerformanceFactory, ReadingFactory
from apps.articles.factories import BlogItemFactory, NewsItemFactory
from apps.content_pages.factories import ImagesBlockFactory
from apps.core.constants import Status
from apps.core.factories import PersonFactory
from apps.info.factories import FestivalFactory, InfoLinkFactory, PlaceFactory
from apps.library.factories import AuthorFactory, PlayFactory, ProgramTypeFactory
from apps.library.models import ProgramType
from apps.main.factories import BannerFactory

MAIN_URL = reverse("main:main_page")


@pytest.fixture(autouse=True)
def set_media_temp_folder(settings, tmp_path_factory):
    settings.MEDIA_ROOT = tmp_path_factory.mktemp("media")
    settings.HIDDEN_MEDIA_ROOT = tmp_path_factory.mktemp("hidden")
    (settings.HIDDEN_MEDIA_ROOT / "plays").mkdir()


@pytest.fixture
def festival():
    start_date = datetime(2021, 7, 14)
    end_date = datetime(2021, 7, 15)
    return FestivalFactory(start_date=start_date, end_date=end_date, year=2021)


@pytest.fixture
def links(festival):
    return InfoLinkFactory.create_batch(10)


@pytest.fixture
def program_types():
    return ProgramTypeFactory.create_batch(5)


@pytest.fixture
def persons_email_city_image():
    return PersonFactory.create_batch(10, add_city=True, add_email=True, add_image=True)


@pytest.fixture
def authors(persons_email_city_image, festival, program_types):
    return AuthorFactory.complex_create(5)


@pytest.fixture
def play(authors, festival):
    return PlayFactory(published=True)


@pytest.fixture
def play_in_short_list(authors, festival):
    short_list_program_type = ProgramType.objects.get(slug="short-list")
    return PlayFactory(published=True, programs=[short_list_program_type])


@pytest.fixture
def plays(authors, festival):
    return PlayFactory.create_batch(10, year=festival.year)


@pytest.fixture
def persons():
    PersonFactory.create_batch(6)


@pytest.fixture
def images_block(persons):
    return ImagesBlockFactory(add_image=True)


@pytest.fixture
def banners():
    return BannerFactory.create_batch(3)


@pytest.fixture
def places():
    return PlaceFactory.create_batch(3)


@pytest.fixture
def reading(plays, persons):
    return ReadingFactory()


@pytest.fixture
def performance(plays, persons):
    return PerformanceFactory.create_batch(5, status=Status.PUBLISHED)


@pytest.fixture
def four_performances(plays, persons):
    return PerformanceFactory.complex_create(4)


@pytest.fixture
def four_performance_events(four_performances):
    return EventFactory.create_batch(4)


@pytest.fixture
def events_hidden_on_main(freezer, reading, performance):
    freezer.move_to("2021-05-20 15:42")
    return EventFactory.create_batch(4, date_time_in_three_hours=True, hidden_on_main=False)


@pytest.fixture
def news_items_with_content(plays, images_block, four_performance_events):
    return NewsItemFactory.complex_create(3, status=Status.PUBLISHED)


@pytest.fixture
def blog_items_with_content(plays, images_block, four_performance_events):
    return BlogItemFactory.complex_create(3, status=Status.PUBLISHED)
