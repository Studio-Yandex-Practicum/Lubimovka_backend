from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.settings.base import EMAIL_SEND_TO


def send_question(serializer):
    html_message = render_to_string(
        "email.html",
        {
            "question": serializer.validated_data["question"],
            "name": serializer.validated_data["name"],
            "email": serializer.validated_data["email"],
        },
    )
    message = EmailMessage(
        "SUBJECT",
        html_message,
        to=[
            EMAIL_SEND_TO,
        ],
    )
    message.content_subtype = "html"
    message.send()
