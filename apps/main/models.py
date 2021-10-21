from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.core.models import Image


class MainSettings(models.Model):
    @classmethod
    def get_settings(cls, settings_type):
        return MainSettings.objects.filter(type=settings_type)

    @classmethod
    def get_setting(cls, settings_key):
        return MainSettings.objects.get(settings_key=settings_key)

    class SettingsType(models.TextChoices):
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

    class SettingsKey(models.TextChoices):
        FESTIVAL_STATUS = "Festival_status", _("Состояние фестиваля (Да/Нет)")

        MAIN_TITLE = "Main_title", _("Заголовок для главной страницы")
        MAIN_DESCRIPTION = "Main_description", _(
            "Описание не главной страницы"
        )
        MAIN_URL = "Main_url", _("Ссылка для главной страницы")
        MAIN_IMAGE = "Main_image", _("Картинка для главной страницы")

        WHAT_WE_DO_PAGE_MAIN_TITLE = (
            "What_we_do_main_title",
            _("Главный заголовок страницы Что мы делаем?"),
        )
        WHAT_WE_DO_PAGE_TITLE = (
            "What_we_do_title",
            _("Подзаголовок страницы Что мы делаем?"),
        )
        WHAT_WE_DO_PAGE_INFO = (
            "What_we_do_page_info",
            _("Информационные блоки для страницы Что мы делаем?"),
        )
        IDEOLOGY_PAGE_FIRST_TITLE = (
            "Ideology_first_title",
            _("Первый подзаголовок страницы Идеология"),
        )
        IDEOLOGY_PAGE_SECOND_TITLE = (
            "Ideology_second_title",
            _("Второй подзаголовок страницы Идеология"),
        )
        IDEOLOGY_PAGE_INFO = (
            "Ideology_info",
            _("Информационные блоки для страницы Идеология"),
        )
        HISTORY_PAGE_TITLE = (
            "History_title",
            _("Подзаголовок страницы История"),
        )
        HISTORY_PAGE_INFO = (
            "History_info",
            _("Информационные блоки для страницы История"),
        )
        MAIL_SEND_TO = "Mail_send_to", _(
            "Email для отправки вопросов на сайте"
        )

    SETTINGS_FIELDS = {
        SettingsKey.FESTIVAL_STATUS: ["boolean"],
        SettingsKey.MAIN_TITLE: ["title"],
        SettingsKey.WHAT_WE_DO_PAGE_MAIN_TITLE: ["title"],
        SettingsKey.WHAT_WE_DO_PAGE_TITLE: ["title"],
        SettingsKey.IDEOLOGY_PAGE_FIRST_TITLE: ["title"],
        SettingsKey.IDEOLOGY_PAGE_SECOND_TITLE: ["title"],
        SettingsKey.HISTORY_PAGE_TITLE: ["title"],
        SettingsKey.MAIN_DESCRIPTION: ["text"],
        SettingsKey.MAIN_URL: ["url"],
        SettingsKey.MAIN_IMAGE: ["image"],
        SettingsKey.MAIL_SEND_TO: ["email"],
        SettingsKey.WHAT_WE_DO_PAGE_INFO: [],
        SettingsKey.IDEOLOGY_PAGE_INFO: [],
        SettingsKey.HISTORY_PAGE_INFO: [],
    }

    SETTINGS_GROUPS = {
        SettingsType.FESTIVAL_SETTINGS: [SettingsKey.FESTIVAL_STATUS],
        SettingsType.MAIN_PAGE_SETTINGS: [
            SettingsKey.MAIN_TITLE,
            SettingsKey.MAIN_DESCRIPTION,
            SettingsKey.MAIN_URL,
            SettingsKey.MAIN_IMAGE,
        ],
        SettingsType.HISTORY_PAGE_SETTINGS: [SettingsKey.HISTORY_PAGE_INFO],
        SettingsType.ABOUT_FESTIVAL_WHAT_WE_DO_PAGE_SETTINGS: [
            SettingsKey.WHAT_WE_DO_PAGE_MAIN_TITLE,
            SettingsKey.WHAT_WE_DO_PAGE_TITLE,
            SettingsKey.WHAT_WE_DO_PAGE_INFO,
        ],
        SettingsType.ABOUT_FESTIVAL_IDEOLOGY_PAGE_SETTINGS: [
            SettingsKey.IDEOLOGY_PAGE_FIRST_TITLE,
            SettingsKey.IDEOLOGY_PAGE_SECOND_TITLE,
            SettingsKey.IDEOLOGY_PAGE_INFO,
        ],
        SettingsType.OTHER_SETTINGS: [SettingsKey.MAIL_SEND_TO],
    }

    type = models.CharField(
        choices=SettingsType.choices,
        max_length=40,
        verbose_name="Выбор типа настроек",
    )
    settings_key = models.CharField(
        choices=SettingsKey.choices,
        max_length=40,
        verbose_name="Выбор ключа настроек",
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
        upload_to="main/",
        blank=True,
        verbose_name="Изображение",
    )
    images_for_page = models.ManyToManyField(
        Image,
        through="SettingsImageRelation",
        blank=True,
        related_name="images",
        verbose_name="Картинки для страницы",
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

    def clean(self, *args, **kwargs):
        if self.settings_key not in self.SETTINGS_GROUPS[self.type]:
            raise ValidationError(
                "SettingsKey настройки не соответствует type"
            )

    def save(self, *args, **kwargs):
        fields = {
            "boolean": False,
            "title": "",
            "text": "",
            "url": "",
            "image": "",
            "email": "",
        }
        if self.settings_key not in [
            MainSettings.SettingsKey.WHAT_WE_DO_PAGE_INFO,
            MainSettings.SettingsKey.IDEOLOGY_PAGE_INFO,
            MainSettings.SettingsKey.HISTORY_PAGE_INFO,
        ]:
            SettingsImageRelation.objects.filter(settings=self.id).delete()
            InfoBlock.objects.filter(setting=self.id).delete()
            for field in self.SETTINGS_FIELDS[self.settings_key]:
                del fields[field]
        for settings_key, value in fields.items():
            setattr(self, settings_key, value)
        super().save(*args, **kwargs)


class InfoBlock(models.Model):
    class BlockType(models.TextChoices):
        MAIN = "Main", _("Главный блок")
        FIRST = "First", _(
            "Первая группа блоков, относящаяся к первому подзаголовку"
        )
        SECOND = "Second", _(
            "Вторая группа блоков, относящаяся к первому подзаголовку"
        )

    block_title = models.CharField(
        max_length=100,
        verbose_name="Описание или заголовок блока",
        blank=True,
    )
    block_text = models.TextField(
        max_length=300,
        verbose_name="Текст блока",
    )
    setting = models.ForeignKey(
        MainSettings,
        on_delete=models.CASCADE,
    )
    block = models.CharField(
        choices=BlockType.choices,
        max_length=30,
        verbose_name="Принадлежность к блоку",
    )
    block_order = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Порядок отображения внутри блоков странице сверху вниз",
    )

    def clean(self):
        if self.block == InfoBlock.BlockType.MAIN and self.pk is not None:
            if (
                InfoBlock.objects.filter(block=InfoBlock.BlockType.MAIN)
                .exclude(id=self.id)
                .exists()
            ):
                raise ValidationError("Главный блок может быть только один")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["block", "block_order"],
                name="unique_order",
            )
        ]
        ordering = ["block_order"]
        verbose_name = "Информационный блок"
        verbose_name_plural = "Информационные блоки"

    def __str__(self):
        return self.block_title


class SettingsImageRelation(models.Model):
    settings = models.ForeignKey(
        MainSettings,
        on_delete=models.CASCADE,
        related_name="settings",
        verbose_name="Настройка",
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="images_blocks",
        verbose_name="Картинка",
    )
    image_order = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Порядковый номер картинки на странице сверху вниз",
        unique=True,
    )

    class Meta:
        ordering = ["image_order"]
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return self.settings.settings_key
