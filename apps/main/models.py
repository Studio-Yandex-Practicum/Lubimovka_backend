# from django.db import models

from apps.core.models import BaseModel


class MainPage(BaseModel):
    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"
