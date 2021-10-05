from django.db import models

from apps.core.models import BaseModel


class BaseEvent(BaseModel):
    """
    Промежуточная модель, связывающая модели Спектакля, Мастер-класса и Читки
    с моделью События (Event).
    Связь реализована через OneToOneFields в моделях Performance, Masterclass
    и Reading (поле event), а также ForeignKey в моделе Event (поле
    base_event).
    Подробнее о данном способе связи - в статье:
    https://lukeplant.me.uk/blog/posts/avoid-django-genericforeignkey/
    (блок 'Alternative 3 - intermediate table with OneToOneFields on
    destination models')
    """

    def __str__(self):
        return f"{repr(self.target_model)}"

    @property
    def target_model(self):
        if getattr(self, "masterclasses", None) is not None:
            return self.masterclasses
        if getattr(self, "readings", None) is not None:
            return self.readings
        if getattr(self, "performances", None) is not None:
            return self.performances
        return None

    target_model.fget.short_description = "Спектакль/Мастер-класс/Читка"

    class Meta:
        ordering = ("-created",)
        verbose_name = "Базовое событие"
        verbose_name_plural = "Базовые события"


class Event(BaseModel):
    PERFORMANCE = "Спектакль"
    MASTER_CLASS = "Мастер-класс"
    READING = "Читка"
    EVENT_TYPES = [
        (PERFORMANCE, PERFORMANCE),
        (MASTER_CLASS, MASTER_CLASS),
        (READING, READING),
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
    paid = models.BooleanField(verbose_name="Платное", default=False)
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
