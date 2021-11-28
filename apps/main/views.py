import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.afisha.models import Event
from apps.articles.models import BlogItem, NewsItem
from apps.core.models import Settings
from apps.info.models import Festival, Place
from apps.library.models import ProgramType
from apps.main.models import Banner
from apps.main.serializers import (
    BannerSerializer,
    EventItemsForMainSerializer,
    MainBlogItemsForMainSerializer,
    NewsItemsForMainSerializer,
    PlaceForMainSerializer,
    PlayForMainSerializer,
)


class MainView(APIView):
    def get(self, request):
        context = {}
        main_add_blog = Settings.get_setting("main_add_blog")
        main_add_news = Settings.get_setting("main_add_news")
        main_add_affiche = Settings.get_setting("main_add_affiche")
        main_show_affiche_only_for_today = Settings.get_setting(
            "main_show_affiche_only_for_today"
        )
        main_add_banner = Settings.get_setting("main_add_banner")
        main_add_short_list = Settings.get_setting("main_add_short_list")
        main_add_video_archive = Settings.get_setting("main_add_video_archive")
        main_add_places = Settings.get_setting("main_add_places")
        # Дневник (блог)
        if main_add_blog:
            blog_items = BlogItem.objects.order_by("-created")[:6]
            blog_item_serializer = MainBlogItemsForMainSerializer(
                blog_items, many=True
            )
            context["blog_item"] = blog_item_serializer.data
            context["blog_title"] = Settings.get_setting("main_blog_title")
        # Новости
        if main_add_news:
            news_items = NewsItem.objects.order_by("-pub_date")[:6]
            news_item_serializer = NewsItemsForMainSerializer(
                news_items, many=True
            )
            context["news_item"] = news_item_serializer.data
            context["news_title"] = Settings.get_setting("main_news_title")
        # Афиша
        if main_add_affiche:
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
            context["event_items"] = event_item_serializer.data
            context["event_title"] = Settings.get_setting("main_affiche_title")
        # Баннеры
        if main_add_banner:
            banners_items = Banner.objects.all()
            banners_item_serializer = BannerSerializer(
                banners_items, many=True
            )
            context["banners_item"] = banners_item_serializer.data
            context["banners_title"] = Settings.get_setting(
                "main_banner_title"
            )
        # Шорт-лист
        if main_add_short_list:
            program = ProgramType.objects.get(name="Шорт-лист")
            festival = Festival.objects.all().order_by("-year").first()
            plays_items = program.plays.filter(
                festival=festival, is_draft=False
            )[:6]
            plays_item_serializer = PlayForMainSerializer(
                plays_items, many=True
            )
            context["short_list"] = plays_item_serializer.data
            context["short_list_title"] = Settings.get_setting(
                "main_short_list_title"
            )
        # Видео архив
        if main_add_video_archive:
            context["main_video_archive_url"] = Settings.get_setting(
                "main_video_archive_url"
            )
            context["main_video_archive_photo"] = Settings.get_setting(
                "main_video_archive_photo"
            )
        # Площадки
        if main_add_places:
            places = Place.objects.all()
            places_team_serializer = PlaceForMainSerializer(places, many=True)
            context["places_team_serializer"] = places_team_serializer.data

        return Response({"context": context})
