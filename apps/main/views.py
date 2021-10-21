from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.main.models import MainSettings
from apps.main.serializers import SettingsSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def main_get_settings(request):
    serializer = SettingsSerializer(data=request.data)
    if serializer.is_valid():
        if len(request.data["settings"]) == 1:
            if request.data["settings"] in MainSettings.SettingsType.values:
                settings = MainSettings.get_settings_type(
                    request.data["settings"][0]
                )
            else:
                settings = MainSettings.get_setting(
                    request.data["settings"][0]
                )
            return JsonResponse(settings, status=status.HTTP_200_OK)
        else:
            settings = MainSettings.get_settings(request.data["settings"])
            return JsonResponse(settings, status=status.HTTP_200_OK)
