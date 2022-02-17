import pytest
from django.core.exceptions import ObjectDoesNotExist

from apps.articles.factories import BlogItemContentModuleFactory, BlogItemFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def simple_blog_item(persons):
    """Create BlogItem without contents."""
    return BlogItemFactory.create(add_several_co_author=True)


@pytest.fixture(
    params=(
        {"array_image": True},
        {"array_person": True},
        {"array_play": True},
        {"unit_preamble": True},
        {"unit_quote": True},
        {"unit_text": True},
        {"unit_title": True},
    )
)
def blog_item_content_module(request, simple_blog_item, plays):
    content_module_param = request.param
    return BlogItemContentModuleFactory.create(content_page=simple_blog_item, **content_module_param)


def test_blog_item_delete_related_content_module(blog_item_content_module, plays, festivals):
    """Delete `ContentModule` object and check that related object also deleted."""
    item = blog_item_content_module.item
    blog_item_content_module.delete()

    with pytest.raises(ObjectDoesNotExist):
        item.refresh_from_db()
