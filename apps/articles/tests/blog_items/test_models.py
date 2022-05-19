import pytest
from django.core.exceptions import ObjectDoesNotExist

from apps.articles.factories import BlogItemContentModuleFactory
from apps.articles.models import BlogItem

pytestmark = [pytest.mark.django_db]


@pytest.fixture(
    params=(
        {"array_image": True},
        {"array_person": True},
        {"array_event": True},
        {"array_play": True},
        {"array_video": True},
        {"unit_link": True},
        {"unit_rich_text": True},
    )
)
def blog_item_content_module(request, blog_item_published, events, plays, persons):
    content_module_param = request.param
    return BlogItemContentModuleFactory.create(content_page=blog_item_published, **content_module_param)


def test_blog_item_delete_related_content_module(blog_item_content_module, plays, festivals):
    """Delete `ContentModule` object and check that related object also deleted."""
    item = blog_item_content_module.item
    blog_item_content_module.delete()

    with pytest.raises(ObjectDoesNotExist):
        item.refresh_from_db()


def test_blog_item_queryset_published(blog_item_published, blog_item_not_published):
    """Check published queryset retrun only `BlogItem` with status `PUBLISHED`."""
    qs = BlogItem.objects.published()

    is_not_published_in_qs = qs.filter(id=blog_item_not_published.id).exists()
    assert (
        is_not_published_in_qs is False
    ), f"Проверьте что блог со статусом `{blog_item_not_published.status}` не отдается в queryset."

    is_published_in_qs = qs.filter(id=blog_item_published.id).exists()
    assert is_published_in_qs is True, "Проверьте что блог со статусом `PUBLISHED` есть в queryset."
