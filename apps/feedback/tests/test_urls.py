import pytest
from django.urls import reverse

QUESTIONS_URL = reverse("questions")


pytestmark = pytest.mark.django_db


class TestQuestionsAPIUrls:
    """Checks status code for question url."""

    def test_question_url(self, client):
        data = {
            "question": "Text",
            "author_name": "Name",
            "author_email": "author@mail.ru",
        }
        url = QUESTIONS_URL
        response = client.post(url, data=data)
        assert response.status_code == 201, f"Проверьте, что при POST запросе {url} возвращается статус 201"
