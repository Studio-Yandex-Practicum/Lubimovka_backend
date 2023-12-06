from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.urls import reverse
from rest_framework import status

from apps.articles.factories import BlogItemFactory

pytestmark = [pytest.mark.django_db]

BLOG_ITEM_LIST_URL = reverse("blog-item-list")


@pytest.fixture
def blog_items_with_known_datetime():
    moscow_tz = ZoneInfo("Europe/Moscow")
    blog_item_1 = BlogItemFactory(
        title="year_1995_month_10",
        pub_date=datetime(1995, 10, 12, tzinfo=moscow_tz),
        status="PUBLISHED",
    )
    blog_item_2 = BlogItemFactory(
        title="year_1995_month_11",
        pub_date=datetime(1995, 11, 12, tzinfo=moscow_tz),
        status="PUBLISHED",
    )
    blog_item_3 = BlogItemFactory(
        title="year_1995_month_12",
        pub_date=datetime(1995, 12, 12, tzinfo=moscow_tz),
        status="PUBLISHED",
    )
    blog_item_4 = BlogItemFactory(
        title="year_2000_month_10",
        pub_date=datetime(2000, 10, 12, tzinfo=moscow_tz),
        status="PUBLISHED",
    )
    return blog_item_1, blog_item_2, blog_item_3, blog_item_4


@pytest.mark.parametrize("paginator_field", ("count", "next", "previous", "results"))
def test_blog_item_list_paginated(client, paginator_field, blog_item_published):
    """Look for specific fields for paginated response."""
    response = client.get(BLOG_ITEM_LIST_URL)
    response_data = response.data

    assert paginator_field in response_data


@pytest.mark.parametrize(
    "expected_field",
    (
        "id",
        "pub_date",
        "title",
        "description",
        "author_url",
        "author_url_title",
        "image",
    ),
)
def test_blog_item_list_fields(client, expected_field, blog_item_published):
    """Take the first `BlogItem` representation and look for expected fields."""
    response = client.get(BLOG_ITEM_LIST_URL)
    results = response.data.get("results")
    blog_item_data = results[0]

    assert expected_field in blog_item_data


def test_blog_item_list_not_published_in_results(client, blog_item_not_published):
    """Count the amount of results. `BlogItem` objects with status other than `PUBLISHED` should not be there."""
    response = client.get(BLOG_ITEM_LIST_URL)
    count = response.data.get("count")

    assert count == 0


def test_blog_item_list_year_filter(client, blog_items_with_known_datetime):
    """Get filtered response and compare `count` with expected number of objects in database."""
    query_params = {"year": "1995"}
    response = client.get(BLOG_ITEM_LIST_URL, query_params)
    count = response.data.get("count")

    assert count == 3, "Проверьте фильтрацию по году. Ожидалось только 3 объекта в этом году."


def test_blog_item_list_bad_year_filter(client, blog_items_with_known_datetime):
    """Get filtered response with bad year query params."""
    bad_query_params = [
        {"year": "-1"},
        {"year": "0"},
        {"year": "1"},
        {"year": "-1000000000000000"},
        {"year": "1000000000000000"},
        {"year": "1995.000000000000000001"},
        {"year": "1,995e+3"},
        {"year": "0x7CB"},
        {"year": "NULL"},
        {"year": "Test"},
    ]
    for query_params in bad_query_params:
        response = client.get(BLOG_ITEM_LIST_URL, query_params)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f"Проверьте валидацию по фильтру year для значения: {query_params['year']}. "
            "Должен возвращаться код: 400."
        )


def test_blog_item_list_month_filter(client, blog_items_with_known_datetime):
    """Get filtered response and compare `count` with expected number of objects in database."""
    query_params = {"month": "10"}
    response = client.get(BLOG_ITEM_LIST_URL, query_params)
    count = response.data.get("count")

    assert count == 2, "Проверьте фильтрацию по месяцу. Ожидалось только 2 объекта в этом месяце."


def test_blog_item_list_bad_month_filter(client, blog_items_with_known_datetime):
    """Get filtered response with bad month query params."""
    bad_query_params = [
        {"month": "-1"},
        {"month": "0"},
        {"month": "13"},
        {"month": "14"},
        {"month": "-1000000000000000"},
        {"month": "1000000000000000"},
        {"month": "10.000000000000000001"},
        {"month": "1,e+1"},
        {"month": "0xA"},
        {"month": "NULL"},
        {"month": "Test"},
    ]
    for query_params in bad_query_params:
        response = client.get(BLOG_ITEM_LIST_URL, query_params)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f"Проверьте валидацию по фильтру month для значения: {query_params['month']}. "
            "Должен возвращаться код: 400."
        )


def test_blog_item_list_image_absolute_path(client, blog_items_with_known_datetime):
    response = client.get(BLOG_ITEM_LIST_URL)
    results = response.data.get("results")
    blog_item_image = results[0].get("image")

    assert "http://" in blog_item_image, "Убедитесь, что для картинки отдается абсолютный url."
