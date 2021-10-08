from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import generics

from apps.info.serializers import QuestionSerializer
from apps.main.models import MainSettings


class QuestionCreate(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        html_message = render_to_string(
            "email.html",
            {
                "question": serializer.validated_data["question"],
                "name": serializer.validated_data["name"],
                "email": serializer.validated_data["email"],
            },
        )
        settings = MainSettings.objects.first()
        message = EmailMessage(
            "SUBJECT",
            html_message,
            to=[
                person.email
                for person in settings.persons_how_get_questions.all()
            ],
        )
        message.content_subtype = "html"
        message.send()
