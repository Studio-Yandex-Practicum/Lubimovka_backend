from django.core.mail import EmailMessage

from apps.core.models import Setting
from apps.core.utils import send_email
from config.settings.base import MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION


def send_application_email(instance):
    message = EmailMessage(
        from_email=Setting.get_setting("email_send_from"),
        to=(Setting.get_setting("email_on_acceptance_of_plays_page"),),
    )
    message.template_id = MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION
    message.merge_global_data = {
        "year": instance.year,
        "birth_year": instance.birth_year,
        "first_name": instance.last_name,
        "last_name": instance.last_name,
        "city": instance.city,
        "phone_number": instance.phone_number.as_international,
        "email": instance.email,
        "title": instance.title,
    }

    # attach file
    message.attach_file(instance.file.path)

    return send_email(message)
