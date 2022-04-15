from anymail.exceptions import AnymailConfigurationError, AnymailError
from background_task import background
from django.db.models.query import Prefetch
from django.utils import timezone
from googleapiclient.errors import HttpError
from yadisk.exceptions import YaDiskError

from apps.core.models import Role, Setting
from apps.library.services.email import send_application_email
from apps.library.services.yandex_disk_export import yandex_disk_export


def get_festival_year():
    if 7 <= timezone.now().month <= 12:
        return timezone.now().year + 1
    return timezone.now().year


def generate_upload_path(instance, filename):
    festival_year = get_festival_year()
    return f"{instance.__class__.__name__}/{festival_year}/{filename}"


def get_team_roles(obj, filters: dict = None):
    """Return all roles used in event.

    Collects persons related with role using Prefetch.
    """
    roles = Role.objects.filter(**filters).distinct()
    team = obj.team_members.all()
    return roles.prefetch_related(Prefetch("team_members", team))


@background(schedule=60)
def participation_services(instance, domain, gs, logger):
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
