import pytest
from django.urls import reverse

from apps.core.models import Setting

pytestmark = [pytest.mark.django_db]

AFISHA_FESTIVAL_STATUS_URL = reverse("afisha-info")


@pytest.fixture
def afisha_info_settings():
    Setting.objects.filter(settings_key="afisha_description").update(text="some afisha description")
    Setting.objects.filter(settings_key="afisha_info_festival_text").update(text="some info description")
    Setting.objects.filter(settings_key="afisha_asterisk_text").update(text="some afisha asterisk text")
    return None


def test_afisha_info_is_festival_response(client, is_festival_afisha, afisha_info_settings, four_events_october):
    """Test case when `festival_status=True`. Compare returned JSON with expected one."""
    response_data = client.get(AFISHA_FESTIVAL_STATUS_URL).data
    assert response_data == {
        "festival_status": True,
        "description": "some afisha description",
        "info_registration": "some info description",
        "asterisk_text": "some afisha asterisk text",
        "afisha_dates": ["2021-10-05", "2021-10-11", "2021-10-17"],
    }


def test_afisha_info_is_not_festival_response(
    client,
    is_not_festival_afisha,
    afisha_info_settings,
    four_events_october,
):
    """Test case when `festival_status=False`. Compare returned JSON with expected one."""
    response_data = client.get(AFISHA_FESTIVAL_STATUS_URL).data
    assert response_data == {
        "festival_status": False,
        "description": "some afisha description",
        "afisha_dates": ["2021-10-05", "2021-10-11", "2021-10-17"],
    }
