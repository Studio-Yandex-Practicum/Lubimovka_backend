from django.db import models

from apps.core.models import Image


class Text(models.Model):
    text = models.TextField(
        max_length=300,
        verbose_name="Текст",
    )
    text_order = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        ordering = ["text_order"]
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"

    def __str__(self):
        return self.text[:15]


class MainSettings(models.Model):
    FESTIVAL_SETTINGS = "Festival_settings"
    MAIN_PAGE_SETTINGS = "Main_page_settings"
    HISTORY_PAGE_SETTINGS = "History_page_settings"
    ABOUT_FESTIVAL_WHAT_WE_DO_PAGE_SETTINGS = (
        "About_festival_what_we_do_page_settings"
    )
    ABOUT_FESTIVAL_IDEOLOGY_PAGE_SETTINGS = (
        "About_festival_ideology_page_settings"
    )
    OTHER = "Other"
    EMAIL = "Email_value"
    BLOCKS = "Settings_with_blocks"
    BOOL = "Bool_value"
    TEXT = "Text_value"
    IMAGE = "Image"
    TITLE_DESCRIPTION_IMAGES_AND_TEXTS = (
        "Title_description_images_and_texts_value"
    )

    SETTINGS_TYPE_CHOICES = [
        (FESTIVAL_SETTINGS, "Настройки страницы фестиваля"),
        (MAIN_PAGE_SETTINGS, "Настройки главной страницы"),
        (HISTORY_PAGE_SETTINGS, "Настройки страницы История"),
        (
            ABOUT_FESTIVAL_WHAT_WE_DO_PAGE_SETTINGS,
            "Настройки страницы О" " фестивале. Что мы делаем?",
        ),
        (
            ABOUT_FESTIVAL_IDEOLOGY_PAGE_SETTINGS,
            "Настройки страницы О " "фестивале. Идеология?",
        ),
        (OTHER, "Прочие"),
    ]
    SETTINGS_VALUE_TYPE_CHOICES = [
        (EMAIL, "Email"),
        (BLOCKS, "Информационные блоки"),
        (BOOL, "Настройки Да/Нет"),
        (TEXT, "Текст"),
        (IMAGE, "Картинка"),
        (TITLE_DESCRIPTION_IMAGES_AND_TEXTS, "Настройка страницы"),
    ]

    type = models.CharField(
        choices=SETTINGS_TYPE_CHOICES,
        max_length=40,
        verbose_name="Выбор типа настроек",
    )
    value_type = models.CharField(
        choices=SETTINGS_VALUE_TYPE_CHOICES,
        max_length=40,
        verbose_name="Выбор типа значения настроек",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название (значение key)",
        unique=True,
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
    )
    description = models.CharField(
        max_length=100,
        verbose_name="Описание",
    )
    texts_for_page = models.ManyToManyField(
        Text,
        blank=True,
        related_name="pages_text",
        verbose_name="Текст для страницы",
    )
    images_for_page = models.ManyToManyField(
        Image,
        blank=True,
        related_name="pages",
        verbose_name="Картинки для страницы",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Email",
    )
    text = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Текстовое значение",
    )
    image = models.ImageField(
        upload_to="main/",
        verbose_name="Картинка",
    )
    boolean = models.BooleanField(
        default=False,
        verbose_name="Да или Нет",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"

    def __str__(self):
        return self.name


class InfoBlock(models.Model):
    FIRST = "First"
    MAIN = "Main"
    SECOND = "Second"

    BLOCK_TYPE_CHOICES = [
        (FIRST, "Первый"),
        (SECOND, "Второй"),
        (MAIN, "Главный"),
    ]
    title = models.CharField(
        max_length=100,
        verbose_name="Описание или заголовок",
    )
    value = models.CharField(
        max_length=300,
        verbose_name="Текст",
    )
    block_text = models.TextField(
        max_length=300,
        verbose_name="Текст",
    )
    block_image = models.ImageField(
        upload_to="main/",
        verbose_name="Картинка",
    )
    setting = models.ForeignKey(
        MainSettings,
        on_delete=models.PROTECT,
    )
    block_item = models.CharField(
        choices=BLOCK_TYPE_CHOICES,
        max_length=30,
        verbose_name="Выбор номер блока",
    )

    class Meta:
        verbose_name = "Информационный блок"
        verbose_name_plural = "Информационные блоки"

    def __str__(self):
        return self.title
