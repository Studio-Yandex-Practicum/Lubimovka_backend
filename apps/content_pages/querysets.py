from django.db import models


class ContenPageQuerySet(models.QuerySet):
    def published(self):
        """Returns only published objects."""
        qs = self.filter(is_draft=False)
        return qs
