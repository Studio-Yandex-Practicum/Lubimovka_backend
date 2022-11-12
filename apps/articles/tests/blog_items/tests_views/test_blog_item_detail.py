import pytest
from django.urls import reverse

from apps.articles.factories import BlogItemContentModuleFactory, BlogItemFactory, BlogPersonFactory
from apps.core.factories import PersonFactory, RoleFactory

pytestmark = [pytest.mark.django_db]

BLOG_ITEM_DETAIL_URL = reverse("blog-item-detail", args=(100,))


@pytest.fixture
def three_persons():
    return PersonFactory.create_batch(3)


@pytest.fixture
def role_text():
    role_text = RoleFactory(name="Текст", role_type="blog_persons_role")
    return role_text


@pytest.fixture
def role_translator():
    role_translator = RoleFactory(name="Переводчик", role_type="blog_item_role_type")
    return role_translator


@pytest.fixture
def complex_blog_item(three_persons, role_text, role_translator, festivals, plays, persons, performances):
    blog_item = BlogItemFactory(
        id=100,
        status="PUBLISHED",
    )

    BlogItemContentModuleFactory(unit_rich_text=True, order=0, content_page=blog_item)
    BlogItemContentModuleFactory(array_play=True, order=1, content_page=blog_item)
    BlogItemContentModuleFactory(array_image=True, order=2, content_page=blog_item)
    BlogItemContentModuleFactory(array_person=True, order=3, content_page=blog_item)

    first_person, second_person, third_person = three_persons
    BlogPersonFactory(blog=blog_item, person=first_person, role=role_text)
    BlogPersonFactory(blog=blog_item, person=second_person, role=role_text)
    BlogPersonFactory(blog=blog_item, person=third_person, role=role_translator)
    return blog_item


@pytest.mark.parametrize(
    "first_level_field",
    (
        "id",
        "title",
        "description",
        "image",
        "author_url",
        "author_url_title",
        "pub_date",
        "contents",
        "team",
        "other_blogs",
    ),
)
def test_blog_item_detail_first_level_attributes(client, first_level_field, complex_blog_item):
    """Look for required fields for detailed `BlogItem`. This test checks only first level fields."""
    response = client.get(BLOG_ITEM_DETAIL_URL)
    response_data = response.data

    assert first_level_field in response_data


def test_blog_item_detail_contents_and_order(client, complex_blog_item):
    """Get `contents` array and look for created `ContentModule` attributes. Order is matter."""
    response = client.get(BLOG_ITEM_DETAIL_URL)
    response_contents = response.data.get("contents")
    expected_content_in_order = (
        "contentunitrichtext",
        "playsblock",
        "imagesblock",
        "personsblock",
    )

    assert len(response_contents) == 4, "В созданном объекте должно быть 4 блоков контента."

    for order in range(4):
        content_type = response_contents[order].get("content_type")
        assert content_type == expected_content_in_order[order], "Проверьте порядок следования контента."


def test_blog_item_detail_plays_block_content_fields(client, complex_blog_item):
    """Get `contents` -> `playsblock` item and look for expected fields."""
    response = client.get(BLOG_ITEM_DETAIL_URL)
    response_contents = response.data.get("contents")
    playsblock_content = response_contents[1]
    playsblock_content_item = playsblock_content.get("content_item")

    assert playsblock_content_item.get("title"), "У блока с пьесами должен быть заголовок."
    assert playsblock_content_item.get("items"), "У блока с пьесами должен быть массив элементов (пьес)."
    assert len(playsblock_content_item.get("items")) == 3, "Ожидалось 3 пьесы в блоке с пьесами."

    first_play = playsblock_content_item.get("items")[0]
    expected_play_fields_in_order = (
        "id",
        "name",
        "authors",
        "city",
        "year",
        "url_download",
        "url_download_from",
    )

    for order, field in enumerate(first_play):
        assert field == expected_play_fields_in_order[order], "Проверьте fields и их порядок в элементе пьесы"
