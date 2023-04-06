from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.urls import reverse
from rest_framework import status

from apps.articles.factories import NewsItemFactory

pytestmark = [pytest.mark.django_db]

NEWS_ITEM_LIST_URL = reverse("news-item-list")
MOSCOW_TZ = ZoneInfo("Europe/Moscow")


@pytest.fixture
def news_items_with_known_datetime():
    news_item_1 = NewsItemFactory(
        title="first_year_1995_month_november",
        pub_date=datetime(1995, 11, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )
    news_item_2 = NewsItemFactory(
        title="second_year_1995_month_november",
        pub_date=datetime(1995, 11, 25, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )
    news_item_3 = NewsItemFactory(
        title="year_2000_month_january",
        pub_date=datetime(2000, 1, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )
    news_item_4 = NewsItemFactory(
        title="year_2000_month_october",
        pub_date=datetime(2000, 10, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )
    return news_item_1, news_item_2, news_item_3, news_item_4


@pytest.mark.parametrize("paginator_field", ("count", "next", "previous", "results"))
def test_news_item_list_paginated(client, paginator_field, news_item_published):
    """Look for specific fields for paginated response."""
    response = client.get(NEWS_ITEM_LIST_URL)
    response_data = response.data

    assert paginator_field in response_data


@pytest.mark.parametrize(
    "expected_field",
    (
        "id",
        "pub_date",
        "title",
        "description",
        "image",
    ),
)
def test_news_item_list_fields(client, expected_field, news_item_published):
    """Take the first `NewsItem` representation and look for expected fields."""
    response = client.get(NEWS_ITEM_LIST_URL)
    results = response.data.get("results")
    blog_item_data = results[0]

    assert expected_field in blog_item_data


def test_news_item_list_not_published_in_results(client, news_item_not_published):
    """Count the amount of results. `NewsItem` objects with status other than `PUBLISHED` should not be there."""
    response = client.get(NEWS_ITEM_LIST_URL)
    count = response.data.get("count")

    assert count == 0


def test_news_item_list_year_filter(client, news_items_with_known_datetime):
    """Get filtered response and compare `count` with expected number of objects in database."""
    query_params = {"year": "1995"}
    response = client.get(NEWS_ITEM_LIST_URL, query_params)
    count = response.data.get("count")

    assert count == 2, "Проверьте фильтрацию по году. Ожидалось только 2 объекта в этом году."


def test_news_item_list_bad_year_filter(client, news_items_with_known_datetime):
    """Get filtered response with bad year query params."""
    bad_query_params = [
        {"year": "-1"},
        {"year": "0"},
        {"year": "1"},
        {"year": "1950"},
        {"year": "2775"},
        {"year": "-1000000000000000"},
        {"year": "1000000000000000"},
        {"year": "1995.000000000000000001"},
        {"year": "1,995e+3"},
        {"year": "0x7CB"},
        {"year": "NULL"},
        {"year": "Test"},
    ]
    for query_params in bad_query_params:
        response = client.get(NEWS_ITEM_LIST_URL, query_params)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f"Проверьте валидацию по фильтру year для значения: {query_params['year']}. "
            "Должен возвращаться код: 400."
        )


def test_news_item_list_filter_with_server_change_date(client, freezer, news_items_with_known_datetime):
    """Get filtered response with change server date."""
    query_params = {"year": "1995"}
    freezer.move_to("1981-10-15 12:00")
    response = client.get(NEWS_ITEM_LIST_URL, query_params)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, (
        "Проверьте фильтрацию по году при изменение даты на сервере. " "Должен возвращаться код: 400."
    )


def test_news_item_list_month_filter(client, news_items_with_known_datetime):
    """Get filtered response and compare `count` with expected number of objects in database."""
    query_params = {"month": "11"}
    response = client.get(NEWS_ITEM_LIST_URL, query_params)
    count = response.data.get("count")

    assert count == 2, "Проверьте фильтрацию по месяцу. Ожидалось только 2 объекта в этом месяце."


def test_news_item_list_bad_month_filter(client, news_items_with_known_datetime):
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
        response = client.get(NEWS_ITEM_LIST_URL, query_params)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f"Проверьте валидацию по фильтру month для значения: {query_params['month']}. "
            "Должен возвращаться код: 400."
        )


def test_news_item_list_image_absolute_path(client, news_items_with_known_datetime):
    response = client.get(NEWS_ITEM_LIST_URL)
    results = response.data.get("results")
    news_item_image = results[0].get("image")

    assert "http://" in news_item_image, "Убедитесь, что для картинки отдается абсолютный url."
