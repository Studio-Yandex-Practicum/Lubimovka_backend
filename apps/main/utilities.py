import datetime

from apps.afisha.models import Event
from apps.articles.models import BlogItem, NewsItem
from apps.info.models import Festival, Place
from apps.library.models import ProgramType
from apps.main.models import Banner


class MainObject:
    def add_first_screen_data(self, title, url_title, url):
        self.first_screen_title = title
        self.first_screen_url_title = url_title
        self.first_screen_url = url

    def add_blog_data(self, title):
        self.blog_items = BlogItem.ext_objects.published()[:6]
        self.blog_title = title

    def add_news_data(self, title):
        self.news_items = NewsItem.ext_objects.published()[:6]
        self.news_title = title

    def add_afisha(self, main_show_afisha_only_for_today, title):
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
        self.event_title = title

    def add_banners(self, title):
        self.banner_items = Banner.objects.all()
        self.banner_title = title

    def add_short_list(self, title):
        program = ProgramType.objects.get(slug="short-list")
        festival = Festival.objects.all().order_by("-year").first()
        shot_list_plays = program.plays.filter(
            festival=festival, is_draft=False
        )[:6]
        self.short_list_items = shot_list_plays
        self.short_list_title = title

    def add_video_archive(self, url, photo):
        self.video_archive_url = url
        self.video_archive_photo = photo

    def add_places(self):
        self.place_items = Place.objects.all()
