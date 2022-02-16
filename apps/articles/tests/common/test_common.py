import pytest
from django.core.exceptions import ObjectDoesNotExist

from apps.content_pages.factories import ImageForContentFactory
from apps.core.tests.factories import PersonFactory
from apps.info.tests.factories import FestivalFactory
from apps.library.tests.factories import PlayFactory

from ...factories.blog_item import (
    BlogItemFactory,
    BlogItemImagesBlockContentFactory,
    BlogItemPersonsBlockContentFactory,
    BlogItemPlaysBlockContentFactory,
    BlogItemPreambleContentFactory,
    BlogItemQuoteContentFactory,
    BlogItemTextContentFactory,
    BlogItemTitleContentFactory,
)

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def images_for_content():
    return ImageForContentFactory.create_batch(10)


@pytest.fixture
def festivals():
    return FestivalFactory.create_batch(5)


@pytest.fixture
def plays(festivals):
    return PlayFactory.create_batch(10)


@pytest.fixture
def persons():
    return PersonFactory.create_batch(10)


@pytest.fixture
def simple_blog_item():
    """Create BlogItem without contents."""
    return BlogItemFactory.create()


@pytest.fixture(
    params=(
        BlogItemImagesBlockContentFactory,
        BlogItemPersonsBlockContentFactory,
        BlogItemPlaysBlockContentFactory,
        BlogItemPreambleContentFactory,
        BlogItemQuoteContentFactory,
        BlogItemTextContentFactory,
        BlogItemTitleContentFactory,
    )
)
def blog_item_content(request, simple_blog_item, plays, persons, images_for_content):
    content_factory = request.param
    return content_factory.create(content_page=simple_blog_item)


@pytest.mark.django_db
def test_delete_related_content(simple_blog_item, blog_item_content, plays, festivals):
    print(f"festivals={len(festivals)}")
    blog_item = simple_blog_item
    assert blog_item.id == 1
    assert blog_item_content.content_page == blog_item

    item = blog_item_content.item
    blog_item_content.delete()

    with pytest.raises(ObjectDoesNotExist):
        item.refresh_from_db()
