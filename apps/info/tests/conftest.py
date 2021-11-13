import random

import pytest

from apps.core.tests.factories import ImageFactory, PersonFactory
from apps.info.tests.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    SponsorFactory,
    VolunteerFactory,
)


@pytest.fixture
def sponsors():
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
def volunteers():
    return list(
        VolunteerFactory(person=PersonFactory())
        for _ in range(random.randint(0, 5))
    )


@pytest.fixture
def images():
    return list(ImageFactory() for _ in range(random.randint(0, 3)))


@pytest.fixture
def festival(teams, images, sponsors, volunteers):
    images = images
    return FestivalFactory(
        start_date="2021-07-14",
        end_date="2021-07-15",
        # teams=teams,
        # sponsors=sponsors,
        # volunteers=volunteers,
        # images=images,
    )
