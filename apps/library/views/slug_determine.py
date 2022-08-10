from django.shortcuts import redirect
from django.urls import reverse

from apps.library.models import Author


def slug_determine(request, identifier):
    authors_slug_list = Author.objects.all().values_list("slug", flat=True)

    if identifier in authors_slug_list:
        return redirect(reverse("authors-detail", kwargs={"slug": identifier}))
    return redirect(reverse("performance-detail", kwargs={"identifier": identifier}))
