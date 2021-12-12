from django.conf import settings
from django.core.mail import EmailMessage

from apps.core.models import Settings

EMAIL_SUBJECT_PREFIX = settings.EMAIL_SUBJECT_PREFIX
SEND_FROM_QUESTION_EMAIL = settings.SEND_FROM_QUESTION_EMAIL
SEND_TO_QUESTION_EMAIL = settings.SEND_TO_QUESTION_EMAIL


def send_question(serializer):
    """This method transmits question parameters in the template.

    For more information please read the documentation:
    https://anymail.readthedocs.io/en/stable/esps/mailjet//
    """

    message = EmailMessage(
        subject=Settings.get_setting("email_subject_for_question"),
        from_email=Settings.get_setting("email_send_from"),
        to=Settings.get_setting("mail_send_to"),
    )

    message.template_id = (Settings.get_setting("email_subject_for_question"),)
    message.merge_global_data = {
        "question": serializer.validated_data["question"],
        "author_name": serializer.validated_data["author_name"],
        "author_email": serializer.validated_data["author_email"],
    }
    message.send()
