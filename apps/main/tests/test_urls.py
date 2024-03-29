import pytest

from apps.main.tests.conftest import MAIN_URL

pytestmark = pytest.mark.django_db


class TestMainAPIUrls:
    def test_main_urls(
        self,
        client,
        news_items_with_content,
        blog_items_with_content,
        banners,
        plays,
        places,
        events_hidden_on_main,
    ):
        """Checks status code for main url."""
        response = client.get(MAIN_URL)
        assert response.status_code == 200, f"Проверьте, что при GET запросе " f"{MAIN_URL} возвращается статус 200"
