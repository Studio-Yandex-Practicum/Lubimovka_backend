from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import BaseModel
from apps.core.utils import slugify
from apps.feedback.utilities import generate_upload_path, get_festival_year
from apps.feedback.validators import year_validator

UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION = (
    "first_name",
    "last_name",
    "birth_year",
    "city",
    "phone_number",
    "email",
    "title",
    "year",
)
ALLOWED_FORMATS_FILE_FOR_PARTICIPATION = (
    "doc",  #
    "docx",
    "txt",
    "odt",
    "pdf",
)


class ParticipationApplicationFestival(BaseModel):
    """Заявки на участие в фестивале."""

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создана",
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
    )
    pseudonym = models.CharField(
        max_length=30,
        verbose_name="Псевдоним",
        null=True,
        blank=True,
    )
    birth_year = models.PositiveSmallIntegerField(
        validators=(year_validator,),
        verbose_name="Год рождения",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город проживания",
    )
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона",
        help_text="Номер телефона указывается в формате +7",
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="Электронная почта",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название пьесы",
    )
    year = models.PositiveSmallIntegerField(
        validators=(year_validator,),
        verbose_name="Год написания",
    )
    file = models.FileField(
        validators=(FileExtensionValidator(ALLOWED_FORMATS_FILE_FOR_PARTICIPATION),),
        max_length=350,
        verbose_name="Файл",
        upload_to=generate_upload_path,
        help_text=f"Файл должен быть в одном из поддерживаемых форматов: " f"{ALLOWED_FORMATS_FILE_FOR_PARTICIPATION}",
        blank=True,
    )
    url_file_in_storage = models.URLField(
        verbose_name="Ссылка для скачивания файла с Диска",
        blank=True,
        max_length=1024,
    )

    BOOL_CHOICES = ((True, "Да"), (False, "Нет"))
    verified = models.BooleanField(
        default=False,
        verbose_name="Проверена?",
        choices=BOOL_CHOICES,
    )
    exported_to_google = models.BooleanField(
        default=False,
        verbose_name="Выгружена в Google-таблицу",
        editable=False,
    )
    saved_to_storage = models.BooleanField(
        default=False,
        verbose_name="Файл сохранен на Диске",
        editable=False,
    )
    sent_to_email = models.BooleanField(
        default=False,
        verbose_name="Подтверждение отправлено",
        editable=False,
    )
    festival_year = models.PositiveSmallIntegerField(
        default=get_festival_year,
        verbose_name="Год фестиваля",
    )

    class Meta:
        verbose_name_plural = "Заявки на участие"
        verbose_name = "Заявка на участие"
        constraints = (
            models.UniqueConstraint(
                fields=UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION,
                name="unique_application",
            ),
        )

    def __str__(self):
        return f"{self.last_name}-{self.title}"

    def generate_filename(self):
        """Generate new filename as "Last_name-Title" format."""
        filename = f"{self.last_name}_{self.first_name}___{self.title}"
        filename = slugify(filename).replace("-", "_")
        return f"{filename.title()}.{self.file.name.split('.')[-1]}"

    def save(self, *args, **kwargs):
        """Save generated filename."""
        if self.file and not self.saved_to_storage:
            self.file.name = self.generate_filename()
        super().save(*args, **kwargs)

    @property
    def file_url(self):
        if self.saved_to_storage:
            return self.url_file_in_storage
        return self.file.url
