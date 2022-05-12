import pytest

from apps.info.factories import FestivalFactory, InfoLinkFactory
from apps.library.factories import PlayFactory, ProgramTypeFactory

pytestmark = [pytest.mark.django_db]


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
def plays(festivals, program_types):
    return PlayFactory.create_batch(10)
