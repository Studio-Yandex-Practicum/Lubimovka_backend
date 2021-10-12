from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import generics

from apps.info.models import Question
from apps.info.utils import send_question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionCreateAPI(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        send_question(serializer)
