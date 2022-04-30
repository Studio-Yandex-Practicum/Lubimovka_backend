import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "url",
    (
        "/api/v1/info/partners/",
        "/api/v1/info/festivals/years/",
        "/api/v1/info/about-festival/selectors/",
        "/api/v1/info/about-festival/sponsors/",
        "/api/v1/info/about-festival/team/",
        "/api/v1/info/about-festival/volunteers/",
    ),
)
def test_info_url_smoke(client, url):
    """Smoke test. Status code check only."""
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_info_url_festival_detail_smoke(client, festival_2020):
    """Smoke test for exact festival."""
    response = client.get("/api/v1/info/festivals/2020/")
    assert response.status_code == status.HTTP_200_OK
