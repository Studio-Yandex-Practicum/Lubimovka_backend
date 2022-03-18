from anymail.exceptions import AnymailConfigurationError, AnymailInvalidAddress, AnymailRequestsAPIError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import generics

from apps.info.schema.schema_extension import ERROR_MESSAGES_FOR_QUESTION_FOR_400
from apps.info.serializers.question import QuestionSerializer
from apps.info.utils import send_question


@extend_schema(
    responses={
        201: QuestionSerializer,
        400: ERROR_MESSAGES_FOR_QUESTION_FOR_400,
    }
)
class QuestionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            response = send_question(serializer)
            if (
                hasattr(response, "anymail_status")
                and response.anymail_status.esp_response.status_code == status.HTTP_200_OK
            ):
                instance.sent = True
                instance.save()
        except AnymailConfigurationError:
            raise ValidationError("Неверные настройки Mailjet.")
        except (AnymailRequestsAPIError, AnymailInvalidAddress):
            raise ValidationError("Не указан адрес электронной почты отправителя.")
        except ValueError:
            raise ValidationError("Неверный ID шаблона Mailjet.")
