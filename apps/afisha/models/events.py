from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save

from apps.afisha.models import MasterClass, Performance, Reading
from apps.core.models import BaseModel


class CommonEvent(BaseModel):
    """
    Промежуточная модель, связывающая модели Спектакля, Мастер-класса и Читки с моделью События (Event).

    Связь реализована через OneToOneFields в моделях Performance, Masterclass
    и Reading (поле events), а также ForeignKey в моделе Event (поле
    common_event).
    Подробнее о данном способе связи - в статье:
    https://lukeplant.me.uk/blog/posts/avoid-django-genericforeignkey/
    (блок 'Alternative 3 - intermediate table with OneToOneFields on
    destination models')
    """

    class Meta:
        ordering = ("-created",)
        verbose_name = "Базовое событие"
        verbose_name_plural = "Базовые события"

    def __str__(self):
        return f"{self.target_model}"

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


class Event(BaseModel):
    class EventType(models.TextChoices):
        PERFORMANCE = "PERFORMANCE", "Спектакль"
        MASTERCLASS = "MASTERCLASS", "Мастер-класс"
        READING = "READING", "Читка"

    class ActionType(models.TextChoices):
        REGISTRATION = "REGISTRATION", "Регистрация"
        TICKETS = "TICKETS", "Билеты"
        STREAM = "STREAM", "Трансляция"

    common_event = models.ForeignKey(
        CommonEvent,
        on_delete=models.CASCADE,
        related_name="body",
        verbose_name="Событие",
        help_text=(
            "Создайте спектакль, читку или мастер-класс чтобы получить возможность создать соответствующее событие"
        ),
    )
    type = models.CharField(
        choices=EventType.choices,
        max_length=50,
        verbose_name="Тип события",
        help_text="Выберите тип события",
    )
    date_time = models.DateTimeField(
        verbose_name="Дата и время",
        blank=True,
        null=True,
    )
    url = models.URLField(
        max_length=200,
        verbose_name="Ссылка",
    )
    action = models.CharField(
        choices=ActionType.choices,
        default="REGISTRATION",
        max_length=50,
        verbose_name="Название действия",
        help_text="Выберите название действия, соответсвующее содержанию ссылки",
    )
    pinned_on_main = models.BooleanField(
        default=False,
        verbose_name="Закрепить на главной",
    )
    is_archived = models.BooleanField(
        default=False,
        verbose_name="В архиве",
    )

    class Meta:
        ordering = ("-date_time",)
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        event_name = self.common_event.target_model
        event_label = self.EventType(self.type).label
        if self.date_time is not None:
            event_date = self.date_time.date().strftime("%d.%m.%Y")
            event_time = self.date_time.time().strftime("%H:%M")
            return f'{event_label} - "{event_name}". Дата: {event_date}. Время: {event_time}'
        return f'{event_label} - "{event_name}". (В архиве)'

    def save(self, *args, **kwargs):
        allowed_event_types = {
            Performance: self.EventType.PERFORMANCE,
            MasterClass: self.EventType.MASTERCLASS,
            Reading: self.EventType.READING,
        }
        self.type = allowed_event_types[type(self.common_event.target_model)]
        super().save(*args, **kwargs)

    def clean(self):
        if not self.date_time and not self.is_archived:
            raise ValidationError("Необходимо предоставить дату события, " "либо поставить отметку 'В архиве'")
        return super().clean()


def create_common_event(sender, instance, **kwargs):
    if not instance.events_id:
        instance.events_id = CommonEvent.objects.create().id


pre_save.connect(create_common_event, sender=MasterClass)
pre_save.connect(create_common_event, sender=Reading)
pre_save.connect(create_common_event, sender=Performance)
