import logging
import threading

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.views import APIView

from apps.core.utils import get_domain
from apps.feedback.models import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION, ParticipationApplicationFestival
from apps.feedback.permissions import SettingsPlayReceptionPermission
from apps.feedback.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
from apps.feedback.services import ParticipationApplicationExport

logger = logging.getLogger("django")


class ParticipationViewSet(APIView):
    permission_classes = [SettingsPlayReceptionPermission]
    # Django REST Framework проверяет CSRF токен для всех запросов,
    # если включена аутентификация по сессии
    # https://www.django-rest-framework.org/topics/ajax-csrf-cors/#csrf-protection
    # Пока Frontend не научится прикреплять заголовок X-CSRFToken к этому запросу
    # аутентификацию для него придется отключить
    authentication_classes = []
    parser_classes = (FormParser, MultiPartParser)

    class ParticipationSerializer(serializers.ModelSerializer):
        year = serializers.IntegerField(
            min_value=1900,
            max_value=timezone.now().year,
            label="Год написания",
        )
        birth_year = serializers.IntegerField(
            min_value=1900,
            max_value=timezone.now().year,
            label="Год рождения",
        )
        url_file_in_storage = serializers.URLField(read_only=True)

        class Meta:
            model = ParticipationApplicationFestival
            exclude = ["verified", "festival_year"]
            extra_kwargs = {"file": {"required": True}}
            validators = [
                UniqueTogetherValidator(
                    queryset=ParticipationApplicationFestival.objects.all(),
                    fields=UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION,
                    message="Заявка уже была отправлена.",
                )
            ]

    @extend_schema(
        request=ParticipationSerializer,
        responses={
            201: None,
            400: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
            403: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
        },
    )
    def post(self, request):
        serializer = self.ParticipationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()
        file_link = get_domain(request) + str(instance.file.url)

        export = ParticipationApplicationExport()
        thread_for_services = threading.Thread(target=export.export_application, args=(instance, file_link))
        thread_for_services.start()
        return Response(status=status.HTTP_201_CREATED)
