from django.db.models import Prefetch, QuerySet
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

from apps.articles.filters import PubDateFilter
from apps.articles.models import BlogItem


def blog_item_list_get(filters: dict[str, str] = None) -> QuerySet:
    """Return published and filtered `BlogItem` queryset."""
    filters = filters or {}
    published_blog_items = BlogItem.ext_objects.published()
    return PubDateFilter(filters, published_blog_items).qs


def blog_item_detail_get(blog_item_id):
    """Return `detailed` published `BlogItem` object if it exists.

    The `BlogItem` extends with:
    - _other_blogs: Return latest four `BlogItem` except the object itself.
    - _team: Make `team` data based on `roles` and `blog_persons`.
    Team serialized data has to look like this:
        "team": [
            {
                "name": "Переводчик",
                "slug": "translator",
                "persons": [
                    "Каллистрат Абрамов",
                    "Александра Авдеева"
            },
            {
                ...
            }
        ]
    To do that two things have to be done:
        1. Limit `roles` to distinct `roles`
        2. Limit (prefetch) `blog_persons` (roles reverse relation) with
        blog_item's objects only (typically `role.blog_persons` returns all
        blog_persons, not only related to exact blog_item).
    """
    published_blog_items = BlogItem.ext_objects.published()
    blog_item = get_object_or_404(published_blog_items, id=blog_item_id)

    blog_item._other_blogs = published_blog_items.exclude(id=blog_item_id)[:4]

    blog_item_roles = blog_item.roles.distinct()
    blog_item_persons = blog_item.blog_persons.all()
    blog_item_persons_full_name = blog_item_persons.annotate(
        annotated_full_name=Concat("person__first_name", V(" "), "person__last_name")
    )
    blog_item._team = blog_item_roles.prefetch_related(Prefetch("blog_persons", queryset=blog_item_persons_full_name))

    return blog_item
