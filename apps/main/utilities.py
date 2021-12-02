import datetime

from apps.afisha.models import Event
from apps.articles.models import BlogItem, NewsItem
from apps.core.models import Settings
from apps.info.models import Festival, Place
from apps.library.models import ProgramType
from apps.main.models import Banner


class MainObject:
    def add_first_screen_data(self):
        main_add_first_screen = Settings.get_setting("main_add_first_screen")
        if main_add_first_screen:
            self.first_screen_title = Settings.get_setting(
                "main_first_screen_title"
            )
            self.first_screen_url_title = Settings.get_setting(
                "main_first_screen_url_title"
            )
            self.first_screen_url = Settings.get_setting(
                "main_first_screen_url"
            )

    def add_blog_data(self):
        main_add_blog = Settings.get_setting("main_add_blog")
        if main_add_blog:
            self.blog_items = BlogItem.ext_objects.published()[:6]
            self.blog_title = Settings.get_setting("main_blog_title")

    def add_news_data(self):
        main_add_news = Settings.get_setting("main_add_news")
        if main_add_news:
            self.news_items = NewsItem.ext_objects.published()[:6]
            self.news_title = Settings.get_setting("main_news_title")

    def add_afisha(self):
        main_add_afisha = Settings.get_setting("main_add_afisha")
        if main_add_afisha:
            main_show_afisha_only_for_today = Settings.get_setting(
                "main_show_afisha_only_for_today"
            )
            if main_show_afisha_only_for_today:
                today = datetime.datetime.now().date()
                tomorrow = today + datetime.timedelta(days=1)
                event_items = Event.objects.filter(
                    date_time__range=(today, tomorrow),
                    pinned_on_main=True,
                )
            else:
                event_items = Event.objects.filter(pinned_on_main=True)[:6]
            self.event_items = event_items
            self.event_title = Settings.get_setting("main_afisha_title")

    def add_banners(self):
        main_add_banners = Settings.get_setting("main_add_banners")
        if main_add_banners:
            self.banner_items = Banner.objects.all()

    def add_short_list(self):
        main_add_short_list = Settings.get_setting("main_add_short_list")
        if main_add_short_list:
            program = ProgramType.objects.get(slug="short-list")
            festival = Festival.objects.all().order_by("-year").first()
            shot_list_plays = program.plays.filter(
                festival=festival, is_draft=False
            )[:6]
            self.short_list_items = shot_list_plays
            self.short_list_title = Settings.get_setting(
                "main_short_list_title"
            )

    def add_video_archive(self):
        main_add_video_archive = Settings.get_setting("main_add_video_archive")
        if main_add_video_archive:
            self.video_archive_url = Settings.get_setting(
                "main_video_archive_url"
            )
            self.video_archive_photo = Settings.get_setting(
                "main_video_archive_photo"
            )

    def add_places(self):
        main_add_places = Settings.get_setting("main_add_places")
        if main_add_places:
            self.place_items = Place.objects.all()
