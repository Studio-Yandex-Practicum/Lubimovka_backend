from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import generics

from apps.info.serializers import QuestionSerializer


class QuestionCreate(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        html_content = render_to_string(
            "email.html", {"text": serializer.validated_data["question"]}
        )
        message = EmailMultiAlternatives(
            to=["sova408@mail.ru"],
        )
        message.attach_alternative(html_content, "text/html")
        print("Отправлено")
