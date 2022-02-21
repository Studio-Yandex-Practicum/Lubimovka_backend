from typing import Union

from apps.core.models import Setting


def afisha_festival_status() -> dict[str, Union[str, bool]]:
    """Return festival status and Afisha's page header data."""
    festival_status = Setting.get_setting("festival_status")
    description = Setting.get_setting("afisha_description")
    info_registration = Setting.get_setting("afisha_info_festival_text")
    asterisk_text = Setting.get_setting("afisha_asterisk_text")
    afisha_festival_status_data = {
        "festival_status": festival_status,
        "description": description,
        "info_registration": info_registration,
        "asterisk_text": asterisk_text,
    }
    return afisha_festival_status_data
