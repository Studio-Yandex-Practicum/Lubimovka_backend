import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.afisha.factories import EventFactory
from apps.core.factories import ImageFactory, PersonFactory
from apps.info.factories import FestivalFactory
from apps.library.factories import (
    MasterClassFactory,
    PerformanceFactory,
    PlayFactory,
    ProgramTypeFactory,
    ReadingFactory,
)

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return APIClient(format="json")


@pytest.fixture(autouse=True)
def set_media_temp_folder(tmpdir):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")


@pytest.fixture
def images():
    return ImageFactory.create_batch(10)


@pytest.fixture
def program_types():
    return ProgramTypeFactory.create_batch(5)


@pytest.fixture
def festivals(images):
    return FestivalFactory.create_batch(5)


@pytest.fixture
def plays(festivals, program_types):
    return PlayFactory.create_batch(10)


@pytest.fixture
def persons_email_city_image():
    return PersonFactory.create_batch(10, add_city=True, add_email=True, add_image=True)


@pytest.fixture
def masterclasses(persons_email_city_image):
    return MasterClassFactory.create_batch(5)


@pytest.fixture
def readings(persons_email_city_image, plays):
    return ReadingFactory.create_batch(5)


@pytest.fixture
def performances(persons_email_city_image, plays):
    return PerformanceFactory.create_batch(5)


@pytest.fixture
def random_events(freezer, masterclasses, readings, performances):
    freezer.move_to("2022-02-23 10:00")
    return EventFactory.create_batch(10)
