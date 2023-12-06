import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.core.factories import PersonFactory
from apps.core.models import Setting
from apps.info.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    InfoLinkFactory,
    SelectorFactory,
    SponsorFactory,
    VolunteerFactory,
)


@pytest.fixture(autouse=True)
def set_show_settings():
    """Show all related people by default."""
    Setting.objects.filter(settings_key__in=("show_team", "show_sponsors", "show_volunteers")).update(boolean=True)


@pytest.fixture(autouse=True)
def set_media_temp_folder(tmpdir):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")


@pytest.fixture(autouse=True)
def client():
    return APIClient(format="json")


@pytest.fixture
def persons_with_image():
    return PersonFactory.create_batch(10, add_image=True)


@pytest.fixture
def persons_with_image_email_city():
    return PersonFactory.create_batch(10, add_image=True, add_email=True, add_city=True)


@pytest.fixture
def sponsor(persons_with_image):
    return SponsorFactory()


@pytest.fixture
def sponsors(persons_with_image):
    return SponsorFactory.create_batch(5)


@pytest.fixture
def festival_team(persons_with_image):
    return FestivalTeamFactory(person=PersonFactory(add_image=True))


@pytest.fixture
def festival_teams(persons_with_image_email_city):
    return FestivalTeamFactory.create_batch(5)


@pytest.fixture
def festival_2020():
    return FestivalFactory(year=2020)


@pytest.fixture
def links(festival_2020):
    return InfoLinkFactory.create_batch(10)


@pytest.fixture
def volunteer(persons_with_image_email_city, festival_2020):
    return VolunteerFactory()


@pytest.fixture
def volunteers(persons_with_image_email_city, festival_2020):
    return VolunteerFactory.create_batch(5)


@pytest.fixture
def selector(persons_with_image_email_city, festival_2020):
    return SelectorFactory()


@pytest.fixture
def selectors(persons_with_image_email_city, festival_2020):
    return SelectorFactory.create_batch(5)
