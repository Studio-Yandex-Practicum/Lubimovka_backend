import pytest

from apps.core.factories import PersonFactory
from apps.info.factories import FestivalFactory, InfoLinkFactory
from apps.library.factories import AuthorFactory, PlayFactory, ProgramTypeFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def set_media_temp_folder(settings, tmp_path_factory):
    settings.MEDIA_ROOT = tmp_path_factory.mktemp("media")
    settings.HIDDEN_MEDIA_ROOT = tmp_path_factory.mktemp("hidden")
    (settings.HIDDEN_MEDIA_ROOT / "plays").mkdir()


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
    return PlayFactory.create_batch(10, programs=program_types)
