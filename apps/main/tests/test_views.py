import pytest

from apps.library.models import Play
from apps.main.tests.conftest import MAIN_URL

pytestmark = pytest.mark.django_db


class TestMainAPIViews:
    def test_get_main_fields(self, client, news, blog, banners, plays):
        """Checks fields in response."""
        fields = ["first_screen", "news", "afisha", "banners", "short_list", "places", "video_archive"]
        response = client.get(MAIN_URL)
        for field in fields:
            assert field in response.data, f"Проверьте, что при GET запросе {MAIN_URL} data содержит {field}"

    def test_get_main_first_screen_fields(self, client, news, blog, banners, plays):
        """Checks data["first_screen"] fields in response."""
        fields = ["title", "url_title", "url"]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                field in response.data["first_screen"]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[first_screen] содержит {field}"

    def test_get_main_news_and_short_list_fields(self, client, news, blog, banners, plays):
        """Checks data["news"] and data["short_list"] fields in response."""
        fields = [
            "title",
            "items",
        ]
        data_fields = ["news", "short_list"]
        response = client.get(MAIN_URL)
        for field in fields:
            for data_field in data_fields:
                assert field in response.data.get(
                    data_field
                ), f"Проверьте, что при GET запросе {MAIN_URL} data[{data_field}] содержит {field}"

    def test_get_main_afisha_fields(self, client, news, blog, banners, plays):
        """Checks data["afisha"] fields in response."""
        fields = [
            "title",
            "description",
            "items",
            "info_registration",
            "asterisk_text",
        ]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                field in response.data["afisha"]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[afisha] содержит {field}"

    def test_get_main_banners_and_places_fields(self, client, news, blog, banners, plays):
        """Checks data["banners"] and data["places"] fields in response."""
        fields = [
            "places",
            "banners",
        ]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                "items" in response.data[field]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[{field}] содержит items"

    def test_get_main_video_archive_fields(self, client, news, blog, banners, plays):
        """Checks data["video_archive"] in response."""
        fields = [
            "url",
            "photo",
        ]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                field in response.data["video_archive"]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[video_archive] содержит items"

    def test_news_count_in_response_matches_count_in_db(self, client, news, blog, banners, plays):
        """Checks that count news in response matches count in db."""
        response = client.get(MAIN_URL)
        objects_count_in_response = len(response.data["news"]["items"])
        objects_count_in_db = len(news)
        assert (
            objects_count_in_db == objects_count_in_response
        ), f"Проверьте, что при GET запросе {MAIN_URL} возвращаются все объекты"

    def test_get_main_news_items_fields(self, client, news, blog, banners, plays):
        """Checks data["news"]["items"] in response."""
        fields = ["id", "title", "description", "image", "pub_date"]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                field in response.data["news"]["items"][0]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[news][items] содержит {field}"

    def test_banners_count_in_response_matches_count_in_db(self, client, news, blog, banners, plays):
        """Checks that count banners in response matches count in db."""
        response = client.get(MAIN_URL)
        objects_count_in_response = len(response.data["banners"]["items"])
        objects_count_in_db = len(banners)
        assert (
            objects_count_in_db == objects_count_in_response
        ), f"Проверьте, что при GET запросе {MAIN_URL} возвращаются все объекты"

    def test_get_main_banners_items_fields(self, client, news, blog, banners, plays):
        """Checks data["banners"]["items"] in response."""
        fields = ["id", "title", "description", "url", "image", "button"]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                field in response.data["banners"]["items"][0]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[banners][items] содержит {field}"

    def test_play_count_in_short_list_in_response_matches_count_in_db(self, client, news, blog, banners, plays):
        """Checks that count play in short list in response matches count in db."""
        response = client.get(MAIN_URL)
        objects_count_in_response = len(response.data["short_list"]["items"])
        objects_count_in_db = Play.objects.filter(is_draft=False).count()
        assert (
            objects_count_in_db == objects_count_in_response
        ), f"Проверьте, что при GET запросе {MAIN_URL} возвращаются все объекты"

    def test_get_main_short_list_items_fields(self, client, news, blog, banners, play):
        """Checks data["short_list"]["items"] in response."""
        fields = [
            "id",
            "name",
            "authors",
            "city",
            "year",
            "url_download",
            "url_reading",
        ]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                field in response.data["short_list"]["items"][0]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[short_list][items] содержит {field}"

    def test_places_count_in_response_matches_count_in_db(self, client, news, blog, banners, plays, places):
        """Checks that count places in response matches count in db."""
        response = client.get(MAIN_URL)
        objects_count_in_response = len(response.data["places"]["items"])
        objects_count_in_db = len(places)
        assert (
            objects_count_in_db == objects_count_in_response
        ), f"Проверьте, что при GET запросе {MAIN_URL} возвращаются все объекты"

    def test_get_main_places_items_fields(self, client, news, blog, banners, play, places):
        """Checks data["places"]["items"] in response."""
        fields = [
            "id",
            "name",
            "description",
            "city",
            "address",
            "map_link",
        ]
        response = client.get(MAIN_URL)
        for field in fields:
            assert (
                field in response.data["places"]["items"][0]
            ), f"Проверьте, что при GET запросе {MAIN_URL} data[places][items] содержит {field}"
