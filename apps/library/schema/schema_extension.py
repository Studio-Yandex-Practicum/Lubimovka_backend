from django.utils import timezone

from apps.library.models.participation_application import (
    ALLOWED_FORMATS_FILE_FOR_PARTICIPATION,
    UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION,
)

ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400 = {
    "example": {
        "non_field_errors": [
            f"Поля {UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION} " f"должны производить массив с уникальными значениями."
        ],
        "year": [
            "Обязательное поле.",
            "Убедитесь, что это значение больше либо равно 1900.",
            "Убедитесь, что это значение меньше либо равно " f"{timezone.now().year}.",
        ],
        "first_name": ["Обязательное поле."],
        "last_name": ["Обязательное поле."],
        "birthday": [
            "Обязательное поле.",
            "Неправильный формат date. " "Используйте один из этих форматов: YYYY-MM-DD.",
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
