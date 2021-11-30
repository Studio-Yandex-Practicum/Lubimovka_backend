from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Settings
from apps.main.serializers import MainSerializer
from apps.main.utilities import MainObject


class MainView(APIView):
    @extend_schema(responses=MainSerializer)
    def get(self, request):
        main = MainObject()
        main_add_blog = Settings.get_setting("main_add_blog")
        main_add_news = Settings.get_setting("main_add_news")
        main_add_afisha = Settings.get_setting("main_add_afisha")
        main_show_afisha_only_for_today = Settings.get_setting(
            "main_show_afisha_only_for_today"
        )
        main_add_banners = Settings.get_setting("main_add_banners")
        main_add_short_list = Settings.get_setting("main_add_short_list")
        main_add_video_archive = Settings.get_setting("main_add_video_archive")
        main_add_places = Settings.get_setting("main_add_places")
        # Add diary (blog) to context
        if main_add_blog:
            title = Settings.get_setting("main_blog_title")
            main.add_blog_data(title=title)
        # Add news to context
        if main_add_news:
            title = Settings.get_setting("main_news_title")
            main.add_news_data(title=title)
        # # Add afisha to context
        if main_add_afisha:
            title = Settings.get_setting("main_afisha_title")
            main.add_afisha(main_show_afisha_only_for_today, title=title)
        # Add banners to context
        if main_add_banners:
            title = Settings.get_setting("main_banners_title")
            main.add_banners(title=title)
        # # Add short-list to context
        if main_add_short_list:
            title = Settings.get_setting("main_short_list_title")
            main.add_short_list(title=title)
        # Add video-archive to context
        if main_add_video_archive:
            url = Settings.get_setting("main_video_archive_url")
            photo = Settings.get_setting("main_video_archive_photo")
            main.add_video_archive(
                url=url,
                photo=photo,
            )
        # Add places to context
        if main_add_places:
            main.add_places()

        # Common access to context. It's required to return correct url links
        context = {
            "request": self.request,
        }
        main_serializer = MainSerializer(main, context=context)
        return Response(main_serializer.data)
