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
        self.context["blog_item"] = blog_item_serializer.data

    def add_news_items(self):
        news_items = NewsItem.ext_objects.published().order_by("-pub_date")[:6]
        news_item_serializer = NewsItemForMainSerializer(news_items, many=True)
        self.context["news_item"] = news_item_serializer.data

    def add_affiche(self, main_show_affiche_only_for_today):
        if main_show_affiche_only_for_today:
            today = datetime.datetime.now().date()
            tomorrow = today + datetime.timedelta(days=1)
            event_items = Event.objects.filter(
                date_time__range=(today, tomorrow)
            )
            event_item_serializer = EventItemsForMainSerializer(
                event_items, many=True
            )
        else:
            event_items = Event.objects.all()[:6]
            event_item_serializer = EventItemsForMainSerializer(
                event_items, many=True
            )
        self.context["event_items"] = event_item_serializer.data

    def add_banner(self):
        banners_items = Banner.objects.all()
        banners_item_serializer = BannerSerializer(banners_items, many=True)
        self.context["banners_item"] = banners_item_serializer.data

    def add_short_list(self):
        program = ProgramType.objects.get(name="Шорт-лист")
        festival = Festival.objects.all().order_by("-year").first()
        plays_items = program.plays.filter(festival=festival, is_draft=False)[
            :6
        ]
        plays_item_serializer = PlayForMainSerializer(plays_items, many=True)
        self.context["short_list"] = plays_item_serializer.data

    def add_places(self):
        places = Place.objects.all()
        places_team_serializer = PlaceForMainSerializer(places, many=True)
        self.context["places_team_serializer"] = places_team_serializer.data
