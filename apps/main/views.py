from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Settings
from apps.main.utils import Context


class MainView(APIView):
    def get(self, request):
        context = Context()
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
            context.add_blog_data()
            context.add_setting(
                "blog_title", Settings.get_setting("main_blog_title")
            )
        # Add news to context
        if main_add_news:
            context.add_news_items()
            context.add_setting(
                "news_title", Settings.get_setting("main_news_title")
            )
        # Add afisha to context
        if main_add_afisha:
            context.add_afisha(main_show_afisha_only_for_today)
            context.add_setting(
                "main_afisha_title", Settings.get_setting("main_afisha_title")
            )
        # Add banners to context
        if main_add_banners:
            context.add_banners()
            context.add_setting(
                "banner_title", Settings.get_setting("main_banners_title")
            )
        # Add short-list to context
        if main_add_short_list:
            context.add_short_list()
            context.add_setting(
                "short_list_title",
                Settings.get_setting("main_short_list_title"),
            )
        # Add video-archive to context
        if main_add_video_archive:
            context.add_setting(
                "main_video_archive_url",
                Settings.get_setting("main_video_archive_url"),
            )
            context.add_setting(
                "main_video_archive_photo",
                Settings.get_setting("main_video_archive_photo").url,
            )
        # Add places to context
        if main_add_places:
            context.add_places()
        return Response({"context": context.context})
