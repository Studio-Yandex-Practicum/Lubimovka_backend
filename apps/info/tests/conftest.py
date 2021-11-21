import random

import pytest
from django.urls import reverse

from apps.core.tests.factories import PersonFactory
from apps.info.tests.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    SponsorFactory,
    VolunteerFactory,
)

FESTIVAL_URL_NAME = "festivals"
FESTIVAL_YEARS_URL = reverse("festivals_years")
TEAMS_URL = reverse("festival-teams")
TEAMS_URL_FILTER = TEAMS_URL + "?team="
SPONSORS_URL = reverse("sponsors")
VOLUNTEERS_URL = reverse("volunteers")
PARTNERS_URL = reverse("partners")
QUESTIONS_URL = reverse("questions")


@pytest.fixture
def sponsor():
    return list(
        SponsorFactory(person=PersonFactory())
        for _ in range(random.randint(0, 5))
    )


@pytest.fixture
def teams():
    return list(
        FestivalTeamFactory(person=PersonFactory())
        for _ in range(random.randint(0, 5))
    )


@pytest.fixture
def team():
    return FestivalTeamFactory(person=PersonFactory(add_image=True))


@pytest.fixture
def volunteer():
    return list(
        VolunteerFactory(person=PersonFactory())
        for _ in range(random.randint(0, 5))
    )


@pytest.fixture
def festival(volunteer):
    return FestivalFactory(
        volunteers=volunteer,
        start_date="2021-07-14",
        end_date="2021-07-15",
    )
