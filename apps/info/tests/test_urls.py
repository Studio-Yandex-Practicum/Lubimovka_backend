import pytest
from django.urls import reverse

from apps.info.tests.conftest import (
    FESTIVAL_URL_NAME,
    FESTIVAL_YEARS_URL,
    TEAMS_URL,
)


class TestFestivalAPIUrls:
    @pytest.mark.django_db(transaction=True)
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


class TestAboutFestivalAPIUrls:
    @pytest.mark.django_db(transaction=True)
    def test_get_teams(self, client, teams):
        response = client.get(TEAMS_URL)
        data = response.json()
        assert len(teams) == len(data)
