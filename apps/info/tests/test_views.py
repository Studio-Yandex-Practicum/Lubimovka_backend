import pytest
from django.urls import reverse

from apps.info.models import FestivalTeam
from apps.info.tests.conftest import (
    FESTIVAL_URL_NAME,
    FESTIVAL_YEARS_URL,
    TEAMS_URL,
    TEAMS_URL_FILTER,
)


class TestFestivalAPIViews:
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


class TestAboutFestivalAPIViews:
    @pytest.mark.django_db(transaction=True)
    def test_get_teams(self, client, teams):
        response = client.get(TEAMS_URL)
        data = response.json()
        assert len(teams) == len(data), (
            f"Проверьте, что при GET запросе {TEAMS_URL}"
            f"возвращаются все объекты"
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_teams_with_filter(self, client, teams):
        filters = [
            FestivalTeam.TeamType.ART_DIRECTION,
            FestivalTeam.TeamType.FESTIVAL_TEAM,
        ]
        for teams_filter in filters:
            response = client.get(TEAMS_URL_FILTER + teams_filter)
            data = response.json()
            assert FestivalTeam.objects.filter(
                team=teams_filter
            ).count() == len(data), (
                f"Проверьте, что при GET запросе "
                f"{TEAMS_URL_FILTER + teams_filter}"
                f" возвращаются только соответствующие объекты"
            )

    @pytest.mark.django_db(transaction=True)
    def test_get_teams_detail(self, client, team):
        response = client.get(TEAMS_URL)
        data = response.json()
        for field in [
            "team",
            "position",
        ]:
            assert data[0].get(field) == getattr(team, field), (
                f"Проверьте, что при GET запросе {TEAMS_URL}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )
        for field in [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "city",
            "email",
        ]:
            assert data[0].get("person").get(field) == getattr(
                team.person, field
            ), (
                f"Проверьте, что при GET запросе {TEAMS_URL}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )
        assert (
            data[0].get("person").get("image").endswith(team.person.image.url)
        ), (
            f"Проверьте, что при GET запросе {TEAMS_URL}"
            f'возвращаются данные объекта. Значение "image" неправильное'
        )
