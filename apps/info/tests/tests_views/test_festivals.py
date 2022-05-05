from datetime import datetime

import pytest
from django.urls import reverse

FESTIVAL_URL_NAME = "festivals"
FESTIVAL_YEARS_URL = reverse("festivals-years")

pytestmark = pytest.mark.django_db


class TestFestivalAPIViews:
    def test_get_festival_fields(self, client, festival_2020):
        """Checks festival field in response."""
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival_2020.year})
        response = client.get(url)
        data = response.json()
        for field in (
            "description",
            "year",
            "plays_count",
            "selected_plays_count",
            "selectors_count",
            "volunteers_count",
            "events_count",
            "cities_count",
            "blog_entries",
            "video_link",
        ):
            festival_field_in_response = data.get(field)
            festival_field_in_db = getattr(festival_2020, field)
            assert (
                festival_field_in_response == festival_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"
        for field in (
            "start_date",
            "end_date",
        ):
            date = data.get(field)
            festival_field_in_response = datetime.strptime(date, "%Y-%m-%d").date()
            festival_field_in_db = getattr(festival_2020, field)
            assert (
                festival_field_in_response == festival_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    @pytest.mark.parametrize(
        "field",
        (
            "volunteers",
            "images",
        ),
    )
    def test_get_volunteers_and_images_from_festival(self, client, festival_2020, field):
        """Checks volunteers and images count in festival."""
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival_2020.year})
        response = client.get(url)
        data = response.json()
        objects_count_in_response = len(data.get(field))
        objects_count_in_db = getattr(festival_2020, field).all().count()
        assert (
            objects_count_in_response == objects_count_in_db
        ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    def test_get_festival_years(self, client, festival_2020):
        """Check getting festival years."""
        url = FESTIVAL_YEARS_URL
        response = client.get(url)
        data = response.json()
        year_in_db = getattr(festival_2020, "year")
        years_in_response = data.get("years")
        assert (
            year_in_db in years_in_response
        ), f"Проверьте, что при GET запросе {url} возвращается список годов фестивалей"

    @pytest.mark.parametrize(
        "field",
        (
            "plays_links",
            "additional_links",
        ),
    )
    def test_get_links_from_festival(self, client, festival_2020, field):
        """Checks links count in festival."""
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival_2020.year})
        response = client.get(url)
        data = response.json()
        objects_count_in_response = len(data.get(field))
        objects_count_in_db = getattr(festival_2020, "links").filter(type=field).count()
        assert (
            objects_count_in_response == objects_count_in_db
        ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"
