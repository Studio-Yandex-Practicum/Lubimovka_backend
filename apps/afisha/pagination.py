from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.core.models import Setting


class AfishaPagination(PageNumberPagination):
    """Add blocks if festival mode is enabled in pagination response.

    info_registration - the text about registration under the description,
    asterisk_text - text with an asterisk near the title.

    And also changes title and description for the festival.
    """

    def get_paginated_response(self, data):
        is_festival = Setting.get_setting("festival_status")

        response_data = {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "title": Setting.get_setting("afisha_title_regular"),
            "description": Setting.get_setting("afisha_description_regular"),
            "results": data,
        }
        if is_festival:
            response_data["info_registration"] = Setting.get_setting("afisha_info_festival_text")
            response_data["asterisk_text"] = Setting.get_setting("afisha_asterisk_text")
            response_data["title"] = Setting.get_setting("afisha_title_festival")
            response_data["description"] = Setting.get_setting("afisha_description_festival")
        return Response(response_data)
