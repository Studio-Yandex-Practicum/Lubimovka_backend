import pytest

from apps.articles.factories import NewsItemFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture(params=["IN_PROCESS", "REVIEW", "READY_FOR_PUBLICATION", "REMOVED_FROM_PUBLICATION"])
def one_news_not_published(request):
    yield NewsItemFactory(status=request.param)


@pytest.fixture
def one_news_published():
    """Create published BlogItem."""
    return NewsItemFactory(id=100, status="PUBLISHED")
