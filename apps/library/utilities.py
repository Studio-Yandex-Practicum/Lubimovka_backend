from django.core.mail import EmailMessage
from django.db.models.query import Prefetch
from django.utils import timezone

from apps.core.models import Role, Setting
from config.settings.base import MAILJET_TEMPLATE_ID_PLAY


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


def send_play_email(serializer):
    message = EmailMessage(
        subject="Подана заявка на участие",
        from_email=Setting.get_setting("email_send_from"),
        to=(Setting.get_setting("email_on_acceptance_of_plays_page"),),
    )
    message.template_id = MAILJET_TEMPLATE_ID_PLAY
    message.merge_global_data = {
        "year": serializer.validated_data["year"],
        "birth_year": serializer.validated_data["birth_year"],
        "first_name": serializer.validated_data["last_name"],
        "last_name": serializer.validated_data["last_name"],
        "city": serializer.validated_data["city"],
        "phone_number": serializer.validated_data["phone_number"],
        "email": serializer.validated_data["email"],
        "title": serializer.validated_data["title"],
    }

    # attach file
    filename = serializer.validated_data["file"].name
    data = serializer.validated_data["file"].open().read()
    content_type = serializer.validated_data["file"].content_type
    message.attach(filename, data, content_type)
    message.send()
    return message
