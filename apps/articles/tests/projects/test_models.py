import pytest
from django.core.exceptions import ObjectDoesNotExist

from apps.articles.factories import ProjectContentModuleFactory, ProjectFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def simple_project():
    """Create Project without contents."""
    return ProjectFactory.create()


@pytest.fixture(
    params=(
        {"array_image": True},
        {"unit_link": True},
        {"array_performance": True},
        {"array_person": True},
        {"array_play": True},
        {"unit_text": True},
        {"array_video": True},
    )
)
def project_content_module(request, simple_project, plays, persons, performances):
    content_module_param = request.param
    return ProjectContentModuleFactory.create(content_page=simple_project, **content_module_param)


def test_project_delete_related_content_module(project_content_module, plays, festivals):
    """Delete `ContentModule` object and check that related object also deleted."""
    item = project_content_module.item
    project_content_module.delete()

    with pytest.raises(ObjectDoesNotExist):
        item.refresh_from_db()
