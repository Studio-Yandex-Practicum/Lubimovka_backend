import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.afisha.factories import EventFactory, PerformanceFactory
from apps.core.factories import PersonFactory
from apps.info.factories import FestivalFactory, InfoLinkFactory
from apps.library.factories import AuthorFactory, PlayFactory, ProgramTypeFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return APIClient(format="json")


@pytest.fixture(autouse=True)
def set_media_temp_folder(tmpdir):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")


@pytest.fixture
def festivals():
    return FestivalFactory.create_batch(5)


@pytest.fixture
def program_types():
    return ProgramTypeFactory.create_batch(5)


@pytest.fixture
def links(festivals):
    return InfoLinkFactory.create_batch(10)


@pytest.fixture
def persons_email_city_image():
    return PersonFactory.create_batch(10, add_city=True, add_email=True, add_image=True)


@pytest.fixture
def authors(persons_email_city_image, festivals, program_types):
    return AuthorFactory.complex_create(5)


@pytest.fixture
def plays(authors, festivals):
    return PlayFactory.create_batch(10)


@pytest.fixture
def persons():
    return PersonFactory.create_batch(10)


@pytest.fixture
def performances(persons, plays):
    return PerformanceFactory.complex_create(3)


@pytest.fixture
def events(performances):
    return EventFactory.create_batch(3)
