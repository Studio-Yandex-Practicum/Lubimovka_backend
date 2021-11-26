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
from apps.library.models import Performance, Reading
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

        # Конфигурации
        settings = Settings.objects.all()
        count = 1
        for setting in settings:
            contex = {}
            if setting.festival_status:
                if setting.places:
                    contex.update(
                        {f"places_{count}": places_team_serializer.data}
                    )
            else:
                if setting.readings:
                    contex.update(
                        {f"readings_{count}": readings_serializer.data}
                    )
            if setting.news_item:
                contex.update(
                    {f"news_item_{count}": news_item_serializer.data}
                )
            if setting.performances:
                contex.update(
                    {f"performances_{count}": performances_serializer.data}
                )
            if setting.partners:
                contex.update({f"partners_{count}": partners_serializer.data})
            if setting.sponsors:
                contex.update(
                    {f"sponsors_{count}": sponsors_team_serializer.data}
                )
            count += 1
        return Response({"contex": contex})
