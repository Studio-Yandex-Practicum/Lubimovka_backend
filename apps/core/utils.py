import urllib

from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify as django_slugify

from apps.core.constants import ALPHABET, RUSSIAN_MONTHS


def slugify(name):
    """Return "slug" formated string. It's an ordinary `django_slugify` with cyrillic support."""
    return django_slugify("".join(ALPHABET.get(char, char) for char in name.lower()))


def get_russian_date(date):
    """Return the date as a string in Russian format. Example: "5 мая"."""
    day = date.day
    month = RUSSIAN_MONTHS.get(date.month)
    return f"{day} {month}"


def get_picsum_image(width: int = 1024, height: int = 768) -> ContentFile:
    """Return real image from picsum.photos. Supports width and height arguments."""
    image = urllib.request.urlopen(f"https://picsum.photos/{width}/{height}").read()
    return ContentFile(image)
