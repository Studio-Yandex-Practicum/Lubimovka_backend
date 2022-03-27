from django.core.mail import EmailMessage
from rest_framework import status

from apps.core.models import Setting
from config.settings.base import MAILJET_TEMPLATE_ID_PLAY


def send_application_email(serializer):
    message = EmailMessage(
        subject="Подана заявка на участие",
        from_email=Setting.get_setting("email_send_from"),
        to=(Setting.get_setting("email_on_acceptance_of_plays_page"),),
    )
    message.template_id = MAILJET_TEMPLATE_ID_PLAY
    message.merge_global_data = {
        "year": serializer.validated_data["year"],
        "birth_year": serializer.validated_data["birth_year"],
        "first_name": serializer.validated_data["last_name"],
        "last_name": serializer.validated_data["last_name"],
        "city": serializer.validated_data["city"],
        "phone_number": serializer.validated_data["phone_number"],
        "email": serializer.validated_data["email"],
        "title": serializer.validated_data["title"],
    }

    # attach file
    filename = serializer.validated_data["file"].name
    data = serializer.validated_data["file"].open().read()
    content_type = serializer.validated_data["file"].content_type
    message.attach(filename, data, content_type)

    message.send()

    if hasattr(message, "anymail_status") and message.anymail_status.esp_response.status_code == status.HTTP_200_OK:
        return True
    return False
