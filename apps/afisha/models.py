from django.db import models

from apps.core.models import BaseModel


class CommonEvent(BaseModel):
    """
    Промежуточная модель, связывающая модели Спектакля, Мастер-класса и Читки
    с моделью События (Event).
    Связь реализована через OneToOneFields в моделях Performance, Masterclass
    и Reading (поле events), а также ForeignKey в моделе Event (поле
    common_event).
    Подробнее о данном способе связи - в статье:
    https://lukeplant.me.uk/blog/posts/avoid-django-genericforeignkey/
    (блок 'Alternative 3 - intermediate table with OneToOneFields on
    destination models')
    """

    def __str__(self):
        return f"{repr(self.target_model)}"

    @property
    def target_model(self):
        if getattr(self, "masterclass", None) is not None:
            return self.masterclass
        if getattr(self, "reading", None) is not None:
            return self.reading
        if getattr(self, "performance", None) is not None:
            return self.performance
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

    common_event = models.ForeignKey(
        CommonEvent,
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
        verbose_name="Ссылка",
    )
    place = models.CharField(verbose_name="Место", max_length=200)
    pinned_on_main = models.BooleanField(
        verbose_name="Закрепить на главной",
        default=False,
    )

    def __str__(self):
        return f"{self.common_event} - {self.type}, {self.date_time}"

    class Meta:
        ordering = ("-created",)
        verbose_name = "Событие"
        verbose_name_plural = "События"
