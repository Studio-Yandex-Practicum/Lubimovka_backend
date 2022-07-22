from django.core.validators import MinLengthValidator
from django.db import models
from django.template.defaultfilters import truncatechars

from apps.core.models import BaseModel


class Question(BaseModel):
    question = models.TextField(
        max_length=500,
        validators=[MinLengthValidator(2, "Вопрос должен состоять более чем из 2 символов")],
        verbose_name="Текст вопроса",
    )
    author_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    author_email = models.EmailField(
        max_length=50,
        verbose_name="Электронная почта",
    )
    sent_to_email = models.BooleanField(default=False, verbose_name="Отправлена на почту", editable=False)

    class Meta:
        verbose_name = "Вопрос или предложение"
        verbose_name_plural = "Вопросы или предложения"

    def __str__(self):
        return f"{self.author_name} {self.question}"

    @property
    def short_question_text(self):
        """Get short question text."""
        return truncatechars(self.question, 70)

    short_question_text.fget.short_description = "Текст вопроса"
