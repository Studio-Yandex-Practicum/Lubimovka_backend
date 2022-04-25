from django.utils import timezone

from apps.feedback.models.participation_application import (
    ALLOWED_FORMATS_FILE_FOR_PARTICIPATION,
    UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION,
)

ERROR_MESSAGES_FOR_QUESTION_FOR_400 = {
    "example": {
        "author_email": [
            "Это поле не может быть пустым.",
            "Введите правильный адрес электронной почты.",
        ],
        "question": [
            "Это поле не может быть пустым.",
            "Вопрос должен состоять более чем из 2 символов.",
        ],
        "author_name": [
            "Это поле не может быть пустым.",
        ],
    }
}

ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400 = {
    "example": {
        "non_field_errors": [
            f"Повторная отправка заявки с данными в полях {UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION}."
            f"При необходимости отправить повторную заявку, укажите это в названии пьесы."
        ],
        "year": [
            "Обязательное поле.",
            "Убедитесь, что это значение больше либо равно 1900.",
            "Убедитесь, что это значение меньше либо равно " f"{timezone.now().year}.",
        ],
        "first_name": ["Обязательное поле."],
        "last_name": ["Обязательное поле."],
        "birth_year": [
            "Обязательное поле.",
            "Убедитесь, что это значение больше либо равно 1900.",
            "Убедитесь, что это значение меньше либо равно " f"{timezone.now().year}.",
        ],
        "phone_number": [
            "Введен некорректный номер телефона.",
            "Обязательное поле.",
        ],
        "email": ["Обязательное поле."],
        "title": ["Обязательное поле."],
        "file": [
            "Загруженный файл не является корректным файлом.",
            "Ни одного файла не было отправлено.",
            "Расширение файлов {} не поддерживается. ",
            f"Разрешенные расширения: " f"{ALLOWED_FORMATS_FILE_FOR_PARTICIPATION}.",
        ],
    }
}
ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403 = {"example": {"detail": "Приём пьес закрыт."}}
