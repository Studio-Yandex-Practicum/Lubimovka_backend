from django.db.models.functions import Substr

from apps.library.models import Author
from apps.library.utilities import filter_letter_values


def author_first_letter():
    """Return a list of the first letters of surnames and names of authors."""
    authors_firstname_list = Author.objects.annotate(letter=Substr("person__first_name", pos=1, length=1)).values(
        "letter"
    )
    authors_lastname_list = Author.objects.annotate(letter=Substr("person__last_name", pos=1, length=1)).values(
        "letter"
    )
    first_letters = [*authors_firstname_list, *authors_lastname_list]
    letters = filter_letter_values(first_letters)
    return letters
