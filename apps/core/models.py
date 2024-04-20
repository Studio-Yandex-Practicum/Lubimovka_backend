from pathlib import Path
from typing import Any, Union

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.mixins import FileCleanUpMixin
from apps.core.utils import slugify
from apps.core.validators import email_validator

NEWS_HELP_TEXT = (
    "При включении данной настройки, автоматический будет "
    "выключена настройка Отображение дневника на главной страницы"
)
BLOG_HELP_TEXT = (
    "При включении данной настройки, автоматический будет "
    "выключена настройка 'Отображение новостей на главной странице'"
)
CORE_ROLES = ("director", "directress", "dramatist", "dramatess")


class BaseModel(models.Model):
    """
    An abstract base class model.

    It provides self-updating ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


class Image(BaseModel):
    image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        verbose_name="Изображение",
        help_text="Загрузите фотографию",
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.image.url


class Person(FileCleanUpMixin, BaseModel):
    cleanup_fields = ("image",)
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        blank=True,
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
        validators=(email_validator,),
        verbose_name="Электронная почта",
        help_text="Необходим, если для связанного автора создан виртуальный адрес",
        null=True,
        blank=True,
        unique=True,
    )
    image = models.ImageField(
        upload_to="images/person_avatars",
        verbose_name="Фотография",
        blank=True,
        help_text="Обязательно указать для: членов команды, попечителей фестиваля и волонтёров.",
    )

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"
        ordering = ("last_name", "first_name")
        constraints = [
            UniqueConstraint(
                fields=["first_name", "last_name", "middle_name", "email"],
                name="unique_person",
            )
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Сохранение связанного автора для обновления таблицы переадресации почты
        if hasattr(self, "authors"):
            self.authors.save()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    @admin.display(description="Фамилия и имя")
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def reversed_full_name(self):
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def mail_forwarding_enabled(self):
        if hasattr(self, "authors") and hasattr(self.authors, "virtual_email"):
            return self.authors.virtual_email.enabled
        return False

    @property
    def mail_forwarding_created(self):
        return hasattr(self, "authors") and hasattr(self.authors, "virtual_email")


class Role(BaseModel):
    """Role for `Person`.

    Saves different type of roles:
        - blog persons roles
        - performance roles
        - play roles
        - master class roles
        - reading roles

    Suppose to be used in pair with `Person` model and intermediate (through)
    table.
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название",
    )
    name_plural = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name="Название во множественном числе",
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        verbose_name="Код-имя латиницей",
        help_text="Заполняется автоматически",
    )
    types = models.ManyToManyField(
        "RoleType",
        related_name="type_roles",
        verbose_name="Типы ролей",
    )

    order = models.PositiveSmallIntegerField(
        "Порядок",
        default=0,
        db_index=True,
        blank=False,
        null=False,
        help_text="Определяет очередность вывода",
    )

    class Meta:
        verbose_name = "Должность/позиция"
        verbose_name_plural = "Должности/позиции"
        ordering = ("order",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class RoleType(models.Model):
    class SelectRoleType(models.TextChoices):
        BLOG_PERSONS_ROLE = "blog_persons_role", _("Роль в блоге")
        PERFORMANCE_ROLE = "performanse_role", _("Роль в спектаклях")
        PLAY_ROLE = "play_role", _("Роль в пьесах")
        READING_ROLE = "reading_role", _("Роль в специальных событиях")

    role_type = models.CharField(
        max_length=20,
        choices=SelectRoleType.choices,
        default="blog_persons_role",
        unique=True,
        verbose_name="Тип роли",
        help_text="Укажите, где будет использована роль",
    )

    class Meta:
        verbose_name = "Тип роли"
        verbose_name_plural = "Типы ролей"

    def __str__(self):
        role_label = RoleType.SelectRoleType(self.role_type).label
        return str(role_label)


class Setting(FileCleanUpMixin, BaseModel):
    cleanup_fields = ("image",)

    class SettingGroup(models.TextChoices):
        EMAIL = "EMAIL", _("Почта")
        MAIN = "MAIN", _("Главная")
        FIRST_SCREEN = "FIRST_SCREEN", _("Первая страница")
        GENERAL = "GENERAL", _("Общие")
        AFISHA = "AFISHA", _("Афиша")
        GOOGLE_EXPORT = "PLAY_SUPPLY", _("Подача пьес")

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

    HELP_TEXT = {
        "main_add_blog": BLOG_HELP_TEXT,
        "main_add_news": NEWS_HELP_TEXT,
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
        blank=True,
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
        upload_to=path_by_app_label_and_class_name,
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

    def clean(self):
        if (
            self.group in {self.SettingGroup.FIRST_SCREEN, self.SettingGroup.MAIN}
            and self.field_type == self.SettingFieldType.IMAGE
            and not self.image
        ):
            raise ValidationError(
                {"image": "Изображение должно присутствовать на странице. Оставьте или замените на другое."}
            )

    def save(self, *args, **kwargs):
        colors_settings_keys = ("background_color", "accent_color")
        if self.settings_key in colors_settings_keys and self.text:
            self._generate_css()
        return super().save(*args, **kwargs)

    @property
    def value(self):
        return getattr(
            self,
            self.TYPES_AND_FIELDS[self.field_type],
        )

    @classmethod
    def get_setting(cls, settings_key):
        is_settings_key_found = Setting.objects.filter(settings_key=settings_key).exists()
        assert is_settings_key_found, f"Ключа настроек `{settings_key}` не найдено."

        setting = Setting.objects.get(settings_key=settings_key)
        return setting.value

    @classmethod
    def get_settings(cls, settings_keys: Union[list[str], tuple[str]]) -> dict[str, Any]:
        """Get list or tuple of setting keys and return dict with values."""
        # fmt: off
        assert (
            (isinstance(settings_keys, tuple) or isinstance(settings_keys, list))
            and len(settings_keys)
        ), "Метод ожидает только непустые `tuple` или `list` из строк `settings_key`."
        # fmt: on

        settings_qs = Setting.objects.filter(settings_key__in=settings_keys)
        settings_dict = {
            setting.settings_key: getattr(setting, cls.TYPES_AND_FIELDS[setting.field_type]) for setting in settings_qs
        }

        assert set(settings_keys).issubset(
            settings_dict
        ), f"Не все переданные ключи найдены. Нашлись {settings_dict.keys()}"

        return settings_dict

    def _set_settings(self, settings):
        for key, value in settings.items():
            count = Setting.objects.filter(settings_key=key).update(boolean=value)
            assert count == 1, f"Количество записей с ключом '{key}' оказалось равно {count} (ожидалось 1)"

    def _generate_css(self):
        """Generate CSS file with colors."""
        Setting.objects.filter(settings_key=self.settings_key).update(text=self.text)
        colors = self.get_settings(("background_color", "accent_color"))
        filename = Path("apps/core/static/site_colors.css")
        with open(filename, "w+") as f:
            # fmt: off
            css_file_contents = (":root {{\n"
                                 "--background-color-primary-season: {};\n"
                                 "--background-color-secondary-season: {};\n}}\n"
                                 ).format(colors["background_color"], colors["accent_color"])
            f.write(css_file_contents)
