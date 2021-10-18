from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
        "SUBJECT",
        html_message,
        to=[
            settings.EMAIL_SEND_TO,
        ],
    )
    message.content_subtype = "html"
    message.send()
