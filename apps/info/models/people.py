from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, Person
from apps.info.models import Festival


class Partner(BaseModel):
    class PartnerType(models.TextChoices):
        GENERAL_PARTNER = "general", _("Генеральный партнер")
        FESTIVAL_PARTNER = "festival", _("Партнер фестиваля")
        INFO_PARTNER = "info", _("Информационный партнер")

    name = models.CharField(
        max_length=200,
        verbose_name="Наименование",
    )
    type = models.CharField(
        max_length=8,
        choices=PartnerType.choices,
        verbose_name="Тип",
    )
    url = models.URLField(
        max_length=200,
        verbose_name="Ссылка на сайт",
    )
    image = models.ImageField(
        upload_to="images/info/partnerslogo",
        verbose_name="Логотип",
        help_text="Загрузите логотип партнёра",
    )
    in_footer_partner = models.BooleanField(
        default=False,
        verbose_name="Отображать внизу страницы",
        help_text=("Поставьте галочку, чтобы показать логотип партнёра внизу страницы"),
    )

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ("type",)

    def save(self, *args, **kwargs):
        this = Partner.objects.get(id=self.id)
        if this:
            if this.image != self.image:
                this.image.delete(save=False)
        super(Partner, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.type}"


class Sponsor(BaseModel):
    person = models.OneToOneField(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
    )
    position = models.CharField(
        max_length=150,
        verbose_name="Должность",
    )

    class Meta:
        verbose_name = "Попечитель фестиваля"
        verbose_name_plural = "Попечители фестиваля"

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        if self._has_person_before_saving() and not self.person.image:
            raise ValidationError("Для спонсора должно быть выбрано фото")
        return super().clean(*args, **kwargs)

    def _has_person_before_saving(self):
        return self.person_id is not None


class Volunteer(BaseModel):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
    )
    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        related_name="volunteers",
        verbose_name="Фестиваль",
    )
    review_title = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Заголовок отзыва",
    )
    review_text = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name="Текст отзыва",
    )

    class Meta:
        verbose_name = "Волонтёр фестиваля"
        verbose_name_plural = "Волонтёры фестиваля"
        ordering = ("person__last_name", "person__first_name")
        constraints = [
            UniqueConstraint(
                fields=("person", "festival"),
                name="unique_volunteer",
            )
        ]

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - волонтёр фестиваля {self.festival.year} года"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self._has_person_before_saving():
            if not self.person.email:
                raise ValidationError("Укажите email для волонтёра")
            if not self.person.image:
                raise ValidationError("Для волонтёра необходимо выбрать его фото")
            if not self.person.city:
                raise ValidationError("Укажите город проживания волонтёра")

    def _has_person_before_saving(self):
        return self.person_id is not None
