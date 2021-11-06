import pytest

from apps.info.models import Festival


@pytest.fixture
def festival():
    return Festival.objects.create(
        start_date="2021-07-14",
        end_date="2021-07-15",
        description="TestTest",
        year=2021,
        blog_entries="Test",
        video_link="http://test/",
    )


class TestFestivalAPI:
    @pytest.mark.django_db
    def test_get_festival(self, client):
        response = client.get("/api/v1/info/festival/")
        assert response.status_code == 200, (
            "Проверьте, что при GET запросе `/api/v1/info/festival/` "
            "возвращается статус 200"
        )

    @pytest.mark.django_db
    def test_get_festival_filter_detail(self, client, festival):
        response = client.get("/api/v1/info/festival/?year=2021")
        data = response.json()
        for field in [
            "start_date",
            "end_date",
            "description",
            "year",
            "blog_entries",
            "video_link",
        ]:
            assert data[0].get(field) == getattr(festival, field), (
                f"Проверьте, что при GET запросе `//api/v1/info/festival/`"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    @pytest.mark.django_db
    def test_get_festival_detail(self, client, festival):
        response = client.get("/api/v1/info/festival/")
        data = response.json()

        assert data[0].get("year") == getattr(festival, "year"), (
            "Проверьте, что при GET запросе `//api/v1/info/festival/ "
            "возвращаются данные объекта. Значение year неправильное"
        )


@pytest.mark.webtest
def test_send_http():
    pass
