import random
import unicodedata
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.response import Response
from xhtml2pdf import pisa


#  xhtml2pdf.readthedocs.io/en/latest/usage.html#using-xhtml2pdf-in-django
def link_callback(uri, rel):
    """Convert links.

    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    if uri.startswith(mUrl):
        path = Path(mRoot).joinpath(Path(uri.replace(mUrl, "")))
    elif uri.startswith(sUrl):
        path = Path(sRoot).joinpath(Path(uri.replace(sUrl, "")))
    else:
        return uri

    # make sure that file exists
    if not path.is_file():
        raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
    return str(path)


def get_pdf_response(press_release_instance):
    press_release_year = press_release_instance.festival.year
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=press-release_{press_release_year}.pdf"
    template = get_template("press_release.html")
    style_file = Path(settings.STATIC_ROOT).joinpath("core/ckeditor/press-release-styles.css")
    with style_file.open() as file:
        styles = file.read()
    content = template.render(
        {
            "text": unicodedata.normalize("NFC", press_release_instance.text),
            "styles": styles,
        }
    )
    pisa_status = pisa.CreatePDF(content, dest=response, encoding="UTF-8", link_callback=link_callback)
    if pisa_status.err:
        return Response(
            "Пожалуйста, попробуйте повторить попытку позже",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return response


def get_random_objects_by_queryset(queryset, number=None):
    items = list(queryset)
    length = len(items)
    if length == 0:
        return None
    if number is not None:
        if number > length:
            number = length
        return random.sample(items, number)
    return random.choice(items)


def get_random_objects_by_model(model, number=None):
    queryset = model.objects.all()
    return get_random_objects_by_queryset(queryset, number)
