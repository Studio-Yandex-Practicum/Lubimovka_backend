from django.core.mail import EmailMessage

from apps.core.models import Setting


def send_question(serializer):
    """Transmit question parameters in the template.

    For more information please read the documentation:
    https://anymail.readthedocs.io/en/stable/esps/mailjet//
    """
    message = EmailMessage(
        subject=Setting.get_setting("email_subject_for_question"),
        from_email=Setting.get_setting("email_send_from"),
        to=(Setting.get_setting("email_send_to"),),
    )

    message.template_id = Setting.get_setting("email_question_template_id")
    message.merge_global_data = {
        "question": serializer.validated_data["question"],
        "author_name": serializer.validated_data["author_name"],
        "author_email": serializer.validated_data["author_email"],
    }
    message.send()
