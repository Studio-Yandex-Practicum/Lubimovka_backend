from django.template.defaultfilters import slugify as django_slugify

from apps.core.constants import ALPHABET, RUSSIAN_MONTHS


def slugify(name):
    return django_slugify("".join(ALPHABET.get(char, char) for char in name.lower()))


def get_russian_date(date):
    """Return the date in string form in Russian.

    example: "5 мая".
    """
    day = date.day
    month = RUSSIAN_MONTHS.get(date.month)
    return f"{day} {month}"
