import pytest
from rest_framework import status

pytestmark = [pytest.mark.django_db]


def test_blog_item_list_smoke(client):
    response = client.get("/api/v1/blog/")
    assert response.status_code == status.HTTP_200_OK


def test_blog_item_detail_smoke(client, blog_published):
    response = client.get("/api/v1/blog/100/")
    assert response.status_code == status.HTTP_200_OK


def test_blog_item_years_months_smoke(client):
    response = client.get("/api/v1/blog/years-months/")
    assert response.status_code == status.HTTP_200_OK
