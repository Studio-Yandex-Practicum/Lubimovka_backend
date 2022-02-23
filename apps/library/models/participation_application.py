from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import BaseModel
from apps.core.utils import slugify
from apps.library.utilities.participation_file import generate_upload_path
from apps.library.validators import year_validator

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

    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
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
        verbose_name="Файл",
        upload_to=generate_upload_path,
        help_text=f"Файл в одно из форматов " f"{ALLOWED_FORMATS_FILE_FOR_PARTICIPATION}",
    )

    BOOL_CHOICES = ((True, "Да"), (False, "Нет"))
    verified = models.BooleanField(
        default=False,
        verbose_name="Проверена?",
        choices=BOOL_CHOICES,
    )
    exported_to_google = models.BooleanField(default=False, verbose_name="Выгружена в Google-таблицу", editable=False)
    saved_to_storage = models.BooleanField(default=False, verbose_name="Файл сохранен на Диске", editable=False)

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
        self.file.name = self.generate_filename()
        super().save(*args, **kwargs)
