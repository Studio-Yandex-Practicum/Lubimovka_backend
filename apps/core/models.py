from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps import core
from apps.core.utilities.get_object import get_object


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
        BLOCK = "block", _("Блок для страницы")

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
    images_for_page = models.ManyToManyField(
        Image,
        through="core.SettingImageRelation",
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

    def save(self, *args, **kwargs):
        """В случае изменения типа поля - все прочие поля очищаются"""
        fields = {
            "boolean": False,
            "title": "",
            "text": "",
            "url": "",
            "image": "",
            "email": "",
        }
        if self.field_type != Settings.SettingFieldType.BLOCK:
            SettingImageRelation.objects.filter(settings=self.id).delete()
            InfoBlock.objects.filter(setting=self.id).delete()
            del fields[self.field_type]
        for settings_key, value in fields.items():
            setattr(self, settings_key, value)
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls, settings):
        """Метод класса с помощью которого можно получить значение
        настроек в формате json.

        Параметры:
        "settings" - это список, который может
        состоять из ключей (settings_key) или групп запрашиваемых настроек (
        type)

        Возвращает:
        Значения настроек в формате json
        """

        data = {}
        for setting in settings:
            if setting in cls.SettingType:
                settings_data = cls.get_settings_of_a_specific_type(setting)
            else:
                settings_data = cls.get_one_setting(setting)
            if type(settings_data) is bool or settings_data:
                data[setting] = settings_data
        return data

    @classmethod
    def get_settings_of_a_specific_type(cls, settings_type):
        """Метод класса с помощью которого можно получить значения
        одного типа настроек в формате json.

        Параметры:
        "settings_type": str - название типа настроек (type)

        Возвращает:
        Значения настроек в формате json
        """

        data = {}
        settings = Settings.objects.filter(type=settings_type)
        for setting in settings:
            data[setting.settings_key] = cls.get_one_setting(
                setting.settings_key
            )
        return data

    @classmethod
    def get_one_setting(cls, settings_key):
        """Метод класса с помощью которого можно получить значение
        одной настройки в формате json.

        Параметры:
        "settings_key": str - значение ключа настройки

        Возвращает:
        Значение настройки в формате srt или json в зависимости от настройки
        """

        data = {}
        if get_object(Settings, settings_key=settings_key):
            setting = get_object(Settings, settings_key=settings_key)
            if setting.field_type == Settings.SettingFieldType.BLOCK:
                data["images"] = {}
                settings_images_relation_qs = (
                    SettingImageRelation.objects.filter(settings_id=setting.id)
                )
                for settings_images_relation in settings_images_relation_qs:
                    serializer = core.serializers.ImageSerializer(
                        data={
                            "image": Image.objects.get(
                                id=settings_images_relation.image_id,
                            ).image,
                        }
                    )
                    if serializer.is_valid():
                        data["images"][
                            settings_images_relation.image_order
                        ] = serializer.data["image"]
                data["info"] = {}
                info_blocks = InfoBlock.objects.filter(setting_id=setting.id)
                for info_block in info_blocks:
                    data["info"][info_block.block] = {}
                for info_block in info_blocks:
                    data["info"][info_block.block][info_block.block_order] = {
                        "title": info_block.block_title,
                        "text": info_block.block_text,
                    }
            else:
                if setting.field_type != "image":
                    data = getattr(setting, setting.field_type)
                else:
                    serializer = core.serializer.ImageSerializer(
                        data={
                            "image": setting.image,
                        }
                    )
                    if serializer.is_valid():
                        data = serializer.data["image"]
        return data


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
        Settings,
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

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["setting", "block", "block_order"],
                name="unique_order",
            )
        ]
        ordering = ["block_order"]
        verbose_name = "Информационный блок"
        verbose_name_plural = "Информационные блоки"

    def __str__(self):
        return self.block_title


class SettingImageRelation(models.Model):
    settings = models.ForeignKey(
        Settings,
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
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["settings", "image_order"],
                name="unique_image_order",
            )
        ]
        ordering = ["image_order"]
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return self.settings.settings_key
