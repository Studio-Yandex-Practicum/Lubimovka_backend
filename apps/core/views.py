from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.articles.models import NewsItem
from apps.articles.serializers import NewsItemSerializer
from apps.content_pages.serializers import PerformanceSerializer
from apps.core.models import Settings
from apps.info.models import FestivalTeam, Partner, Place, Sponsor
from apps.info.serializers import (
    FestivalTeamsSerializer,
    PartnerSerializer,
    PlaceSerializer,
    SponsorSerializer,
)
from apps.library.models import Performance, Reading
from apps.library.serializers import ReadingEventSerializer


def error500(request, *args, **kwargs):
    """
    Generic 500 error handler.
    """
    data = {"error": "ServerError", "message": "Ошибка на сервере"}
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def error400(request, exception, *args, **kwargs):
    """
    Generic 400 error handler.
    """
    data = {"error": "BadRequest", "message": "Запрос не может быть обработан"}
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def error404(request, exception, *args, **kwargs):
    """
    Generic 404 error handler.
    """
    data = {"error": "Http404", "message": "Запрошенный ресурс не найден"}
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


class MainView(APIView):
    def get(self, request):
        # Новости
        news_item = NewsItem.objects.order_by("-created")[:6]
        news_item_serializer = NewsItemSerializer(news_item, many=True)
        # Спектакли
        performances = Performance.objects.order_by("-created")[:6]
        performances_serializer = PerformanceSerializer(
            performances, many=True
        )
        # Читки
        readings = Reading.objects.order_by("-created")[:6]
        readings_serializer = ReadingEventSerializer(readings, many=True)
        # Партнеры
        partners = Partner.objects.all()
        partners_serializer = PartnerSerializer(partners, many=True)
        # Команда фестиваля
        festival_team = FestivalTeam.objects.all()
        festival_team_serializer = FestivalTeamsSerializer(
            festival_team, many=True
        )
        # Спонсоры
        sponsors = Sponsor.objects.all()
        sponsors_team_serializer = SponsorSerializer(sponsors, many=True)
        # Площадки
        places = Place.objects.all()
        places_team_serializer = PlaceSerializer(places, many=True)

        # Конфигурации
        settings = Settings.objects.first()

        if settings.boolean:
            contex = {
                "news_item": news_item_serializer.data,
                "readings": readings_serializer.data,
                "partners": partners_serializer.data,
                "festival_team": festival_team_serializer.data,
                "sponsors": sponsors_team_serializer.data,
            }
        else:
            contex = {
                "news_item": news_item_serializer.data,
                "performances": performances_serializer.data,
                "partners": partners_serializer.data,
                "festival_team": festival_team_serializer.data,
                "sponsors": sponsors_team_serializer.data,
                "places": places_team_serializer.data,
            }

        return Response({"contex": contex})
