import pytest
from rest_framework import status

pytestmark = [pytest.mark.django_db]


def test_project_item_list_smoke(client):
    response = client.get("/api/v1/projects/")
    assert response.status_code == status.HTTP_200_OK


def test_project_detail_smoke(client, project_published):
    response = client.get("/api/v1/projects/100/")
    assert response.status_code == status.HTTP_200_OK
