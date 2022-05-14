from django.conf import settings
from django.core.mail import EmailMessage

from apps.core.models import Setting
from apps.core.utils import send_email


def send_question(instance):
    """Transmit question parameters in the template.

    For more information please read the documentation:
    https://anymail.readthedocs.io/en/stable/esps/mailjet//
    """
    message = EmailMessage(
        subject=Setting.get_setting("email_subject_for_question"),
        from_email=Setting.get_setting("email_send_from"),
    )

    message.template_id = settings.MAILJET_TEMPLATE_ID_QUESTION
    message.merge_global_data = {
        "question": instance.question,
        "author_name": instance.author_name,
        "author_email": instance.author_email,
    }

    return send_email(message)
