from django.db import models

from apps.core.models import BaseModel
from apps.library.models import Author
from apps.postfix.validators import VirtualNameValidator


class Virtual(BaseModel):
    enabled = models.BooleanField(verbose_name="включено", default=True)
    author = models.OneToOneField(
        Author,
        verbose_name="автор",
        on_delete=models.CASCADE,
        related_name="virtual_email",
        null=True,
        blank=True,
    )
    mailbox = models.CharField(
        verbose_name="почтовый ящик",
        unique=True,
        max_length=64,
        help_text="имя почтового ящика до знака @",
        validators=(VirtualNameValidator(),),
    )

    class Meta:
        verbose_name = "виртуальный адрес"
        verbose_name_plural = "виртуальные адреса"

    def __str__(self):
        return self.mailbox


class Recipient(BaseModel):
    email = models.EmailField(verbose_name="получатель")
    virtual = models.ForeignKey(Virtual, on_delete=models.CASCADE, related_name="recipients")

    class Meta:
        verbose_name = "адрес назначения"
        verbose_name_plural = "адреса назначения"

    def __str__(self):
        return self.email
