from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.core.models import Settings
from apps.core.serializers import SettingsSerializer


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


@api_view(["GET"])
@permission_classes([AllowAny])
def get_setting(request):
    serializer = SettingsSerializer(data=request.data)
    if serializer.is_valid():
        settings = Settings.get_setting(request.data["settings"])
        return JsonResponse(settings, status=status.HTTP_200_OK)
