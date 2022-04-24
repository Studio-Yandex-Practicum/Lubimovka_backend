import pytest

from apps.articles.factories import NewsItemFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture(params=["IN_PROCESS", "REVIEW", "READY_FOR_PUBLICATION", "REMOVED_FROM_PUBLICATION"])
def news_item_not_published(request):
    """Yield all possible `NewsItem` with status other than `PUBLISHED`."""
    yield NewsItemFactory(status=request.param)


@pytest.fixture
def news_item_published():
    """Create published NewsItem."""
    return NewsItemFactory(id=100, status="PUBLISHED")
