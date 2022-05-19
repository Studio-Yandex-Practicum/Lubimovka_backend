from collections import OrderedDict
from typing import Union

from django.db.models import F, Prefetch, QuerySet
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.articles.filters import PubDateFilter
from apps.articles.models import BlogItem, NewsItem, Project
from apps.core.utils import calculate_hash


def article_get_years_months_publications(
    article_model: Union[BlogItem, NewsItem, Project]
) -> dict[int, dict[int, list[int]]]:
    """Return ordered list of years and months of published BlogItem/NewsItem.

    The list is ordered by years (DESC). Each record should be a dict looked like this:
        {
            "year": 2020
            "months": [2, 3, 10]  <-- ordered ASC
        }
    """
    publications_years_months_qs = (
        article_model.objects.published()
        .annotate(year=F("pub_date__year"), month=F("pub_date__month"))
        .values_list("year", "month")
        .distinct()
        .order_by("-year", "month")
    )

    year_months_records = OrderedDict()
    for year, month in publications_years_months_qs:
        year_record = year_months_records.get(year, {"year": year, "months": []})
        year_record["months"].append(month)
        year_months_records[year] = year_record

    return year_months_records.values()


def blog_item_list_get(filters: dict[str, str] = None) -> QuerySet:
    """Return published and filtered `BlogItem` queryset."""
    filters = filters or {}
    published_blog_items = BlogItem.objects.published()
    return PubDateFilter(filters, published_blog_items).qs


def check_hash(current_hash, id):
    """Check hash and return bool."""
    return current_hash == calculate_hash(id)


def blog_item_detail_get(blog_item_id, item_detail=None):
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
    published_blog_items = BlogItem.objects.published()
    blog_item = item_detail or get_object_or_404(published_blog_items, id=blog_item_id)

    blog_item._other_blogs = published_blog_items.exclude(id=blog_item_id)[:4]

    blog_item_roles = blog_item.roles.distinct()
    blog_item_persons = blog_item.blog_persons.all()
    blog_item_persons_full_name = blog_item_persons.annotate(
        annotated_full_name=Concat("person__first_name", V(" "), "person__last_name")
    )
    blog_item._team = blog_item_roles.prefetch_related(Prefetch("blog_persons", queryset=blog_item_persons_full_name))

    return blog_item


def preview_item_detail_get(article_model, object_id, hash_sum=None):
    """Return object for preview page if hash matches."""
    if hash_sum and check_hash(hash_sum, object_id):
        return article_model.objects.preview(object_id)
    raise Http404()
