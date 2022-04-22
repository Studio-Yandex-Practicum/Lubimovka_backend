import pytest
from django.conf import settings
from django.urls import reverse

from apps.core.factories import ImageFactory, PersonFactory
from apps.info.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    PartnerFactory,
    SelectorFactory,
    SponsorFactory,
    VolunteerFactory,
)

FESTIVAL_URL_NAME = "festivals"
FESTIVAL_YEARS_URL = reverse("festivals-years")
TEAMS_URL = reverse("festival-teams")
TEAMS_URL_FILTER = TEAMS_URL + "?team="
SPONSORS_URL = reverse("sponsors")
VOLUNTEERS_URL = reverse("volunteers")
PARTNERS_URL = reverse("partners")


@pytest.fixture(autouse=True)
def set_media_temp_folder(tmpdir):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")


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
def festival_teams(persons_with_image):
    return FestivalTeamFactory.create_batch(5)


@pytest.fixture
def images():
    return ImageFactory.create_batch(10)


@pytest.fixture
def festival(images):
    return FestivalFactory()


@pytest.fixture
def volunteer(persons_with_image_email_city, festival):
    return VolunteerFactory()


@pytest.fixture
def volunteers(persons_with_image_email_city, festival):
    return VolunteerFactory.create_batch(5)


@pytest.fixture
def selector(persons_with_image_email_city, festival):
    return SelectorFactory()


@pytest.fixture
def selectors(persons_with_image_email_city, festival):
    return SelectorFactory.create_batch(5)


@pytest.fixture
def partner():
    return PartnerFactory()


@pytest.fixture
def partners():
    return PartnerFactory.create_batch(5)
