from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.afisha.factories import EventFactory, MasterClassFactory, PerformanceFactory, ReadingFactory
from apps.core.constants import Status
from apps.core.factories import PersonFactory
from apps.core.models import Setting
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
def is_festival_afisha():
    Setting.objects.filter(settings_key="festival_status").update(boolean=True)


@pytest.fixture
def is_not_festival_afisha():
    Setting.objects.filter(settings_key="festival_status").update(boolean=False)


@pytest.fixture
def program_types():
    return ProgramTypeFactory.create_batch(5)


@pytest.fixture
def festivals():
    return FestivalFactory.create_batch(5)


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
def plays(authors, festivals, program_types):
    return PlayFactory.create_batch(10)


@pytest.fixture
def masterclasses(persons_email_city_image):
    return MasterClassFactory.create_batch(5)


@pytest.fixture
def readings(persons_email_city_image, plays):
    return ReadingFactory.create_batch(5)


@pytest.fixture
def performances(persons_email_city_image, plays):
    return PerformanceFactory.create_batch(5, status=Status.PUBLISHED)


@pytest.fixture
def four_events_october(freezer, masterclasses, readings, performances):
    freezer.move_to("2021-09-01")
    event_oct_17 = EventFactory(date_time=datetime(2021, 10, 17, 23, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    event_oct_5 = EventFactory(date_time=datetime(2021, 10, 5, 17, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    first_event_oct_11 = EventFactory(date_time=datetime(2021, 10, 11, 18, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    second_event_oct_11 = EventFactory(date_time=datetime(2021, 10, 11, 10, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    return event_oct_17, event_oct_5, first_event_oct_11, second_event_oct_11
