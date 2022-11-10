import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "url",
    ("/api/v1/schema/",),
)
def test_core_url_smoke(client, url):
    """Smoke test. Status code check only."""
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
