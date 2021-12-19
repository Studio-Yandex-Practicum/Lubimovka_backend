from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.response import Response
from xhtml2pdf import pisa

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


def get_pdf_response(press_release_instance, path_to_font):
    press_release_year = press_release_instance.festival.year
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename='press-release_{press_release_year}.pdf'"
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
        return Response("Пожалуйста, попробуйте повторить попытку позже", status_code=status.HTTP_400_BAD_REQUEST)
    return response
