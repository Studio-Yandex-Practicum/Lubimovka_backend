import pytest
from rest_framework import status

pytestmark = [pytest.mark.django_db]


def test_afisha_info_smoke(client):
    response = client.get("/api/v1/afisha/info/")
    assert response.status_code == status.HTTP_200_OK


def test_afisha_event_list_smoke(client, four_events_october):
    response = client.get("/api/v1/afisha/events/")
    assert response.status_code == status.HTTP_200_OK
