from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Setting
from apps.info.serializers import EmailsSerializer


class EmailsAPIView(APIView):
    def get(self, request):
        """Get all required emails that can be changed.

        except email on contacts page
        """
        email_for_press = Setting.get_setting("email_for_press")
        email_on_project_page = Setting.get_setting("email_on_project_page")
        email_on_organizers_page = Setting.get_setting("email_on_organizers_page")
        email_on_trustees_page = Setting.get_setting("email_on_trustees_page")
        email_on_about_festival_page = Setting.get_setting("email_on_about_festival_page")
        email_on_acceptance_of_plays_page = Setting.get_setting("email_on_acceptance_of_plays_page")
        email_on_author_page = Setting.get_setting("email_on_author_page")
        data = {
            "email_for_press": email_for_press,
            "email_on_project_page": email_on_project_page,
            "email_on_organizers_page": email_on_organizers_page,
            "email_on_trustees_page": email_on_trustees_page,
            "email_on_about_festival_page": email_on_about_festival_page,
            "email_on_acceptance_of_plays_page": email_on_acceptance_of_plays_page,
            "email_on_author_page": email_on_author_page,
        }
        serializer = EmailsSerializer(data)
        return Response(serializer.data)
