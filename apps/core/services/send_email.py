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
        send_status = message.send()
        if send_status == 0:
            return False
        elif not hasattr(message, "anymail_status"):
            return True
        elif message.anymail_status.esp_response.status_code == status.HTTP_200_OK:
            return True
        return False
    except AnymailConfigurationError:
        msg = f"Неверные настройки Mailjet. Не удалось отправить письмо на почтовые адреса - {to_emails}."
        logger.critical(msg, exc_info=True)
    except (AnymailRequestsAPIError, AnymailInvalidAddress):
        msg = (
            f"Не указан адрес электронной почты отправителя."
            f"Не удалось отправить письмо на почтовые адреса - {to_emails}."
        )
        logger.critical(msg, exc_info=True)
    except ValueError:
        msg = f"Неверный ID шаблона Mailjet. Не удалось отправить письмо на почтовые адреса - {to_emails}."
        logger.critical(msg, exc_info=True)
    except AnymailError:
        msg = "Ooops, something goes wrong! :("
        logger.critical(msg, exc_info=True)
