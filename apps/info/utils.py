from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

EMAIL_SUBJECT_PREFIX = settings.EMAIL_SUBJECT_PREFIX
SEND_FROM_QUESTION_EMAIL = settings.SEND_FROM_QUESTION_EMAIL
SEND_TO_QUESTION_EMAIL = settings.SEND_TO_QUESTION_EMAIL


def send_question(serializer):
    html_message = render_to_string(
        "email.html",
        {
            "question": serializer.validated_data["question"],
            "author_name": serializer.validated_data["author_name"],
            "author_email": serializer.validated_data["author_email"],
        },
    )
    message = EmailMessage(
        subject=EMAIL_SUBJECT_PREFIX,
        from_email=SEND_FROM_QUESTION_EMAIL,
        body=html_message,
        to=(SEND_TO_QUESTION_EMAIL,),
    )
    message.content_subtype = "html"
    message.send()
