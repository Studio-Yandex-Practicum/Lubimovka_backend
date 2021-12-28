from django.db import models

from apps.core.models import Setting


class SettingGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group=self.model.group_name)


class SettingEmail(Setting):
    objects = SettingGroupManager()
    group_name = "EMAIL"

    class Meta:
        proxy = True
        verbose_name = "Настройки почты"
        verbose_name_plural = "Настройки почты"


class SettingGeneral(Setting):
    objects = SettingGroupManager()
    group_name = "GENERAL"

    class Meta:
        proxy = True
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"


class SettingMain(Setting):
    objects = SettingGroupManager()
    group_name = "MAIN"

    class Meta:
        proxy = True
        verbose_name = "Настройки главной страницы"
        verbose_name_plural = "Настройки главной страницы"


class SettingFirstScreen(Setting):
    objects = SettingGroupManager()
    group_name = "FIRST_SCREEN"

    class Meta:
        proxy = True
        verbose_name = "Настройки первой страницы"
        verbose_name_plural = "Настройки первой страницы"
