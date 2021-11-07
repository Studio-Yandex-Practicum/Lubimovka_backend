import pytest
from django.urls import reverse

from apps.info.models import Festival

YEAR = 2021
FESTIVAL_URL = reverse("festivals", kwargs={"year": YEAR})
FESTIVAL_YEARS_URL = reverse("festivals_years")


@pytest.fixture
def festival():
    return Festival.objects.create(
        start_date="2021-07-14",
        end_date="2021-07-15",
        description="TestTest",
        year=YEAR,
        blog_entries="Test",
        video_link="http://test/",
    )


class TestFestivalAPI:
    @pytest.mark.django_db
    def test_festival_urls(self, client, festival):
        urls = (FESTIVAL_YEARS_URL, FESTIVAL_URL)
        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, (
                f"Проверьте, что при GET запросе {url} "
                f"возвращается статус 200"
            )

    @pytest.mark.django_db
    def test_get_festival_detail(self, client, festival):
        response = client.get(FESTIVAL_URL)
        data = response.json()
        for field in [
            "start_date",
            "end_date",
            "description",
            "year",
            "blog_entries",
            "video_link",
        ]:
            assert data.get(field) == getattr(festival, field), (
                f"Проверьте, что при GET запросе {FESTIVAL_URL}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    @pytest.mark.django_db
    def test_get_festival_years(self, client, festival):
        response = client.get(FESTIVAL_YEARS_URL)
        data = response.json()

        assert getattr(festival, "year") in data.get("years"), (
            f"Проверьте, что при GET запросе {FESTIVAL_YEARS_URL} "
            f"возвращается список годов фестивалей"
        )


@pytest.mark.webtest
def test_send_http():
    pass
