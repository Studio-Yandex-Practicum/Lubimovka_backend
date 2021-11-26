from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.articles.models import NewsItem
from apps.articles.serializers.news_items import NewsItemsSerializer
from apps.content_pages.serializers.content_items import PerformancesSerializer
from apps.core.models import Settings
from apps.info.models import Partner, Place, Sponsor
from apps.info.serializers import PlaceSerializer
from apps.info.serializers.partners import PartnersSerializer
from apps.info.serializers.sponsors import SponsorsSerializer
from apps.library.models import Performance, ProgramType, Reading
from apps.library.serializers.program_type import ProgramTypeSerializer
from apps.library.serializers.reading import ReadingEventsSerializer


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
        global contex
        # Новости
        news_items = NewsItem.objects.order_by("-created")[:6]
        news_item_serializer = NewsItemsSerializer(news_items, many=True)
        # Спектакли
        performances = Performance.objects.order_by("-created")[:6]
        performances_serializer = PerformancesSerializer(
            performances, many=True
        )
        # Читки/Пьесы
        readings = Reading.objects.order_by("-created")[:6]
        readings_serializer = ReadingEventsSerializer(readings, many=True)
        # Партнеры
        partners = Partner.objects.all()
        partners_serializer = PartnersSerializer(partners, many=True)
        # Спонсоры
        sponsors = Sponsor.objects.all()
        sponsors_team_serializer = SponsorsSerializer(sponsors, many=True)
        # Площадки
        places = Place.objects.all()
        places_team_serializer = PlaceSerializer(places, many=True)
        # Шорт-лист
        program_type = ProgramType.objects.order_by("-created")[:4]
        program_type_serializer = ProgramTypeSerializer(
            program_type, many=True
        )

        # Конфигурации
        festival_status = Settings.get_setting("festival_status")
        if festival_status:
            contex = {
                "news_item": news_item_serializer.data,
                "readings": readings_serializer.data,
                "partners": partners_serializer.data,
                "sponsors": sponsors_team_serializer.data,
                "program_type": program_type_serializer.data,
            }
        contex = {
            "news_item": news_item_serializer.data,
            "readings": readings_serializer.data,
            "partners": partners_serializer.data,
            "sponsors": sponsors_team_serializer.data,
            "places": places_team_serializer.data,
            "performances": performances_serializer.data,
        }
        return Response({"contex": contex})
