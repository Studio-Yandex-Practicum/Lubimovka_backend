from django.db import models

from apps.core.models import BaseModel
from apps.library.models import Author


class Virtual(BaseModel):
    enabled = models.BooleanField(verbose_name="включено", default=True)
    author = models.ForeignKey(Author, verbose_name="автор", on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(verbose_name="виртуальный адрес", unique=True)

    class Meta:
        verbose_name = "виртуальный адрес"
        verbose_name_plural = "виртуальные адреса"

    def __str__(self):
        return self.email


class VirtualAuthor(Virtual):
    class Meta:
        proxy = True
        verbose_name = "адрес для автора"
        verbose_name_plural = "адреса для авторов"

    def slug(self):
        return self.author.slug


class Recipient(BaseModel):
    email = models.EmailField(verbose_name="получатель")
    virtual = models.ForeignKey(Virtual, on_delete=models.CASCADE, related_name="recipients")

    class Meta:
        verbose_name = "адрес назначения"
        verbose_name_plural = "адреса назначения"

    def __str__(self):
        return self.email
