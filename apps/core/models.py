from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating ``created`` and
    ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(BaseModel):
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Изображение",
        help_text="Загрузите фотографию",
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Person(BaseModel):
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        blank=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город проживания",
        blank=True,
    )
    email = models.EmailField(
        max_length=200,
        verbose_name="Электронная почта",
        null=True,
        blank=True,
        unique=True,
    )
    image = models.ImageField(
        upload_to="images/person_avatars",
        verbose_name="Фотография",
        blank=True,
    )

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"
        ordering = ("last_name",)
        constraints = [
            UniqueConstraint(
                fields=["first_name", "last_name", "middle_name", "email"],
                name="unique_person",
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Settings(BaseModel):
    class SettingFieldType(models.TextChoices):
        BOOLEAN = "BOOLEAN", _("Да/Нет")
        TITLE = "TITLE", _("Заголовок/Описание")
        TEXT = "TEXT", _("Текст")
        URL = "URL", _("URL")
        IMAGE = "IMAGE", _("Картинка")
        EMAIL = "EMAIL", _("EMAIL")

    TYPES_AND_FIELDS = {
        SettingFieldType.BOOLEAN: "boolean",
        SettingFieldType.TITLE: "title",
        SettingFieldType.TEXT: "text",
        SettingFieldType.URL: "url",
        SettingFieldType.IMAGE: "image",
        SettingFieldType.EMAIL: "email",
    }

    field_type = models.CharField(
        choices=SettingFieldType.choices,
        max_length=40,
        verbose_name="Выбор поля настроек",
    )
    settings_key = models.SlugField(
        max_length=40,
        verbose_name="Ключ настроек",
        unique=True,
    )
    boolean = models.BooleanField(
        default=False,
        verbose_name="Да или Нет",
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Заголовок",
    )
    text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Текст",
    )
    url = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка",
    )
    image = models.ImageField(
        upload_to="core/",
        blank=True,
        verbose_name="Изображение",
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email",
    )

    class Meta:
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"

    def __str__(self):
        return self.settings_key

    def save(self, *args, **kwargs):
        fields = {
            "boolean": False,
            "title": "",
            "text": "",
            "url": "",
            "image": "",
            "email": "",
        }
        del fields[self.TYPES_AND_FIELDS[self.field_type]]
        for settings_key, value in fields.items():
            setattr(self, settings_key, value)
        super().save(*args, **kwargs)

    @classmethod
    def get_setting(cls, settings_key):
        if Settings.objects.filter(settings_key=settings_key).exists():
            setting = Settings.objects.get(settings_key=settings_key)
            return {
                settings_key: getattr(
                    setting, cls.TYPES_AND_FIELDS[setting.field_type]
                )
            }
