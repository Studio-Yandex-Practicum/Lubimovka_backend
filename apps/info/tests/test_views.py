from datetime import datetime

import pytest
from django.urls import reverse

from apps.info.models import FestivalTeam, Question
from apps.info.tests.conftest import (
    FESTIVAL_URL_NAME,
    FESTIVAL_YEARS_URL,
    PARTNERS_URL,
    QUESTIONS_URL,
    SPONSORS_URL,
    TEAMS_URL,
    TEAMS_URL_FILTER,
    VOLUNTEERS_URL,
)

pytestmark = pytest.mark.django_db

ABOUT_FESTIVAL_URLS_AND_FIXTURES = [
    (TEAMS_URL, pytest.lazy_fixture("team")),
    (SPONSORS_URL, pytest.lazy_fixture("sponsor")),
    (VOLUNTEERS_URL, pytest.lazy_fixture("volunteer")),
]


class TestFestivalAPIViews:
    def test_get_festival_fields(self, client, festival):
        """Checks festival field in response."""
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year})
        response = client.get(url)
        data = response.json()
        for field in (
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
            assert (
                festival_field_in_response == festival_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"
        for field in (
            "start_date",
            "end_date",
        ):
            date = data.get(field)
            festival_field_in_response = datetime.strptime(date, "%Y-%m-%d").date()
            festival_field_in_db = getattr(festival, field)
            assert (
                festival_field_in_response == festival_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    @pytest.mark.parametrize(
        "field",
        (
            "volunteers",
            "images",
        ),
    )
    def test_get_volunteers_and_images_from_festival(self, client, festival, field):
        """Checks volunteers and images count in festival."""
        url = reverse(FESTIVAL_URL_NAME, kwargs={"year": festival.year})
        response = client.get(url)
        data = response.json()
        objects_count_in_response = len(data.get(field))
        objects_count_in_db = getattr(festival, field).all().count()
        assert (
            objects_count_in_response == objects_count_in_db
        ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    def test_get_festival_years(self, client, festival):
        """Check getting festival years."""
        url = FESTIVAL_YEARS_URL
        response = client.get(url)
        data = response.json()
        year_in_db = getattr(festival, "year")
        years_in_response = data.get("years")
        assert (
            year_in_db in years_in_response
        ), f"Проверьте, что при GET запросе {url} возвращается список годов фестивалей"


class TestAboutFestivalAPIViews:
    @pytest.mark.parametrize(
        "url, objects",
        [
            (TEAMS_URL, pytest.lazy_fixture("teams")),
            (SPONSORS_URL, pytest.lazy_fixture("sponsors")),
            (VOLUNTEERS_URL, pytest.lazy_fixture("volunteers")),
        ],
    )
    def test_objects_count_in_response_matches_count_in_db(self, client, url, objects):
        """Checks that count objects in response matches count in db for team, sponsor, volunteer."""
        response = client.get(url)
        objects_in_response = response.json()
        count_objects = len(objects_in_response)
        objects_count_in_db = len(objects)
        assert objects_count_in_db == count_objects, f"Проверьте, что при GET запросе {url} возвращаются все объекты"

    @pytest.mark.parametrize(
        "teams_filter",
        (
            FestivalTeam.TeamType.ART_DIRECTION,
            FestivalTeam.TeamType.FESTIVAL_TEAM,
        ),
    )
    def test_get_teams_with_filter(self, client, teams, teams_filter):
        """Checks that we can get teams with filter."""
        url = TEAMS_URL_FILTER + teams_filter
        response = client.get(url)
        count_teams_in_db = FestivalTeam.objects.filter(team=teams_filter).count()
        count_teams_in_response = len(response.json())
        assert (
            count_teams_in_db == count_teams_in_response
        ), f"Проверьте, что при GET запросе {url} возвращаются только соответствующие объекты"

    def test_get_team_fields(self, client, team):
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
            team_field_in_db = getattr(team, field)
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


class TestPartnersAPIViews:
    def test_partners_count_in_response_matches_count_in_db(self, client, partners):
        """Checks that count partners in response matches count in db."""
        url = PARTNERS_URL
        response = client.get(url)
        objects_count_in_response = len(response.json())
        objects_count_in_db = len(partners)
        assert (
            objects_count_in_db == objects_count_in_response
        ), f"Проверьте, что при GET запросе {url} возвращаются все объекты"

    def test_get_partners_fields(self, client, partner):
        """Checks partners field in response."""
        url = PARTNERS_URL
        response = client.get(url)
        data = response.json()
        for field in ("id", "name", "type", "url"):
            team_field_in_response = data[0].get(field)
            team_field_in_db = getattr(partner, field)
            assert (
                team_field_in_response == team_field_in_db
            ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение {field} неправильное"

    def test_get_image_for_person(self, client, partner):
        """Checks partners image field in response."""
        url = PARTNERS_URL
        response = client.get(url)
        data = response.json()
        image_url_in_response = data[0].get("image")
        image_url_in_db = partner.image.url
        assert image_url_in_response.endswith(
            image_url_in_db
        ), f"Проверьте, что при GET запросе {url} возвращаются данные объекта. Значение 'image' неправильное"


class TestQuestionsAPIViews:
    def test_question_url(self, client):
        """Checks that question object add in db with correct fields values."""
        data = {
            "question": "Text",
            "author_name": "Name",
            "author_email": "author@mail.ru",
        }
        url = QUESTIONS_URL
        response = client.post(url, data=data)
        for field, value in data.items():
            question = Question.objects.get(id=response.json().get("id"))
            question_value = getattr(question, field)
            data_value = value
            assert question_value == data_value, (
                f"Проверьте, что при POST запросе {url} "
                f"в базу данных добавляется объект c корректным"
                f"значением поля {field}"
            )
