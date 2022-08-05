from django.conf import settings
from django.core.mail import EmailMessage

from apps.core.models import Setting
from apps.core.utils import send_email


def send_question(instance):
    """Transmit question parameters in the template.

    For more information please read the documentation:
    https://anymail.readthedocs.io/en/stable/esps/mailjet//
    """
    settings_keys = (
        "email_subject_for_question",
        "email_send_from",
        "email_send_to",
    )
    email_settings = Setting.get_settings(settings_keys=settings_keys)

    message = EmailMessage(
        subject=email_settings.get("email_subject_for_question"),
        from_email=email_settings.get("email_send_from"),
        to=(email_settings.get("email_send_to"),),
    )

    message.template_id = settings.MAILJET_TEMPLATE_ID_QUESTION
    message.merge_global_data = {
        "question": instance.question,
        "author_name": instance.author_name,
        "author_email": instance.author_email,
    }

    return send_email(message)
