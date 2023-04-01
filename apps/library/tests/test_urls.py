import pytest
from rest_framework import status

pytestmark = [pytest.mark.django_db]


def test_slug_determine_404(client):
    response = client.get("/api/v1/library/non_existing_slug/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
