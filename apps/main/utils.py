import datetime

from apps.afisha.models import Event
from apps.articles.models import BlogItem, NewsItem
from apps.info.models import Festival, Place
from apps.library.models import ProgramType
from apps.main.models import Banner
from apps.main.serializers import (
    BannerSerializer,
    BlogItemListForMainSerializer,
    EventItemsForMainSerializer,
    NewsItemForMainSerializer,
    PlaceForMainSerializer,
    PlayForMainSerializer,
)


class Context:
    def __init__(self):
        self.context = {}

    def add_setting(self, name, value):
        self.context[name] = value

    def add_blog_data(self):
        blog_items = BlogItem.ext_objects.published().order_by("-pub_date")[:6]
        blog_item_serializer = BlogItemListForMainSerializer(
            blog_items, many=True
        )
        self.context["blog_items"] = blog_item_serializer.data

    def add_news_items(self):
        news_items = NewsItem.ext_objects.published().order_by("-pub_date")[:6]
        news_item_serializer = NewsItemForMainSerializer(news_items, many=True)
        self.context["news_items"] = news_item_serializer.data

    def add_afisha(self, main_show_afisha_only_for_today):
        if main_show_afisha_only_for_today:
            today = datetime.datetime.now().date()
            tomorrow = today + datetime.timedelta(days=1)
            event_items = Event.objects.filter(
                date_time__range=(today, tomorrow),
                pinned_on_main=True,
            )
            event_item_serializer = EventItemsForMainSerializer(
                event_items, many=True
            )
        else:
            event_items = Event.objects.filter(pinned_on_main=True)[:6]
            event_item_serializer = EventItemsForMainSerializer(
                event_items, many=True
            )
        self.context["main_afisha_event_items"] = event_item_serializer.data

    def add_banners(self):
        banner_items = Banner.objects.all()
        banner_item_serializer = BannerSerializer(banner_items, many=True)
        self.context["banner_items"] = banner_item_serializer.data

    def add_short_list(self):
        program = ProgramType.objects.get(slug="short-list")
        festival = Festival.objects.all().order_by("-year").first()
        shot_list_plays = program.plays.filter(
            festival=festival, is_draft=False
        )[:6]
        shot_list_plays_serializer = PlayForMainSerializer(
            shot_list_plays, many=True
        )
        self.context["short_list"] = shot_list_plays_serializer.data

    def add_places(self):
        places = Place.objects.all()
        places_team_serializer = PlaceForMainSerializer(places, many=True)
        self.context["places"] = places_team_serializer.data
