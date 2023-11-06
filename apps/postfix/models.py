from django.db import models

from apps.core.models import BaseModel


class Virtual(BaseModel):
    enabled = models.BooleanField(verbose_name="включено", default=True)
    email = models.EmailField(verbose_name="виртуальный адрес")

    class Meta:
        verbose_name = "виртуальный адрес"
        verbose_name_plural = "виртуальные адреса"

    def __str__(self):
        return self.email


class Recipient(BaseModel):
    email = models.EmailField(verbose_name="получатель")
    virtual = models.ForeignKey(Virtual, on_delete=models.CASCADE, related_name="recipients")

    class Meta:
        verbose_name = "адрес назначения"
        verbose_name_plural = "адреса назначения"

    def __str__(self):
        return self.email
