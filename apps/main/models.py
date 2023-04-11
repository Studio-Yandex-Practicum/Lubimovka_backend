from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.mixins import image_clean_up_mixin_factory
from apps.core.models import BaseModel, Setting


class Banner(image_clean_up_mixin_factory(("image",)), BaseModel):
    class ButtonType(models.TextChoices):
        TICKETS = "TICKETS", _("Билеты")
        DETAILS = "DETAILS", _("Подробнее")
        READ = "READ", _("Читать")

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание",
    )
    url = models.URLField(
        max_length=200,
        verbose_name="Ссылка",
    )
    image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        verbose_name="Картинка",
    )
    button = models.CharField(
        choices=ButtonType.choices,
        max_length=40,
        verbose_name="Выбор типа кнопки",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядок",
        db_index=True,
    )

    class Meta:
        verbose_name = "Банер на главной странице"
        verbose_name_plural = "Банеры на главной странице"
        ordering = ("order",)

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if Banner.objects.count() >= 3 and not self.id:
            raise ValidationError("Нельзя создать более 3-х банеров")


class SettingGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group=self.model.group_name)


class SettingEmail(Setting):
    objects = SettingGroupManager()
    group_name = "EMAIL"

    class Meta:
        proxy = True
        verbose_name = "Настройки обратной связи"
        verbose_name_plural = "Настройки обратной связи"


class SettingGeneral(Setting):
    objects = SettingGroupManager()
    group_name = "GENERAL"

    class Meta:
        proxy = True
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"

    def save(self, *args, **kwargs):
        if self.settings_key == "festival_status":
            if self.boolean:
                self._set_settings(
                    {
                        "main_add_blog": True,
                        "main_add_news": False,
                        "main_add_places": True,
                        "main_add_short_list": False,
                        "main_show_afisha_only_for_today": True,
                    }
                )
            else:
                self._set_settings(
                    {
                        "main_add_blog": False,
                        "main_add_news": True,
                        "main_add_places": False,
                        "main_add_short_list": True,
                        "main_show_afisha_only_for_today": False,
                    }
                )
        return super().save(*args, **kwargs)


class SettingMain(Setting):
    objects = SettingGroupManager()
    group_name = "MAIN"

    class Meta:
        proxy = True
        verbose_name = "Настройки главной страницы"
        verbose_name_plural = "Настройки главной страницы"

    def save(self, *args, **kwargs):
        if self.settings_key == "main_add_news":
            if self.boolean:
                self._set_settings(
                    {
                        "main_add_blog": False,
                    }
                )
        if self.settings_key == "main_add_blog":
            if self.boolean:
                self._set_settings(
                    {
                        "main_add_news": False,
                    }
                )

        return super().save(*args, **kwargs)


class SettingFirstScreen(Setting):
    objects = SettingGroupManager()
    group_name = "FIRST_SCREEN"

    class Meta:
        proxy = True
        verbose_name = "Настройки первой страницы"
        verbose_name_plural = "Настройки первой страницы"


class SettingAfishaScreen(Setting):
    objects = SettingGroupManager()
    group_name = "AFISHA"

    class Meta:
        proxy = True
        verbose_name = "Настройки афиши"
        verbose_name_plural = "Настройки афиши"


class SettingPlaySupply(Setting):
    objects = SettingGroupManager()
    group_name = "PLAY_SUPPLY"

    class Meta:
        proxy = True
        verbose_name = "Настройки подачи пьес"
        verbose_name_plural = "Настройки подачи пьес"
