from django.db import models

from apps.core.models import BaseModel
from apps.library.models import Performance, Person, Play


class ItemBase(BaseModel):
    title = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class OrderedItemBase(BaseModel):
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True
        ordering = ["order"]


class Video(ItemBase):
    description = models.TextField(
        max_length=500,
        blank=True,
    )
    url = models.URLField()

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class OrderedVideo(OrderedItemBase):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="ordered_videos",
    )
    image_block = models.ForeignKey(
        "VideosBlock",
        on_delete=models.CASCADE,
        related_name="ordered_videos",
    )

    def __str__(self):
        return f"{self.order} — {self.video}"


class VideosBlock(ItemBase):
    videos = models.ManyToManyField(
        to=Video,
        through=OrderedVideo,
    )

    class Meta:
        verbose_name = "Блок видео"
        verbose_name_plural = "Блоки видео"


class Image(ItemBase):
    image = models.FileField(upload_to="content_images")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class OrderedImage(OrderedItemBase):
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="ordered_images",
    )
    image_block = models.ForeignKey(
        "ImagesBlock",
        on_delete=models.CASCADE,
        related_name="ordered_images",
    )

    def __str__(self):
        return f"{self.order} — {self.image}"


class ImagesBlock(ItemBase):
    images = models.ManyToManyField(
        to=Image,
        through=OrderedImage,
    )

    class Meta:
        verbose_name = "Блок изображения"
        verbose_name_plural = "Блоки изображений"


class Link(ItemBase):
    description = models.TextField(
        max_length=250,
        verbose_name="Описание ссылки",
    )
    url = models.URLField()

    class Meta:
        verbose_name = "Ссылка с описанием"
        verbose_name_plural = "Ссылки с описанием"


class OrderedPerformance(OrderedItemBase):
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name="ordered_performances",
    )
    performance_block = models.ForeignKey(
        "PerformancesBlock",
        on_delete=models.CASCADE,
        related_name="ordered_performances",
    )

    def __str__(self):
        return f"{self.order} — {self.performance}"


class PerformancesBlock(ItemBase):
    performances = models.ManyToManyField(
        to=Performance,
        through=OrderedPerformance,
    )

    class Meta:
        verbose_name = "Блок спектаклей"
        verbose_name_plural = "Блоки спектаклей"


class OrderedPlay(OrderedItemBase):
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="ordered_plays",
    )
    play_block = models.ForeignKey(
        "PlaysBlock",
        on_delete=models.CASCADE,
        related_name="ordered_plays",
    )

    def __str__(self):
        return f"{self.order} — {self.play}"


class PlaysBlock(ItemBase):
    plays = models.ManyToManyField(
        to=Play,
        through=OrderedPlay,
    )

    class Meta:
        verbose_name = "Блок пьес"
        verbose_name_plural = "Блоки пьес"


class OrderedPerson(OrderedItemBase):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="ordered_persons",
    )
    person_block = models.ForeignKey(
        "PersonsBlock",
        on_delete=models.CASCADE,
        related_name="ordered_persons",
    )

    def __str__(self):
        return f"{self.order} — {self.person}"


class PersonsBlock(ItemBase):
    persons = models.ManyToManyField(
        to=Person,
        through=OrderedPerson,
    )

    class Meta:
        verbose_name = "Блок персон"
        verbose_name_plural = "Блоки персон"
