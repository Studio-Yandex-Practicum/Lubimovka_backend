from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.urls import reverse

from apps.articles.factories import BlogItemFactory

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
    (record,) = response_data

    assert "year" in record
    assert "months" in record


def test_blog_item_years_months_one_publication(client, blog_item_1_1995_november):
    """Verify the response with expected data when one there is one publication."""
    expected_record = {
        "year": blog_item_1_1995_november.pub_date.year,
        "months": [blog_item_1_1995_november.pub_date.month],
    }

    response_data = client.get(BLOG_YEARS_MONTH_URL).data

    assert len(response_data) == 1
    (record,) = response_data
    assert record == expected_record


def test_blog_item_years_months_distinct(client, blog_item_1_1995_november, blog_item_2_1995_november):
    """Verify the response with expected data when there are two publication with same year and month."""
    expected_record = {
        "year": blog_item_1_1995_november.pub_date.year,
        "months": [blog_item_1_1995_november.pub_date.month],
    }

    response_data = client.get(BLOG_YEARS_MONTH_URL).data

    assert len(response_data) == 1
    (record,) = response_data
    assert record == expected_record


def test_blog_item_years_months_empty_when_blog_items_not_published(client, blog_item_not_published):
    """Count the amount of results. All `BlogItem` objects are not published and result should be empty."""
    response_data = client.get(BLOG_YEARS_MONTH_URL).data

    assert len(response_data) == 0, "Not published objects should not influence years-month response."


def test_blog_item_years_month_ordering(
    client, blog_item_1_1995_november, blog_item_3_2000_january, blog_item_4_2000_october
):
    """The response should be ordered by years DESC and by month ASC."""
    first_expected_record = {
        "year": blog_item_3_2000_january.pub_date.year,
        "months": [blog_item_3_2000_january.pub_date.month, blog_item_4_2000_october.pub_date.month],
    }
    second_expected_record = {
        "year": blog_item_1_1995_november.pub_date.year,
        "months": [blog_item_1_1995_november.pub_date.month],
    }
    response_data = client.get(BLOG_YEARS_MONTH_URL).data

    assert len(response_data) == 2

    (first_record, second_record) = response_data
    assert first_record == first_expected_record
    assert second_record == second_expected_record
