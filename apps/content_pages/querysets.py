from django.db import models

from apps.core.constants import Status


class PublishedContentQuerySet(models.QuerySet):
    def published(self):
        """Return only published objects."""
        qs = self.filter(status=Status.PUBLISHED)
        return qs
