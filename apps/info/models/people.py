from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, Person
from apps.info.models import Festival


class Partner(BaseModel):
    class PartnerType(models.TextChoices):
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
    is_general = models.BooleanField(
        default=False,
        verbose_name="Генеральный партнер",
        help_text="Поставьте галочку, чтобы сделать партнёра генеральным",
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Описание",
        help_text="Поле не обязательное",
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
    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядок",
        db_index=True,
    )

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ("order",)

    def save(self, *args, **kwargs):
        this = Partner.objects.filter(id=self.id).first()
        if this and this.image != self.image:
            this.image.delete(save=False)
        super().save(*args, **kwargs)

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
    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядок",
        db_index=True,
    )

    class Meta:
        verbose_name = "Попечитель фестиваля"
        verbose_name_plural = "Попечители фестиваля"
        ordering = ("order",)

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"

    def clean(self, *args, **kwargs):
        if self.person_id and not self.person.image:
            raise ValidationError("Для спонсора должно быть выбрано фото")


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
    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядок",
        db_index=True,
    )

    class Meta:
        verbose_name = "Волонтёр фестиваля"
        verbose_name_plural = "Волонтёры фестиваля"
        ordering = ("order",)
        constraints = [
            UniqueConstraint(
                fields=("person", "festival"),
                name="unique_volunteer",
            )
        ]

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - волонтёр фестиваля {self.festival.year} года"

    def clean(self):
        errors = []
        if not self.person_id:
            return
        if not self.person.image:
            errors.append("Для волонтёра необходимо выбрать его фото")
        if (self.review_title and not self.review_text) or (self.review_text and not self.review_title):
            errors.append("Нельзя сделать отзыв без заголовка или заголовок без отзыва")

        if errors:
            raise ValidationError(errors)


class Selector(BaseModel):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
    )
    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        related_name="selectors",
        verbose_name="Фестиваль",
    )
    position = models.CharField(
        max_length=150,
        verbose_name="Должность",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядок",
        db_index=True,
    )

    class Meta:
        verbose_name = "Отборщик фестиваля"
        verbose_name_plural = "Отборщики фестиваля"
        ordering = ("order",)
        constraints = [
            UniqueConstraint(
                fields=("person", "festival"),
                name="unique_selector",
            )
        ]

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - Отборщик фестиваля {self.festival.year} года"

    def clean(self):
        if self.person_id and not self.person.image:
            raise ValidationError("Для отборщика необходимо выбрать его фото")
