import pytest
from django.urls import reverse

from apps.info.models import FestivalTeam
from apps.info.tests.conftest import (
    FESTIVAL_URL_NAME,
    FESTIVAL_YEARS_URL,
    TEAMS_URL,
    TEAMS_URL_FILTER,
)


@pytest.mark.django_db(
    pytest.mark.django_db,
)
class TestFestivalAPIViews:
    def test_get_festival_fields(self, client, festival):
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year})
        response = client.get(url)
        data = response.json()
        for field in (
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
        ):
            assert data.get(field) == getattr(festival, field), (
                f"Проверьте, что при GET запросе {url}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    def test_get_volunteers_and_images_from_festival(self, client, festival):
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year})
        response = client.get(url)
        data = response.json()
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

    def test_get_festival_years(self, client, festival):
        response = client.get(FESTIVAL_YEARS_URL)
        data = response.json()

        assert getattr(festival, "year") in data.get("years"), (
            f"Проверьте, что при GET запросе {FESTIVAL_YEARS_URL} "
            f"возвращается список годов фестивалей"
        )


@pytest.mark.django_db(
    pytest.mark.django_db,
)
class TestAboutFestivalAPIViews:
    def test_teams_count_in_response_matches_count_in_db(self, client, teams):
        response = client.get(TEAMS_URL)
        data = response.json()
        assert len(teams) == len(data), (
            f"Проверьте, что при GET запросе {TEAMS_URL}"
            f"возвращаются все объекты"
        )

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

    def test_get_teams_fields(self, client, team):
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

    def test_get_fields_for_person_in_team(self, client, team):
        response = client.get(TEAMS_URL)
        data = response.json()
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

    def test_get_image_for_person_in_team(self, client, team):
        response = client.get(TEAMS_URL)
        data = response.json()
        assert (
            data[0].get("person").get("image").endswith(team.person.image.url)
        ), (
            f"Проверьте, что при GET запросе {TEAMS_URL}"
            f'возвращаются данные объекта. Значение "image" неправильное'
        )
