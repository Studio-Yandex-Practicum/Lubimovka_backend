import pytest
from django.http import Http404

from apps.articles import selectors
from apps.articles.factories import BlogItemFactory
from apps.articles.factories.blog_items import BlogPersonFactory
from apps.articles.models import BlogItem
from apps.core.factories import PersonFactory, RoleFactory

pytestmark = [pytest.mark.django_db]


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
def blog_item_with_persons(three_persons, role_text, role_translator):
    blog_item = BlogItemFactory(status="PUBLISHED")
    first_person, second_person, third_person = three_persons
    BlogPersonFactory(blog=blog_item, person=first_person, role=role_text)
    BlogPersonFactory(blog=blog_item, person=second_person, role=role_text)
    BlogPersonFactory(blog=blog_item, person=third_person, role=role_translator)
    return blog_item


def test_selector_blog_item_detail_get_return_only_published(blog_item_not_published):
    """Selector should return 404 if `BlogItem` has status other than `PUBLISHED`."""
    blog_item_id = blog_item_not_published.id
    blog_items_published = BlogItem.ext_objects.published()
    with pytest.raises(Http404):
        selectors.blog_item_detail_get(blog_item_id, blog_items_published)


def test_selector_blog_item_detail_get_type(blog_item_with_persons):
    """Selector should return `BlogItem` object."""
    blog_item_id = blog_item_with_persons.id
    blog_items_published = BlogItem.ext_objects.published()
    blog_item = selectors.blog_item_detail_get(blog_item_id, blog_items_published)

    assert isinstance(blog_item, BlogItem), "Тип возвращаемого объекта `BlogItem`."


@pytest.mark.parametrize("extended_attr", ("_team", "_other_blogs"))
def test_selector_blog_item_detail_get_has_extended_attributes(extended_attr, blog_item_with_persons):
    """Returned `BlogItem` has to be extended with "_other_blogs" and "_team."""
    blog_item_id = blog_item_with_persons.id
    blog_items_published = BlogItem.ext_objects.published()
    blog_item = selectors.blog_item_detail_get(blog_item_id, blog_items_published)

    blog_item_extended_attr = getattr(blog_item, extended_attr, None)
    assert blog_item_extended_attr is not None, f"Проверьте, что в возвращаемом объекте есть {extended_attr}."


def test_selector_blog_item_detail_get_team_annotated_full_name(blog_item_with_persons):
    """`_team.persons` structure has to have `annotated_full_name` attribute."""
    blog_item_id = blog_item_with_persons.id
    blog_items_published = BlogItem.ext_objects.published()
    blog_item = selectors.blog_item_detail_get(blog_item_id, blog_items_published)

    team = blog_item._team
    first_role = team.first()
    first_person_in_role = first_role.blog_persons.first()

    assert first_person_in_role.annotated_full_name


def test_selector_blog_item_detail_get_roles_count(blog_item_with_persons):
    """Check the amount tested object."""
    blog_item_id = blog_item_with_persons.id
    blog_items_published = BlogItem.ext_objects.published()
    blog_item = selectors.blog_item_detail_get(blog_item_id, blog_items_published)
    roles = blog_item._team

    assert roles.count() == 2, "У созданного блога должно быть только 2 роли в команде"


@pytest.mark.parametrize(
    "role_name",
    (
        "Текст",
        "Переводчик",
    ),
)
def test_selector_blog_item_detail_get_roles_names(role_name, blog_item_with_persons):
    """Roles in `_team` should be distinct and match person fixtures."""
    blog_item_id = blog_item_with_persons.id
    blog_items_published = BlogItem.ext_objects.published()
    blog_item = selectors.blog_item_detail_get(blog_item_id, blog_items_published)
    roles = blog_item._team
    roles_names = roles.values_list("name", flat=True)

    assert role_name in roles_names


def test_selector_blog_item_detail_get_role_persons(blog_item_with_persons):
    """Get every role array in `_team` and count persons in it. It should match to expected."""
    blog_item_id = blog_item_with_persons.id
    blog_items_published = BlogItem.ext_objects.published()
    blog_item = selectors.blog_item_detail_get(blog_item_id, blog_items_published)
    roles = blog_item._team

    role_translator = roles.get(slug="translator")
    assert role_translator.blog_persons.count() == 1, "У созданного объекта должен быть только один переводчик."

    role_text = roles.get(slug="text")
    assert role_text.blog_persons.count() == 2, "У созданного объекта должно быть 2 персоны с текстом."
