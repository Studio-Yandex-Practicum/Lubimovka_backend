import pytest
from django.urls import reverse

from apps.info.tests.conftest import (
    FESTIVAL_URL_NAME,
    FESTIVAL_YEARS_URL,
    PARTNERS_URL,
    SPONSORS_URL,
    TEAMS_URL,
    VOLUNTEERS_URL,
)


@pytest.mark.django_db(
    pytest.mark.django_db,
)
class TestFestivalAPIUrls:
    def test_festival_urls(self, client, festival):
        urls = (
            FESTIVAL_YEARS_URL,
            reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year}),
        )
        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, (
                f"Проверьте, что при GET запросе {url} "
                f"возвращается статус 200"
            )


@pytest.mark.django_db(
    pytest.mark.django_db,
)
class TestAboutFestivalAPIUrls:
    def test_about_festival_urls(self, client):
        urls = (
            TEAMS_URL,
            SPONSORS_URL,
            VOLUNTEERS_URL,
            PARTNERS_URL,
        )
        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, (
                f"Проверьте, что при GET запросе {url} "
                f"возвращается статус 200"
            )
