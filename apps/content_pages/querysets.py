from django.db import models


class ContenPageQuerySet(models.QuerySet):
    def published(self):
        """Return only published objects."""
        qs = self.filter(status="published")
        return qs
