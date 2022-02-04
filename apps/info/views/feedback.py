from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Setting
from apps.info.serializers import FeedbackSerializer


class FeedbackAPIView(APIView):
    def get(self, request):
        """Get all required emails that can be changed.

        except email on contacts page
        """
        email_on_project_page = Setting.get_setting("email_on_project_page")
        email_on_what_we_do_page = Setting.get_setting("email_on_what_we_do_page")
        email_on_trustees_page = Setting.get_setting("email_on_trustees_page")
        email_on_about_festival_page = Setting.get_setting("email_on_about_festival_page")
        email_on_acceptance_of_plays_page = Setting.get_setting("email_on_acceptance_of_plays_page")
        email_on_author_page = Setting.get_setting("email_on_author_page")
        data = {
            "email_on_project_page": email_on_project_page,
            "email_on_what_we_do_page": email_on_what_we_do_page,
            "email_on_trustees_page": email_on_trustees_page,
            "email_on_about_festival_page": email_on_about_festival_page,
            "email_on_acceptance_of_plays_page": email_on_acceptance_of_plays_page,
            "email_on_author_page": email_on_author_page,
        }
        serializer = FeedbackSerializer(data)
        return Response(serializer.data)
