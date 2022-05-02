import pytest
from django.urls import reverse

from apps.feedback.models import Question

QUESTIONS_URL = reverse("questions")

pytestmark = pytest.mark.django_db


class TestQuestionsAPIViews:
    def test_question_url(self, client):
        """Checks that question object add in db with correct fields values."""
        data = {
            "question": "Text",
            "author_name": "Name",
            "author_email": "author@mail.ru",
        }
        url = QUESTIONS_URL
        response = client.post(url, data=data)
        question = Question.objects.filter(question=data["question"])
        assert 201 == response.status_code
        assert question.exists() is True
