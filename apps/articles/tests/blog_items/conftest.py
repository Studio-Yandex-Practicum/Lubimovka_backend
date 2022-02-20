import pytest
from rest_framework.test import APIClient

from apps.articles.factories import BlogItemFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return APIClient(format="json")


@pytest.fixture
def simple_blog_item(persons):
    """Create BlogItem without contents."""
    return BlogItemFactory.create(add_several_co_author=True)


@pytest.fixture
def simple_blog_item_not_published():
    """Create not published BlogItem."""
    return BlogItemFactory(is_draft=True)


@pytest.fixture
def simple_blog_item_published():
    """Create published BlogItem."""
    return BlogItemFactory(id=100, is_draft=False)
