from django.conf import settings
from django.core.validators import EmailValidator

FULL_EMAIL = "{name}@{domain}"


class VirtualNameValidator(EmailValidator):
    def __call__(self, value: str | None) -> None:
        full_email = FULL_EMAIL.format(name=value, domain=settings.POSTFIX_MAIL_DOMAIN)
        self.message = EmailValidator.message + f" Введен адрес {full_email}."
        return super().__call__(full_email)
