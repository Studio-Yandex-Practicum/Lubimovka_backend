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

    def __str__(self):
        return f"{self.id}"

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


class Settings(models.Model):
    class SettingType(models.TextChoices):
        """Группы настроек"""

        FESTIVAL_SETTINGS = "Festival_settings", _("Настройки фестиваля")
        MAIN_PAGE_SETTINGS = "Main_page_settings", _(
            "Настройки главной страницы"
        )
        HISTORY_PAGE_SETTINGS = "History_page_settings", _(
            "Настройки страницы истории"
        )
        ABOUT_FESTIVAL_WHAT_WE_DO_PAGE_SETTINGS = (
            "About_festival_what_we_do_page_settings",
            _("Настройки страницы О фестивале. Что мы делаем?"),
        )
        ABOUT_FESTIVAL_IDEOLOGY_PAGE_SETTINGS = (
            "About_festival_ideology_page_settings",
            _("Настройки страницы О фестивале. Идеология."),
        )
        OTHER_SETTINGS = "Other_settings", _("Прочие настройки")

    class SettingFieldType(models.TextChoices):
        """Поле для настроек"""

        BOOLEAN = "boolean", _("Да/Нет")
        TITLE = "title", _("Заголовок/Описание")
        TEXT = "text", _("Текст")
        URL = "url", _("URL")
        IMAGE = "image", _("Картинка")

    type = models.CharField(
        choices=SettingType.choices,
        max_length=40,
        verbose_name="Выбор типа настроек",
    )
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
        ordering = ["id"]
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
        del fields[self.field_type]
        for settings_key, value in fields.items():
            setattr(self, settings_key, value)
        super().save(*args, **kwargs)

    @classmethod
    def get_setting(cls, settings_key):
        if Settings.objects.filter(settings_key=settings_key).exists():
            setting = Settings.objects.get(settings_key=settings_key)
            return {settings_key: getattr(setting, setting.field_type)}
