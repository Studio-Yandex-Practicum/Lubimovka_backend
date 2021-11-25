import pytest
from django.urls import reverse

from apps.info.models import FestivalTeam
from apps.info.tests.conftest import (
    FESTIVAL_URL_NAME,
    FESTIVAL_YEARS_URL,
    SPONSORS_URL,
    TEAMS_URL,
    TEAMS_URL_FILTER,
    VOLUNTEERS_URL,
)

pytestmark = pytest.mark.django_db


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
            festival_field_in_response = data.get(field)
            festival_field_in_db = getattr(festival, field)
            assert festival_field_in_response == festival_field_in_db, (
                f"Проверьте, что при GET запросе {url}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    def test_get_volunteers_and_images_from_festival(self, client, festival):
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year})
        response = client.get(url)
        data = response.json()
        for field in (
            "volunteers",
            "images",
        ):
            objects_count_in_response = len(data.get(field))
            objects_count_in_db = getattr(festival, field).all().count()
            assert objects_count_in_response == objects_count_in_db, (
                f"Проверьте, что при GET запросе {url}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    def test_get_festival_years(self, client, festival):
        response = client.get(FESTIVAL_YEARS_URL)
        data = response.json()
        year_in_db = getattr(festival, "year")
        years_in_response = data.get("years")
        assert year_in_db in years_in_response, (
            f"Проверьте, что при GET запросе {FESTIVAL_YEARS_URL} "
            f"возвращается список годов фестивалей"
        )


class TestAboutFestivalAPIViews:
    def test_objects_count_in_response_matches_count_in_db(
        self, client, teams, sponsors, volunteers
    ):
        """
        Checks if objects count in response matches count in db for:
        - teams
        - sponsors
        - volunteers
        """

        urls_and_objects = {
            TEAMS_URL: teams,
            SPONSORS_URL: sponsors,
            VOLUNTEERS_URL: volunteers,
        }
        for url, objects in urls_and_objects.items():
            response = client.get(url)
            data = response.json()
            objects_count_in_response = len(data)
            objects_count_in_db = len(objects)
            assert objects_count_in_db == objects_count_in_response, (
                f"Проверьте, что при GET запросе {url}"
                f"возвращаются все объекты"
            )

    def test_get_teams_with_filter(self, client, teams):
        filters = (
            FestivalTeam.TeamType.ART_DIRECTION,
            FestivalTeam.TeamType.FESTIVAL_TEAM,
        )
        for teams_filter in filters:
            response = client.get(TEAMS_URL_FILTER + teams_filter)
            data = response.json()
            count_festival_teams_in_db = FestivalTeam.objects.filter(
                team=teams_filter
            ).count()
            count_objects_in_response = len(data)
            assert count_festival_teams_in_db == count_objects_in_response, (
                f"Проверьте, что при GET запросе "
                f"{TEAMS_URL_FILTER + teams_filter}"
                f" возвращаются только соответствующие объекты"
            )

    def test_get_teams_fields(self, client, team):
        response = client.get(TEAMS_URL)
        data = response.json()
        for field in (
            "id",
            "team",
            "position",
        ):
            team_field_in_response = data[0].get(field)
            team_field_in_db = getattr(team, field)
            assert team_field_in_response == team_field_in_db, (
                f"Проверьте, что при GET запросе {TEAMS_URL}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    def test_get_sponsors_fields(self, client, sponsor):
        response = client.get(SPONSORS_URL)
        data = response.json()
        for field in (
            "id",
            "position",
        ):
            team_field_in_response = data[0].get(field)
            team_field_in_db = getattr(sponsor, field)
            assert team_field_in_response == team_field_in_db, (
                f"Проверьте, что при GET запросе {TEAMS_URL}"
                f"возвращаются данные объекта. Значение {field} неправильное"
            )

    def test_get_fields_for_person(self, client, team, sponsor):
        """
        Checks fields for person field for:
        - teams
        - sponsors
        """

        urls_and_objects = {
            TEAMS_URL: team,
            SPONSORS_URL: sponsor,
        }
        for url, object in urls_and_objects.items():
            response = client.get(url)
            data = response.json()
            for field in (
                "id",
                "first_name",
                "last_name",
                "middle_name",
                "city",
                "email",
            ):
                object_field_in_response = data[0].get("person").get(field)
                object_field_in_db = getattr(object.person, field)
                assert object_field_in_response == object_field_in_db, (
                    f"Проверьте, что при GET запросе {url} возвращаются "
                    f"данные объекта. Значение {field} неправильное"
                )

    def test_get_image_for_person(self, client, team, sponsor):
        """
        Checks image field in person for:
        - teams
        - sponsors
        """

        urls_and_objects = {
            TEAMS_URL: team,
            SPONSORS_URL: sponsor,
        }
        for url, object in urls_and_objects.items():
            response = client.get(url)
            data = response.json()
            image_url_in_response = data[0].get("person").get("image")
            image_url_in_db = object.person.image.url
            assert image_url_in_response.endswith(image_url_in_db), (
                f"Проверьте, что при GET запросе {url}"
                f'возвращаются данные объекта. Значение "image" неправильное'
            )
