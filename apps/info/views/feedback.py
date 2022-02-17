from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Person, Setting
from apps.info.serializers import FeedbackSerializer


class FeedbackAPIView(APIView):
    @extend_schema(request=None, responses=FeedbackSerializer)
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
        photo_gallery_facebook = Setting.get_setting("photo_gallery_facebook")
        pr_manager_name = Setting.get_setting("pr_manager_name")
        pr_manager_avatar_email = (
            Person.objects.filter(festivalteam__is_pr_manager=True).values("image", "email").first()
        )
        data = {
            "email_on_project_page": email_on_project_page,
            "email_on_what_we_do_page": email_on_what_we_do_page,
            "email_on_trustees_page": email_on_trustees_page,
            "email_on_about_festival_page": email_on_about_festival_page,
            "email_on_acceptance_of_plays_page": email_on_acceptance_of_plays_page,
            "email_on_author_page": email_on_author_page,
            "photo_gallery_facebook": photo_gallery_facebook,
            "pr_manager_name": pr_manager_name,
            "pr_manager_avatar_email": pr_manager_avatar_email,
        }
        serializer = FeedbackSerializer(data)
        return Response(serializer.data)
