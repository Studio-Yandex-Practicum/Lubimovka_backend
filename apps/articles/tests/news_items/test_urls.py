import pytest
from rest_framework import status

pytestmark = [pytest.mark.django_db]


def test_news_item_list_smoke(client):
    response = client.get("/api/v1/news/")
    assert response.status_code == status.HTTP_200_OK


def test_news_item_detail_smoke(client, news_item_published):
    response = client.get("/api/v1/news/100/")
    assert response.status_code == status.HTTP_200_OK


def test_news_item_years_months_smoke(client):
    response = client.get("/api/v1/news/years-months/")
    assert response.status_code == status.HTTP_200_OK
