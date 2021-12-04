from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.core.utilities import slugify


class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating ``created`` and
    ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


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

    @property
    def reversed_full_name(self):
        return f"{self.last_name} {self.first_name}"


class Role(BaseModel):
    """Role for `Person`.

    Saves different type of roles:
        - blog persons roles
        - performance roles
        - play roles
        ..and so on

    Suppose to be used in pair with `Person` model and intermediate (through)
    table.
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название",
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        verbose_name="Код-имя латиницей",
        help_text="Если пустое, то заполняется автоматически",
    )

    class Meta:
        verbose_name = "Должность/позиция"
        verbose_name_plural = "Должности/позиции"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Settings(BaseModel):
    class SettingGroup(models.TextChoices):
        EMAIL = "EMAIL", _("Почта")
        MAIN = "MAIN", _("Главная")
        FIRST_SCREEN = "FIRST_SCREEN", _("Первая страница")
        GENERAL = "GENERAL", _("Общие")

    class SettingFieldType(models.TextChoices):
        BOOLEAN = "BOOLEAN", _("Да/Нет")
        TEXT = "TEXT", _("Текст")
        URL = "URL", _("URL")
        IMAGE = "IMAGE", _("Картинка")
        EMAIL = "EMAIL", _("EMAIL")

    TYPES_AND_FIELDS = {
        SettingFieldType.BOOLEAN: "boolean",
        SettingFieldType.TEXT: "text",
        SettingFieldType.URL: "url",
        SettingFieldType.IMAGE: "image",
        SettingFieldType.EMAIL: "email",
    }

    group = models.CharField(
        choices=SettingGroup.choices,
        default="GENERAL",
        max_length=50,
        verbose_name="Группа настроек",
    )
    field_type = models.CharField(
        choices=SettingFieldType.choices,
        max_length=40,
        verbose_name="Выбор поля настроек",
    )
    settings_key = models.SlugField(
        max_length=40,
        verbose_name="Ключ настройки",
        unique=True,
    )
    description = models.TextField(
        max_length=250,
        verbose_name="Описание настройки",
        null=True,
    )
    boolean = models.BooleanField(
        default=False,
        verbose_name="Да или Нет",
    )
    text = models.TextField(
        max_length=500,
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
        ordering = ("group", "settings_key")
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"

    def __str__(self):
        return self.settings_key

    @property
    def value(self):
        return getattr(
            self,
            self.TYPES_AND_FIELDS[self.field_type],
        )

    @classmethod
    def get_setting(cls, settings_key):
        if Settings.objects.filter(settings_key=settings_key).exists():
            setting = Settings.objects.get(settings_key=settings_key)
            return setting.value


class SettingsGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group=self.model.name_group)


class SettingsEmail(Settings):
    object = SettingsGroupManager()
    name_group = "EMAIL"

    class Meta:
        proxy = True
        verbose_name = "Настройки почты"
        verbose_name_plural = "Настройки почты"


class SettingsGeneral(Settings):
    object = SettingsGroupManager()
    name_group = "GENERAL"

    class Meta:
        proxy = True
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"


class SettingsMain(Settings):
    object = SettingsGroupManager()
    name_group = "MAIN"

    class Meta:
        proxy = True
        verbose_name = "Настройки главной страницы"
        verbose_name_plural = "Настройки главной страницы"


class SettingsFirstScreen(Settings):
    object = SettingsGroupManager()
    name_group = "FIRST_SCREEN"

    class Meta:
        proxy = True
        verbose_name = "Настройки первой страницы"
        verbose_name_plural = "Настройки первой страницы"
