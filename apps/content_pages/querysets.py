from django.db import models
from django.db.models import Q


class ContenPageQuerySet(models.QuerySet):
    def published(self):
        """Return only published objects."""
        qs = self.filter(status="PUBLISHED")
        return qs

    def current_and_published(self, object_id):
        """Return only published and current objects."""
        qs = self.filter(Q(status="PUBLISHED") | Q(id=object_id))
        return qs
