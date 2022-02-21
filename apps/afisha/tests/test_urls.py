import pytest
from rest_framework import status

pytestmark = [pytest.mark.django_db]


def test_afisha_festival_status_smoke(client):
    response = client.get("/api/v1/afisha/festival-status/")
    assert response.status_code == status.HTTP_200_OK


def test_afisha_events_smoke(client):
    response = client.get("/api/v1/afisha/festival-status/")
    assert response.status_code == status.HTTP_200_OK
