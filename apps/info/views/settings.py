from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Person, Setting
from apps.info.serializers import SettingsSerializer


class SettingsAPIView(APIView):
    @extend_schema(request=None, responses=SettingsSerializer)
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
        photo_gallery_facebook_link = Setting.get_setting("photo_gallery_facebook")
        pr_manager_name = Setting.get_setting("pr_manager_name")
        pr_manager = Person.objects.filter(festivalteammember__is_pr_manager=True).first()
        plays_reception_is_open = Setting.get_setting("plays_reception_is_open")
        data = {
            "email_on_project_page": email_on_project_page,
            "email_on_what_we_do_page": email_on_what_we_do_page,
            "email_on_trustees_page": email_on_trustees_page,
            "email_on_about_festival_page": email_on_about_festival_page,
            "email_on_acceptance_of_plays_page": email_on_acceptance_of_plays_page,
            "email_on_author_page": email_on_author_page,
            "for_press": {
                "pr_manager": {
                    "pr_manager_name": pr_manager_name,
                    "pr_manager_email": pr_manager.email,
                    "pr_manager_photo_link": pr_manager.image,
                },
                "photo_gallery_facebook_link": photo_gallery_facebook_link,
            },
            "plays_reception_is_open": plays_reception_is_open,
        }
        serializer = SettingsSerializer(data, context={"request": self.request})
        return Response(serializer.data)
