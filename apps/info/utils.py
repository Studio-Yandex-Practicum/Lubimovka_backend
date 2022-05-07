from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.response import Response
from xhtml2pdf import pisa

from apps.info.models import Festival


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


def get_vacant_and_current_festival(select):
    """Return QuerySet for select free festivals plus current festivals."""
    return Festival.objects.filter(Q(press_releases__festival__isnull=True) | Q(id=select))
