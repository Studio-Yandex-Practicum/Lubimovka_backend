import logging

from anymail.exceptions import AnymailConfigurationError, AnymailError, AnymailInvalidAddress, AnymailRequestsAPIError
from django.core.mail import EmailMessage
from rest_framework import status

logger = logging.getLogger("django")


def send_email(from_email: str, to_emails: tuple, template_id: str, context: dict, attach_file: bool = False) -> bool:
    """Transmit email context in the template and send email.

    If there is a file in the instance then attach_file=True.

    For more information please read the documentation:
    https://anymail.readthedocs.io/en/stable/esps/mailjet//
    """
    try:
        message = EmailMessage(from_email=from_email, to=to_emails)
        message.template_id = template_id
        message.merge_global_data = context
        if attach_file:
            file_path = context.get("file_path")
            message.attach_file(file_path)
        message.send()
        if hasattr(message, "anymail_status") and message.anymail_status.esp_response.status_code == status.HTTP_200_OK:
            return True
        return False
    except AnymailConfigurationError as error:
        msg = f"Неверные настройки Mailjet. Не удалось отправить письмо на почтовые адреса - {to_emails}."
        logger.critical(msg, error, exc_info=True)
    except (AnymailRequestsAPIError, AnymailInvalidAddress) as error:
        msg = (
            f"Не указан адрес электронной почты отправителя."
            f"Не удалось отправить письмо на почтовые адреса - {to_emails}."
        )
        logger.critical(msg, error, exc_info=True)
    except ValueError as error:
        msg = f"Неверный ID шаблона Mailjet. Не удалось отправить письмо на почтовые адреса - {to_emails}."
        logger.critical(msg, error, exc_info=True)
    except AnymailError as error:
        msg = "Ooops, something goes wrong! :("
        logger.critical(msg, error, exc_info=True)
