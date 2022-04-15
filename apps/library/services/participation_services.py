import logging

from anymail.exceptions import AnymailConfigurationError, AnymailError
from background_task import background
from googleapiclient.errors import HttpError
from yadisk.exceptions import YaDiskError

from apps.core.models import Setting
from apps.library.models import ParticipationApplicationFestival
from apps.library.services.email import send_application_email
from apps.library.services.spreadsheets import GoogleSpreadsheets
from apps.library.services.yandex_disk_export import yandex_disk_export

logger = logging.getLogger("django")

gs = GoogleSpreadsheets()


@background(schedule=60)
def participation_services(instance_id, domain):
    instance = ParticipationApplicationFestival.objects.get(id=instance_id)
    try:
        yandex_disk_export(instance)
    except YaDiskError as error:
        logger.critical(error, exc_info=True)

    try:
        export_success = gs.export(instance=instance, domain=domain)
        if export_success:
            instance.exported_to_google = True
            instance.save()
    except (ValueError, HttpError) as error:
        logger.critical(error, exc_info=True)

    try:
        send_success = send_application_email(instance)
        if send_success:
            instance.sent_to_email = True
            instance.save()
    except (
        AnymailConfigurationError,
        AnymailError,
        ValueError,
    ) as error:
        msg = (
            f"Не удалось отправить заявку на участие в фестивали id = {instance.id} "
            f"на почту {Setting.get_setting('email_on_acceptance_of_plays_page')}."
        )
        logger.critical(msg, error, exc_info=True)
