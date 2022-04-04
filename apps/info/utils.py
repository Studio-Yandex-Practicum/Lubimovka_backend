from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.response import Response
from xhtml2pdf import pisa

from apps.core.models import Setting
from config.settings.base import MAILJET_TEMPLATE_ID_QUESTION


def send_question(instance):
    """Transmit question parameters in the template.

    For more information please read the documentation:
    https://anymail.readthedocs.io/en/stable/esps/mailjet//
    """
    message = EmailMessage(
        subject=Setting.get_setting("email_subject_for_question"),
        from_email=Setting.get_setting("email_send_from"),
        to=(Setting.get_setting("email_send_to"),),
    )

    message.template_id = MAILJET_TEMPLATE_ID_QUESTION
    message.merge_global_data = {
        "question": instance.question,
        "author_name": instance.author_name,
        "author_email": instance.author_email,
    }
    message.send()

    if hasattr(message, "anymail_status") and message.anymail_status.esp_response.status_code == status.HTTP_200_OK:
        return True
    return False


def get_pdf_response(press_release_instance, path_to_font):
    press_release_year = press_release_instance.festival.year
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=press-release_{press_release_year}.pdf"
    template = get_template("press_release.html")
    content = template.render(
        {
            "press_release": press_release_instance,
            "path_to_font": path_to_font,
        }
    )
    pisa_status = pisa.CreatePDF(
        content,
        dest=response,
        encoding="UTF-8",
    )
    if pisa_status.err:
        return Response(
            "Пожалуйста, попробуйте повторить попытку позже",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return response
