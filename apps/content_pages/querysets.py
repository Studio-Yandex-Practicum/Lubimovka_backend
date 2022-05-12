from django.db import models
from django.shortcuts import get_object_or_404

from apps.core.constants import Status


class PublishedContentQuerySet(models.QuerySet):
    def published(self):
        """Return only published objects."""
        qs = self.filter(status=Status.PUBLISHED)
        return qs

    def preview(self, id):
        """Return unpublished object."""
        obj = get_object_or_404(self, id=id)
        return obj
