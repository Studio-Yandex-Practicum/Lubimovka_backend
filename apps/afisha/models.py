from django.db import models

from apps.core.models import BaseModel


class BaseEvent(BaseModel):
    def __str__(self):
        if hasattr(self, "masterclasses"):
            return self.masterclasses.name
        elif hasattr(self, "readings"):
            return self.readings.name
        elif hasattr(self, "performances"):
            return self.performances.name
        else:
            return str(self.pk)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Базовое событие"
        verbose_name_plural = "Базовые события"


class Event(BaseModel):
    PERFORMANCE = "performance"
    MASTER_CLASS = "masterclass"
    READING = "reading"
    EVENT_TYPES = [
        (PERFORMANCE, "Спектакль"),
        (MASTER_CLASS, "Мастер-класс"),
        (READING, "Читка"),
    ]

    base_event = models.ForeignKey(
        BaseEvent,
        on_delete=models.CASCADE,
        related_name="body",
        verbose_name="Событие",
    )
    type = models.CharField(
        verbose_name="Тип события",
        choices=EVENT_TYPES,
        default=PERFORMANCE,
        max_length=50,
    )
    date_time = models.DateTimeField(verbose_name="Дата и время")
    paid = models.BooleanField(verbose_name="Платное")
    url = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка",
        unique=True,
    )
    place = models.CharField(verbose_name="Место", max_length=200)

    def __str__(self):
        return f"{self.base_event} - {self.type}, {self.date_time}"

    class Meta:
        ordering = ("-created",)
        verbose_name = "Событие"
        verbose_name_plural = "События"
