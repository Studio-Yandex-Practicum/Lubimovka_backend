import pytest
from django.conf import settings
from django.urls import reverse

from apps.afisha.factories import EventFactory
from apps.articles.factories import BlogItemFactory, NewsItemFactory
from apps.content_pages.factories import ImagesBlockFactory
from apps.core.factories import ImageFactory, PersonFactory
from apps.info.factories import FestivalFactory, PlaceFactory
from apps.library.factories import MasterClassFactory, PerformanceFactory, PlayFactory, ReadingFactory
from apps.library.models.play import ProgramType
from apps.main.factories import BannerFactory

MAIN_URL = reverse("main:main_page")


@pytest.fixture(autouse=True)
def set_media_temp_folder(tmpdir):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")


@pytest.fixture
def images():
    return ImageFactory.create_batch(10)


@pytest.fixture
def festival(images):
    return FestivalFactory(start_date="2021-07-14", end_date="2021-07-15", year="2021")


@pytest.fixture
def play(festival):
    return PlayFactory(is_draft=False)


@pytest.fixture
def play_in_short_list(festival):
    short_list_program_type = ProgramType.objects.get(slug="short-list")
    return PlayFactory(is_draft=False, program=short_list_program_type)


@pytest.fixture
def plays(festival):
    return PlayFactory.create_batch(4, year=festival.year)


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
def news_items_with_content(plays, images_block):
    return NewsItemFactory.create_batch(
        3,
        add_several_preamble=1,
        add_several_text=1,
        add_several_title=1,
        add_several_quote=1,
        add_several_playsblock=1,
        add_several_imagesblock=1,
        add_several_personsblock=1,
        is_draft=False,
    )


@pytest.fixture
def blog_items_with_content():
    return BlogItemFactory.create_batch(
        3,
        add_several_co_author=1,
        add_several_imagesblock=1,
        add_several_personsblock=1,
        add_several_playsblock=1,
        add_several_preamble=1,
        add_several_quote=1,
        add_several_text=1,
        add_several_title=1,
    )


@pytest.fixture
def places():
    return PlaceFactory.create_batch(3)


@pytest.fixture
def master_class(persons):
    return MasterClassFactory()


@pytest.fixture
def reading(plays, persons):
    return ReadingFactory()


@pytest.fixture
def performance(plays, persons):
    return PerformanceFactory()


@pytest.fixture
def events(freezer, reading, performance, master_class):
    freezer.move_to("2021-05-20 15:42")
    return EventFactory.create_batch(4, date_time_in_three_hours=True)
