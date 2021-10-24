from django.http import Http404
from django.shortcuts import get_object_or_404


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports
    both Model && queryset. Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None
