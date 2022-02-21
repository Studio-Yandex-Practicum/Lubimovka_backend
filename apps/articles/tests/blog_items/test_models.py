import pytest
from django.core.exceptions import ObjectDoesNotExist

from apps.articles.factories import BlogItemContentModuleFactory
from apps.articles.models import BlogItem

pytestmark = [pytest.mark.django_db]


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


def test_blog_item_queryset_published(simple_blog_item_not_published, simple_blog_item_published):
    """Check published queryset retrun only `BlogItem` with `is_draft=False`."""
    qs = BlogItem.ext_objects.published()

    is_not_published_in_qs = qs.filter(id=simple_blog_item_not_published.id).exists()
    assert is_not_published_in_qs is False, "Проверьте что блог с `is_draft=True` не отдается в queryset."

    is_published_in_qs = qs.filter(id=simple_blog_item_published.id).exists()
    assert is_published_in_qs is True, "Проверьте что блог с `is_draft=False` есть в queryset."
