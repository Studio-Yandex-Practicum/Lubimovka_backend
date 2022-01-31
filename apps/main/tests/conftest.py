from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.afisha.tests.factories import EventFactory
from apps.articles.factories.blog_item import BlogItemFactory
from apps.articles.factories.news_factory import NewsFactory
from apps.content_pages.tests.factories import ImageForContentFactory, ImagesBlockFactory
from apps.core.tests.factories import PersonFactory
from apps.info.tests.factories import FestivalFactory, PlaceFactory
from apps.library.tests.factories import MasterClassFactory, PerformanceFactory, PlayFactory, ReadingFactory
from apps.main.tests.factories import BannerFactory

MAIN_URL = reverse("main:main_page")


@pytest.fixture
def images_for_content():
    PersonFactory.create_batch(6)
    return ImageForContentFactory.create_batch(2)


@pytest.fixture
def image(images_for_content):
    return ImagesBlockFactory(add_image=True)


@pytest.fixture
def festival():
    return FestivalFactory(start_date="2021-07-14", end_date="2021-07-15", year="2021")


@pytest.fixture
def plays(festival):
    return list(PlayFactory(year=festival.year) for _ in range(4))


@pytest.fixture
def play(festival):
    return PlayFactory(is_draft=False)


@pytest.fixture
def banners():
    return list(BannerFactory.create_batch(3))


@pytest.fixture
def news(plays, image):
    return list(
        NewsFactory.create_batch(
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
    )


@pytest.fixture
def blog():
    return list(BlogItemFactory.complex_create(1))


@pytest.fixture
def places():
    return list(PlaceFactory.create_batch(3))


@pytest.fixture
def person():
    return list(PersonFactory.create_batch(3))


@pytest.fixture
def master_class(person):
    return list(MasterClassFactory.create_batch(1))


@pytest.fixture
def reading(plays, person):
    return list(ReadingFactory.create_batch(1))


@pytest.fixture
def performance(plays, person):
    return list(PerformanceFactory.create_batch(1))


@pytest.fixture
def events(reading, performance, master_class):
    return list(EventFactory(date_time=timezone.now() + timedelta(hours=1)) for _ in range(4))
