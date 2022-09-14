from django.db.models.functions import Left

from apps.library.models import Author
from apps.library.utilities import filter_letter_values


def author_first_letter():
    """Return a list of the first letters of surnames and names of authors."""
    authors_lastname_list = Author.objects.annotate(letter=Left("person__last_name", 1)).values_list(
        "letter", flat=True
    )

    letters = filter_letter_values(authors_lastname_list)
    return letters
