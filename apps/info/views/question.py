from rest_framework.permissions import AllowAny
from rest_framework.viewsets import generics

from apps.info.serializers.question import QuestionSerializer
from apps.info.utils import send_question


class QuestionCreateAPI(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        send_question(serializer)
