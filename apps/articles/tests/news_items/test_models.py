import pytest
from django.core.exceptions import ObjectDoesNotExist

from apps.articles.factories import NewsItemContentModuleFactory, NewsItemFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def simple_news_item():
    """Create NewsItem without contents."""
    return NewsItemFactory.create()


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
def news_item_content_module(request, simple_news_item, plays, persons):
    content_module_param = request.param
    return NewsItemContentModuleFactory.create(content_page=simple_news_item, **content_module_param)


def test_news_item_delete_related_content(news_item_content_module, plays, festivals):
    item = news_item_content_module.item
    news_item_content_module.delete()

    with pytest.raises(ObjectDoesNotExist):
        item.refresh_from_db()
