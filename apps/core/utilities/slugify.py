from django.template.defaultfilters import slugify as django_slugify

from apps.core.utilities.constants import ALPHABET


def slugify(name):
    return django_slugify(
        "".join(ALPHABET.get(char, char) for char in name.lower())
    )
