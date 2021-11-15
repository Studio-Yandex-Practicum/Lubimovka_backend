import pytest
from django.urls import reverse

FESTIVAL_URL_NAME = "festivals"
FESTIVAL_YEARS_URL = reverse("festivals_years")


class TestFestivalAPI:
    @pytest.mark.django_db(transaction=True)
    def test_festival_urls(self, client, festival):
        urls = (
            FESTIVAL_YEARS_URL,
            reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year}),
        )
        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, (
                f"Проверьте, что при GET запросе {url} "
                f"возвращается статус 200"
            )

    @pytest.mark.django_db(transaction=True)
    def test_get_festival_detail(self, client, festival):
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year})
        response = client.get(url)
        data = response.json()
        for field in [
            "start_date",
            "end_date",
            "description",
            "year",
            "plays_count",
            "selected_plays_count",
            "selectors_count",
            "volunteers_count",
            "events_count",
            "cities_count",
            "blog_entries",
            "video_link",
        ]:
            assert data.get(field) == getattr(festival, field), (
                f"Проверьте, что при GET запросе {url}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )
        for field in [
            "volunteers",
            "images",
        ]:

            assert (
                len(data.get(field)) == getattr(festival, field).all().count()
            ), (
                f"Проверьте, что при GET запросе {url}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    @pytest.mark.django_db(transaction=True)
    def test_get_festival_years(self, client, festival):
        response = client.get(FESTIVAL_YEARS_URL)
        data = response.json()

        assert getattr(festival, "year") in data.get("years"), (
            f"Проверьте, что при GET запросе {FESTIVAL_YEARS_URL} "
            f"возвращается список годов фестивалей"
        )


class TestFestivalTeamsAPI:
    @pytest.mark.django_db(transaction=True)
    def test_festival_urls(self, client, festival):
        urls = (
            FESTIVAL_YEARS_URL,
            reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year}),
        )
        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, (
                f"Проверьте, что при GET запросе {url} "
                f"возвращается статус 200"
            )
