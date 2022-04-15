from anymail.exceptions import AnymailConfigurationError, AnymailInvalidAddress, AnymailRequestsAPIError
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info.models import Question
from apps.info.schema.schema_extension import ERROR_MESSAGES_FOR_QUESTION_FOR_400
from apps.info.utils import send_question


class QuestionCreateAPIView(APIView):
    """Create Question."""

    class QuestionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = "__all__"

    @extend_schema(
        responses={
            201: QuestionSerializer,
            400: ERROR_MESSAGES_FOR_QUESTION_FOR_400,
        }
    )
    def post(self, request):
        serializer = self.QuestionSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            try:
                response_success = send_question(instance)
                if response_success:
                    instance.sent = True
                    instance.save()
            except AnymailConfigurationError:
                raise ValidationError("Неверные настройки Mailjet.")
            except (AnymailRequestsAPIError, AnymailInvalidAddress):
                raise ValidationError("Не указан адрес электронной почты отправителя.")
            except ValueError:
                raise ValidationError("Неверный ID шаблона Mailjet.")
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
