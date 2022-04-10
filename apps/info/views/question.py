from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import generics

from apps.core.models import Setting
from apps.core.utils import send_email
from apps.info.schema.schema_extension import ERROR_MESSAGES_FOR_QUESTION_FOR_400
from apps.info.serializers.question import QuestionSerializer


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
        from_email = Setting.get_setting("email_send_from")
        to_emails = (Setting.get_setting("email_to_send_questions"),)
        template_id = settings.MAILJET_TEMPLATE_ID_QUESTION
        context = {
            "question": instance.question,
            "author_name": instance.author_name,
            "author_email": instance.author_email,
        }
        response_success = send_email(from_email, to_emails, template_id, context)
        if response_success:
            instance.sent = True
            instance.save()
