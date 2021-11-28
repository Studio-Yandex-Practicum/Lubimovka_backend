import pytest
from django.urls import reverse

from apps.info.tests.conftest import (
    FESTIVAL_URL_NAME,
    FESTIVAL_YEARS_URL,
    PARTNERS_URL,
    QUESTIONS_URL,
    SPONSORS_URL,
    TEAMS_URL,
    VOLUNTEERS_URL,
)

pytestmark = pytest.mark.django_db


class TestFestivalAPIUrls:
    def test_festival_urls(self, client, festival):
        """Checks status code for festival url"""

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
    """Checks status code for about festival urls"""

    @pytest.mark.parametrize("url", (TEAMS_URL, SPONSORS_URL, VOLUNTEERS_URL))
    def test_about_festival_urls(self, client, url):
        response = client.get(url)
        assert response.status_code == 200, (
            f"Проверьте, что при GET запросе {url} " f"возвращается статус 200"
        )


class TestPartnersAPIUrls:
    """Checks status code for partners url"""

    def test_partners_urls(self, client):
        url = PARTNERS_URL
        response = client.get(url)
        assert response.status_code == 200, (
            f"Проверьте, что при GET запросе {url} " f"возвращается статус 200"
        )


class TestQuestionsAPIUrls:
    """Checks status code for question url"""

    def test_question_url(self, client):
        data = {
            "question": "Text",
            "author_name": "Name",
            "author_email": "author@mail.ru",
        }
        url = QUESTIONS_URL
        response = client.post(url, data=data)
        assert response.status_code == 201, (
            f"Проверьте, что при POST запросе {url} "
            f"возвращается статус 201"
        )
