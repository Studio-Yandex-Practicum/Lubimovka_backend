from datetime import date, timedelta

from apps.afisha.models import Event
from apps.articles.models import BlogItem, NewsItem
from apps.core.models import Settings
from apps.info.models import Festival, Place
from apps.library.models import Play, ProgramType
from apps.main.models import Banner


class MainObject:
    def add_first_screen_data(self):
        main_add_first_screen = Settings.get_setting("main_add_first_screen")
        if main_add_first_screen:
            title = Settings.get_setting("main_first_screen_title")
            url_title = Settings.get_setting("main_first_screen_url_title")
            url = Settings.get_setting("main_first_screen_url")
            self.first_screen = dict()
            self.first_screen["title"] = title
            self.first_screen["url_title"] = url_title
            self.first_screen["url"] = url

    def add_blog_data(self):
        main_add_blog = Settings.get_setting("main_add_blog")
        if main_add_blog:
            title = Settings.get_setting("main_blog_title")
            items = BlogItem.ext_objects.published()[:6]
            self.blog = dict()
            self.blog["title"] = title
            self.blog["items"] = items

    def add_news_data(self):
        main_add_news = Settings.get_setting("main_add_news")
        if main_add_news:
            title = Settings.get_setting("main_news_title")
            items = NewsItem.ext_objects.published()[:6]
            self.news = dict()
            self.news["title"] = title
            self.news["items"] = items

    def add_afisha(self):
        main_add_afisha = Settings.get_setting("main_add_afisha")
        if main_add_afisha:
            main_show_afisha_only_for_today = Settings.get_setting(
                "main_show_afisha_only_for_today"
            )
            if main_show_afisha_only_for_today:
                today = date.today()
                tomorrow = today + timedelta(days=1)
                items = Event.objects.filter(
                    date_time__range=(today, tomorrow),
                    pinned_on_main=True,
                )
            else:
                items = Event.objects.filter(pinned_on_main=True)[:6]
            title = Settings.get_setting("main_afisha_title")
            self.afisha = dict()
            self.afisha["title"] = title
            self.afisha["items"] = items

    def add_banners(self):
        main_add_banners = Settings.get_setting("main_add_banners")
        if main_add_banners:
            items = Banner.objects.all()
            self.banners = dict()
            self.banners["items"] = items

    def add_short_list(self):
        main_add_short_list = Settings.get_setting("main_add_short_list")
        if main_add_short_list:
            program = ProgramType.objects.get(slug="short-list")
            festival = Festival.objects.all().order_by("-year").first()
            short_list_plays = Play.objects.filter(
                program=program,
                festival=festival,
                is_draft=False,
            )
            title = Settings.get_setting("main_short_list_title")
            items = short_list_plays[:4]
            self.short_list = dict()
            self.short_list["title"] = title
            self.short_list["items"] = items

    def add_video_archive(self):
        main_add_video_archive = Settings.get_setting("main_add_video_archive")
        if main_add_video_archive:
            url = Settings.get_setting("main_video_archive_url")
            photo = Settings.get_setting("main_video_archive_photo")
            self.video_archive = dict()
            self.video_archive["url"] = url
            self.video_archive["photo"] = photo

    def add_places(self):
        main_add_places = Settings.get_setting("main_add_places")
        if main_add_places:
            items = Place.objects.all()
            self.places = dict()
            self.places["items"] = items
