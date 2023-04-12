import pytest
from django.urls import reverse
from rest_framework import status

from apps.info.models import FestivalTeamMember

pytestmark = pytest.mark.django_db


TEAMS_URL = reverse("festival-teams")
TEAMS_URL_FILTER = TEAMS_URL + "?team="
SPONSORS_URL = reverse("sponsors")
VOLUNTEERS_URL = reverse("volunteers")
SELECTORS_URL = reverse("selectors")


ABOUT_FESTIVAL_URLS_AND_FIXTURES = (
    (TEAMS_URL, pytest.lazy_fixture("festival_team")),
    (SPONSORS_URL, pytest.lazy_fixture("sponsor")),
    (VOLUNTEERS_URL, pytest.lazy_fixture("volunteer")),
    (SELECTORS_URL, pytest.lazy_fixture("selector")),
)


class TestAboutFestivalAPIViews:
    @pytest.mark.parametrize(
        "url, objects",
        [
            (TEAMS_URL, pytest.lazy_fixture("festival_teams")),
            (SPONSORS_URL, pytest.lazy_fixture("sponsors")),
            (VOLUNTEERS_URL, pytest.lazy_fixture("volunteers")),
            (SELECTORS_URL, pytest.lazy_fixture("selectors")),
        ],
    )
    def test_objects_count_in_response_matches_count_in_db(self, client, url, objects):
        """Checks that count objects in response matches count in db for team, sponsor, volunteer."""
        response = client.get(url)
        objects_in_response = response.json()
        count_objects = len(objects_in_response)
        objects_count_in_db = len(set(objects))
        assert objects_count_in_db == count_objects, f"Проверьте, что при GET запросе {url} возвращаются все объекты"

    @pytest.mark.parametrize(
        "teams_filter",
        (
            FestivalTeamMember.TeamType.ART_DIRECTION,
            FestivalTeamMember.TeamType.FESTIVAL_TEAM,
        ),
    )
    def test_get_teams_with_filter(self, client, festival_teams, teams_filter):
        """Checks that we can get teams with filter."""
        url = TEAMS_URL_FILTER + teams_filter
        response = client.get(url)
        count_teams_in_db = FestivalTeamMember.objects.filter(team=teams_filter).count()
        count_teams_in_response = len(response.json())
        assert (
            count_teams_in_db == count_teams_in_response
        ), f"Проверьте, что при GET запросе {url} возвращаются только соответствующие объекты"

    def test_get_team_fields(self, client, festival_team):
        """Checks team field in response."""
        url = TEAMS_URL
        response = client.get(url)
        data = response.json()
        for field in (
            "id",
            "team",
            "position",
        ):
            team_field_in_response = data[0].get(field)
            team_field_in_db = getattr(festival_team, field)
            assert (
                team_field_in_response == team_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    def test_get_sponsor_fields(self, client, sponsor):
        """Checks sponsor field in response."""
        url = SPONSORS_URL
        response = client.get(url)
        data = response.json()
        for field in (
            "id",
            "position",
        ):
            team_field_in_response = data[0].get(field)
            team_field_in_db = getattr(sponsor, field)
            assert (
                team_field_in_response == team_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    def test_get_volunteer_fields(self, client, volunteer):
        """Checks volunteer field in response."""
        url = VOLUNTEERS_URL
        response = client.get(url)
        data = response.json()
        for field in ("id", "review_title", "review_text"):
            volunteer_field_in_response = data[0].get(field)
            volunteer_field_in_db = getattr(volunteer, field)
            assert (
                volunteer_field_in_response == volunteer_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    def test_get_selector_fields(self, client, selector):
        """Checks selector field in response."""
        url = SELECTORS_URL
        response = client.get(url)
        data = response.json()
        for field in ("id", "position"):
            selector_field_in_response = data[0].get(field)
            selector_field_in_db = getattr(selector, field)
            assert (
                selector_field_in_response == selector_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    @pytest.mark.parametrize("url, object", ABOUT_FESTIVAL_URLS_AND_FIXTURES)
    def test_get_fields_for_person(self, client, url, object):
        """Checks fields for person field for team, sponsor, volunteer."""
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
            assert (
                object_field_in_response == object_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    @pytest.mark.parametrize("url, object", ABOUT_FESTIVAL_URLS_AND_FIXTURES)
    def test_get_image_for_person(self, client, url, object):
        """Checks image field in person for team, sponsor, volunteer."""
        response = client.get(url)
        data = response.json()
        image_url_in_response = data[0].get("person").get("image")
        image_url_in_db = object.person.image.url
        assert image_url_in_response.endswith(
            image_url_in_db
        ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение 'image' неправильное"

    def test_selectors_item_by_year_filter(self, client, selector):
        """Get filtered selectors and compare `count` with expected number of objects in database."""
        query_params = {"year": "2020"}
        response = client.get(SELECTORS_URL, query_params)
        count = len(response.data)
        assert count == 1, f"Проверьте фильтрацию по году. Ожидалось только {count} объекта в этом году."

    def test_selectors_item_list_bad_year_filter(self, client, selector):
        """Get filtered response with bad year query params."""
        bad_query_params = [
            {"year": "-1"},
            {"year": "0"},
            {"year": "1"},
            {"year": "-1000000000000000"},
            {"year": "1000000000000000"},
            {"year": "1995.000000000000000001"},
            {"year": "1,995e+3"},
            {"year": "0x7CB"},
            {"year": "NULL"},
            {"year": "Test"},
        ]
        for query_params in bad_query_params:
            response = client.get(SELECTORS_URL, query_params)
            assert response.status_code == status.HTTP_400_BAD_REQUEST, (
                f"Проверьте валидацию по фильтру year для значения: {query_params['year']}. "
                "Должен возвращаться код: 400."
            )

    def test_volunteers_item_by_year_filter(self, client, volunteer):
        """Get filtered volunteers and compare `count` with expected number of objects in database."""
        query_params = {"year": "2020"}
        response = client.get(VOLUNTEERS_URL, query_params)
        count = len(response.data)
        assert count == 1, f"Проверьте фильтрацию по году. Ожидалось только {count} объект в этом году."

    def test_volunteers_item_list_bad_year_filter(self, client, volunteer):
        """Get filtered response with bad year query params."""
        bad_query_params = [
            {"year": "-1"},
            {"year": "0"},
            {"year": "1"},
            {"year": "-1000000000000000"},
            {"year": "1000000000000000"},
            {"year": "1995.000000000000000001"},
            {"year": "1,995e+3"},
            {"year": "0x7CB"},
            {"year": "NULL"},
            {"year": "Test"},
        ]
        for query_params in bad_query_params:
            response = client.get(VOLUNTEERS_URL, query_params)
            assert response.status_code == status.HTTP_400_BAD_REQUEST, (
                f"Проверьте валидацию по фильтру year для значения: {query_params['year']}. "
                "Должен возвращаться код: 400."
            )
