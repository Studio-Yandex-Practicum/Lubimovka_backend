import urllib

from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify as django_slugify

from apps.core.constants import ALPHABET


def slugify(name):
    """Return "slug" formated string. It's an ordinary `django_slugify` with cyrillic support."""
    return django_slugify("".join(ALPHABET.get(char, char) for char in name.lower()))


def get_picsum_image(width: int = 1024, height: int = 768) -> ContentFile:
    """Return real image from picsum.photos. Supports width and height arguments."""
    image = urllib.request.urlopen(f"https://picsum.photos/{width}/{height}").read()
    return ContentFile(image)
