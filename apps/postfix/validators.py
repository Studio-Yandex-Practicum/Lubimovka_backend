from django.conf import settings
from django.core.validators import EmailValidator

FULL_EMAIL = "{name}@{domain}"
MESSAGE = "{message} Введен адрес {email}"


class VirtualNameValidator(EmailValidator):
    def __call__(self, value: str | None) -> None:
        full_email = FULL_EMAIL.format(name=value, domain=settings.POSTFIX_MAIL_DOMAIN)
        self.message = MESSAGE.format(message=EmailValidator.message, email=full_email)
        return super().__call__(full_email)
