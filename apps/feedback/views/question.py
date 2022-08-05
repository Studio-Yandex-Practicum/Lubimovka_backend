from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Setting
from apps.core.services.send_email import send_email
from apps.feedback.models import Question
from apps.feedback.schema.schema_extension import ERROR_MESSAGES_FOR_QUESTION_FOR_400


class QuestionCreateAPIView(APIView):
    """Create Question."""

    class QuestionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            exclude = ("sent_to_email",)

    @extend_schema(
        request=QuestionSerializer,
        responses={
            201: None,
            400: ERROR_MESSAGES_FOR_QUESTION_FOR_400,
        },
    )
    def post(self, request):
        settings_keys = (
            "email_send_from",
            "email_to_send_questions",
        )
        email_settings = Setting.get_settings(settings_keys=settings_keys)
        serializer = self.QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        from_email = email_settings.get("email_send_from")
        to_emails = (email_settings.get("email_to_send_questions"),)
        template_id = settings.MAILJET_TEMPLATE_ID_QUESTION
        context = {
            "question": instance.question,
            "author_name": instance.author_name,
            "author_email": instance.author_email,
        }

        response_success = send_email(from_email, to_emails, template_id, context)

        if response_success:
            instance.sent_to_email = True
            instance.save()
        return Response(status=status.HTTP_201_CREATED)
