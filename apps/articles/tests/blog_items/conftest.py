import pytest

from apps.articles.factories import BlogItemFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture(params=["IN_PROCESS", "REVIEW", "READY_FOR_PUBLICATION", "REMOVED_FROM_PUBLICATION"])
def blog_item_not_published(request):
    yield BlogItemFactory(
        # id=200,
        status=request.param
    )


@pytest.fixture
def blog_item_published():
    """Create published BlogItem."""
    return BlogItemFactory(id=100, status="PUBLISHED")
