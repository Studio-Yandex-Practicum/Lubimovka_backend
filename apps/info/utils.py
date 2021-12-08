from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.core.models import Setting


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
        Setting.get_setting("email_subject_for_question"),
        html_message,
        to=[
            Setting.get_setting("mail_send_to"),
        ],
    )
    message.content_subtype = "html"
    message.send()
