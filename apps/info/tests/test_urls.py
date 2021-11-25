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


class TestQuestionsAPIUrls:
    def test_question_url(self, client):
        data = {
            "question": "Text",
            "author_name": "Name",
            "author_email": "author@mail.ru",
        }
        response = client.post(QUESTIONS_URL, data=data)
        assert response.status_code == 201, (
            f"Проверьте, что при POST запросе {QUESTIONS_URL} "
            f"возвращается статус 201"
        )
