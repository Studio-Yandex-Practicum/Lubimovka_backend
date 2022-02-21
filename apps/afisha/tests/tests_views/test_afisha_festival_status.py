import pytest
from django.urls import reverse

from apps.core.models import Setting

pytestmark = [pytest.mark.django_db]

AFISHA_FESTIVAL_STATUS_URL = reverse("afisha-festival-status")


@pytest.fixture
def expected_afisha_festival_status():
    Setting.objects.filter(settings_key="festival_status").update(boolean=True)
    Setting.objects.filter(settings_key="afisha_description").update(text="some afisha description")
    Setting.objects.filter(settings_key="afisha_info_festival_text").update(text="some info description")
    Setting.objects.filter(settings_key="afisha_asterisk_text").update(text="some afisha asterisk text")

    return {
        "festival_status": True,
        "description": "some afisha description",
        "info_registration": "some info description",
        "asterisk_text": "some afisha asterisk text",
    }


def test_afisha_festival_status_response(client, expected_afisha_festival_status):
    """Compare returned JSON with expected one."""
    response_data = client.get(AFISHA_FESTIVAL_STATUS_URL).data
    assert response_data == expected_afisha_festival_status
