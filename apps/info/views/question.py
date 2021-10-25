from rest_framework.viewsets import generics

from apps.info.serializers.question import QuestionSerializer
from apps.info.utils import send_question


class QuestionCreateAPI(generics.CreateAPIView):
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save()
        send_question(serializer)
