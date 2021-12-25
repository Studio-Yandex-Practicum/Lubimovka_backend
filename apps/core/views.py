from django.http import JsonResponse
from rest_framework import status


def error500(request, *args, **kwargs):
    """Return generic 500 error handler."""
    data = {"error": "ServerError", "message": "Ошибка на сервере"}
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def error400(request, exception, *args, **kwargs):
    """Return generic 400 error handler."""
    data = {"error": "BadRequest", "message": "Запрос не может быть обработан"}
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def error404(request, exception, *args, **kwargs):
    """Return generic 404 error handler."""
    data = {"error": "Http404", "message": "Запрошенный ресурс не найден"}
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
