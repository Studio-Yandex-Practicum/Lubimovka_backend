from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.urls import reverse

from apps.articles.factories.blog_items import BlogItemFactory

pytestmark = [pytest.mark.django_db]

BLOG_YEARS_MONTH_URL = reverse("blog-item-years-months")
MOSCOW_TZ = ZoneInfo("Europe/Moscow")


@pytest.fixture
def blog_item_1_1995_november():
    return BlogItemFactory(
        title="first_year_1995_month_november",
        pub_date=datetime(1995, 11, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


@pytest.fixture
def blog_item_2_1995_november():
    return BlogItemFactory(
        title="second_year_1995_month_november",
        pub_date=datetime(1995, 11, 25, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


@pytest.fixture
def blog_item_3_2000_january():
    return BlogItemFactory(
        title="year_2000_month_january",
        pub_date=datetime(2000, 1, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


@pytest.fixture
def blog_item_4_2000_october():
    return BlogItemFactory(
        title="year_2000_month_october",
        pub_date=datetime(2000, 10, 12, tzinfo=MOSCOW_TZ),
        status="PUBLISHED",
    )


def test_blog_item_years_months_fields(client, blog_item_1_1995_november):
    """Verify that received objects has expected fields."""
    response_data = client.get(BLOG_YEARS_MONTH_URL).data
    (year_month,) = response_data

    assert "year" in year_month
    assert year_month["year"] == blog_item_1_1995_november.pub_date.year
    assert "month" in year_month
    assert year_month["month"] == blog_item_1_1995_november.pub_date.month


def test_blog_item_years_months_empty_when_blog_items_not_published(client, blog_item_not_published):
    """Count the amount of results. All `BlogItem` objects are not published and result should be empty."""
    response_data = client.get(BLOG_YEARS_MONTH_URL).data

    assert len(response_data) == 0, "Not published objects should not influence years-month response."


def test_blog_item_years_month_ordering(
    client, blog_item_1_1995_november, blog_item_3_2000_january, blog_item_4_2000_october
):
    """The response should be ordered by years DESC and by month ASC."""
    response_data = client.get(BLOG_YEARS_MONTH_URL).data
    (first_data, second_data, third_data) = response_data

    assert first_data["year"] == blog_item_3_2000_january.pub_date.year
    assert first_data["month"] == blog_item_3_2000_january.pub_date.month
    assert second_data["year"] == blog_item_4_2000_october.pub_date.year
    assert second_data["month"] == blog_item_4_2000_october.pub_date.month
    assert third_data["year"] == blog_item_1_1995_november.pub_date.year
    assert third_data["month"] == blog_item_1_1995_november.pub_date.month


def test_blog_item_years_months_distinct(client, blog_item_1_1995_november, blog_item_2_1995_november):
    """Years-month objects should be distinct in response."""
    response_data = client.get(BLOG_YEARS_MONTH_URL).data

    assert len(response_data) == 1, "The object `years-month` has to be unique in response."
