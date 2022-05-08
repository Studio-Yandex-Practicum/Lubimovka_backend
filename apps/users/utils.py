from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.core.models import Setting
from apps.core.services.send_email import send_email
from apps.core.utils import get_domain


def send_reset_password_email(request, obj, template_id):
    domain = get_domain(request)
    uid = urlsafe_base64_encode(force_bytes(obj.pk))
    token = default_token_generator.make_token(obj)
    reverse_link = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
    link = f"{domain}{reverse_link}"

    context = {
        "full_name": obj.get_full_name(),
        "username": obj.get_username(),
        "email": obj.email,
        "domain": domain,
        "link": link,
    }
    send_email(
        from_email=Setting.get_setting("email_send_from"),
        to_emails=(obj.email,),
        template_id=template_id,
        context=context,
    )
