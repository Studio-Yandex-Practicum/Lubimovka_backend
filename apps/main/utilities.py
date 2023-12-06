from datetime import timedelta

from django.conf import settings
from django.db.models import DateTimeField, ExpressionWrapper, Q
from django.db.models.functions import Now, TruncDay, TruncSecond
from django.utils import timezone

from apps.afisha.models import Event
from apps.articles.models import BlogItem, NewsItem
from apps.core.constants import Status
from apps.core.models import Setting
from apps.info.models import Festival, Place
from apps.library.models import Play, ProgramType
from apps.main.models import Banner


class MainObject:
    def __init__(self) -> None:
        setting_keys = (
            "main_add_first_screen",
            "main_first_screen_title",
            "main_first_screen_url_title",
            "main_first_screen_url",
            "main_first_screen_image",
            "main_add_blog",
            "main_blog_title",
            "main_add_news",
            "main_news_title",
            "main_add_afisha",
            "main_show_afisha_only_for_today",
            "afisha_description",
            "main_add_banners",
            "main_add_short_list",
            "main_short_list_title",
            "main_add_video_archive",
            "main_video_archive_url",
            "main_video_archive_photo",
            "main_add_places",
            "show_general_partners",
            "show_info_partners_and_festival_partners",
            "festival_status",
        )
        self.settings = Setting.get_settings(settings_keys=setting_keys)

    def add_first_screen_data(self):
        main_add_first_screen = self.settings.get("main_add_first_screen")
        if main_add_first_screen:
            title = self.settings.get("main_first_screen_title")
            url_title = self.settings.get("main_first_screen_url_title")
            url = self.settings.get("main_first_screen_url")
            image = self.settings.get("main_first_screen_image")
            self.first_screen = {
                "title": title,
                "url_title": url_title,
                "url": url,
                "image": image,
            }

    def add_blog_data(self):
        main_add_blog = self.settings.get("main_add_blog")
        if main_add_blog:
            title = self.settings.get("main_blog_title")
            items = BlogItem.objects.published()[:6]
            self.blog = {
                "title": title,
                "items": items,
            }

    def add_news_data(self):
        main_add_news = self.settings.get("main_add_news")
        if main_add_news:
            title = self.settings.get("main_news_title")
            items = NewsItem.objects.published()[:6]
            self.news = {
                "title": title,
                "items": items,
            }

    def add_afisha(self):
        main_add_afisha = self.settings.get("main_add_afisha")
        if main_add_afisha:
            main_show_afisha_only_for_today = self.settings.get("main_show_afisha_only_for_today")

            if main_show_afisha_only_for_today:
                today = timezone.now()
                tomorrow = today.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                items = (
                    Event.objects.filter(date_time__range=(today, tomorrow), hidden_on_main=False)
                    .filter(
                        Q(common_event__custom__name__isnull=False)
                        | Q(common_event__performance__status=Status.PUBLISHED)
                    )
                    .order_by("date_time")
                )
            else:
                items = (
                    Event.objects.filter(date_time__gte=timezone.now())
                    .filter(hidden_on_main=False)
                    .filter(
                        Q(common_event__custom__name__isnull=False)
                        | Q(common_event__performance__status=Status.PUBLISHED)
                    )
                    .order_by("date_time")[:6]
                )

            description = self.settings.get("afisha_description")

            self.afisha = {
                "afisha_today": main_show_afisha_only_for_today,
                "description": description,
                "items": items.annotate(
                    opening_date_time=ExpressionWrapper(
                        TruncDay(
                            "date_time",
                        )
                        - timedelta(hours=settings.AFISHA_REGISTRATION_OPENS_HOURS_BEFORE),
                        output_field=DateTimeField(),
                    )
                )
                # TruncDay functions produces DateTime without timezone when wrapped with ExpressionWrapper;
                # to have Now without timezone as well, use TruncSecond here
                .annotate(now=ExpressionWrapper(TruncSecond(Now()), output_field=DateTimeField())),
            }

    def add_banners(self):
        main_add_banners = self.settings.get("main_add_banners")
        if main_add_banners:
            items = Banner.objects.all()
            self.banners = {"items": items}

    def add_short_list(self):
        main_add_short_list = self.settings.get("main_add_short_list")
        if main_add_short_list:
            program = ProgramType.objects.get(slug="short-list")
            festival = Festival.objects.all().order_by("-year").first()
            items = Play.objects.filter(
                programs=program,
                festival=festival,
                published=True,
            ).order_by("?")

            title = self.settings.get("main_short_list_title")
            self.short_list = {
                "title": title,
                "items": items,
            }

    def add_video_archive(self):
        main_add_video_archive = self.settings.get("main_add_video_archive")
        if main_add_video_archive:
            url = self.settings.get("main_video_archive_url")
            photo = self.settings.get("main_video_archive_photo")
            self.video_archive = {
                "url": url,
                "photo": photo,
            }

    def add_places(self):
        main_add_places = self.settings.get("main_add_places")
        if main_add_places:
            items = Place.objects.all()
            self.places = {"items": items}

    def show_partners(self):
        self.show_partners = {
            "show_general_partners": self.settings.get("show_general_partners"),
            "show_info_partners_and_festival_partners": self.settings.get("show_info_partners_and_festival_partners"),
        }
