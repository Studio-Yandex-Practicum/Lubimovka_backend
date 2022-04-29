from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.urls import reverse

from apps.articles.factories import NewsItemFactory

pytestmark = [pytest.mark.django_db]

NEWS_YEARS_MONTH_URL = reverse("news-item-years-months")
MOSCOW_TZ = ZoneInfo("Europe/Moscow")


@pytest.fixture
def news_item_1_1995_november():
    return NewsItemFactory(
        title="first_year_1995_month_november",
        pub_date=datetime(1995, 11, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


@pytest.fixture
def news_item_2_1995_november():
    return NewsItemFactory(
        title="second_year_1995_month_november",
        pub_date=datetime(1995, 11, 25, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


@pytest.fixture
def news_item_3_2000_january():
    return NewsItemFactory(
        title="year_2000_month_january",
        pub_date=datetime(2000, 1, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


@pytest.fixture
def news_item_4_2000_october():
    return NewsItemFactory(
        title="year_2000_month_october",
        pub_date=datetime(2000, 10, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


def test_news_item_years_months_fields(client, news_item_1_1995_november):
    """Verify that received objects has expected fields."""
    response_data = client.get(NEWS_YEARS_MONTH_URL).data
    (year_month,) = response_data

    assert "year" in year_month
    assert year_month["year"] == news_item_1_1995_november.pub_date.year
    assert "month" in year_month
    assert year_month["month"] == news_item_1_1995_november.pub_date.month


def test_news_item_years_months_empty_when_blog_items_not_published(client, news_item_not_published):
    """Count the amount of results. All `NewsItem` objects are not published and result should be empty."""
    response_data = client.get(NEWS_YEARS_MONTH_URL).data

    assert len(response_data) == 0, "Not published objects should not influence years-month response."


def test_news_item_years_month_ordering(
    client, news_item_1_1995_november, news_item_3_2000_january, news_item_4_2000_october
):
    """The response should be ordered by years DESC and by month ASC."""
    response_data = client.get(NEWS_YEARS_MONTH_URL).data
    (first_data, second_data, third_data) = response_data

    assert first_data["year"] == news_item_3_2000_january.pub_date.year
    assert first_data["month"] == news_item_3_2000_january.pub_date.month
    assert second_data["year"] == news_item_4_2000_october.pub_date.year
    assert second_data["month"] == news_item_4_2000_october.pub_date.month
    assert third_data["year"] == news_item_1_1995_november.pub_date.year
    assert third_data["month"] == news_item_1_1995_november.pub_date.month


def test_news_item_years_months_distinct(client, news_item_1_1995_november, news_item_2_1995_november):
    """Years-month objects should be distinct in response."""
    response_data = client.get(NEWS_YEARS_MONTH_URL).data

    assert len(response_data) == 1, "The object `years-month` has to be unique in response."
