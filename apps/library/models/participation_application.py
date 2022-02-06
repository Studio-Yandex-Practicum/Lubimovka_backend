from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import BaseModel
from apps.core.utilities import slugify
from apps.library.utilities.export_to_google import export_new_object
from apps.library.utilities.utilities import generate_class_name_path, get_festival_year
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
        upload_to=generate_class_name_path,
        help_text=f"Файл в одно из форматов " f"{ALLOWED_FORMATS_FILE_FOR_PARTICIPATION}",
    )
    festival_year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Год фестиваля",
    )

    BOOL_CHOICES = ((True, "Да"), (False, "Нет"))
    verified = models.BooleanField(
        default=False,
        verbose_name="Проверена?",
        choices=BOOL_CHOICES,
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
        return f"{filename.title()}.{self.file.name.split('.')[1]}"

    def save(self, *args, **kwargs):
        """Save generated filename.

        Create festival year respectively to date when object is creating
        and export only new objects to Google sheet.
        """
        self.file.name = self.generate_filename()
        if self.id is None:
            self.festival_year = get_festival_year()
            export_new_object(self)
        super().save(*args, **kwargs)
