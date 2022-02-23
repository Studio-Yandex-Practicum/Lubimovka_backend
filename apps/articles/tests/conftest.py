import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.core.factories import ImageFactory, PersonFactory
from apps.info.factories import FestivalFactory
from apps.library.factories import PerformanceFactory, PlayFactory

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
def festivals(images):
    return FestivalFactory.create_batch(5)


@pytest.fixture
def plays(festivals):
    return PlayFactory.create_batch(10)


@pytest.fixture
def persons():
    return PersonFactory.create_batch(10)


@pytest.fixture
def performances(persons, plays):
    return PerformanceFactory.complex_create(3)
