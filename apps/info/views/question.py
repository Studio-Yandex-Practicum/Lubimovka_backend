from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import generics

from apps.info.serializers.question import QuestionSerializer
from apps.info.utils import send_question
from apps.info.views.auto_documentation_info import (
    ERROR_MESSAGES_FOR_QUESTION_FOR_400,
)


@extend_schema(
    responses={
        201: QuestionSerializer,
        400: ERROR_MESSAGES_FOR_QUESTION_FOR_400,
    }
)
class QuestionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save()
        send_question(serializer)
