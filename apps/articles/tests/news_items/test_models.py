import pytest
from django.core.exceptions import ObjectDoesNotExist

from apps.articles.factories import NewsItemContentModuleFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture(
    params=(
        {"array_image": True},
        {"array_person": True},
        {"array_play": True},
        {"unit_rich_text": True},
    )
)
def news_item_content_module(request, one_news_published, plays, persons):
    content_module_param = request.param
    return NewsItemContentModuleFactory.create(content_page=one_news_published, **content_module_param)


def test_news_item_delete_related_content_module(news_item_content_module, plays, festivals):
    """Delete `ContentModule` object and check that related object also deleted."""
    item = news_item_content_module.item
    news_item_content_module.delete()

    with pytest.raises(ObjectDoesNotExist):
        item.refresh_from_db()
