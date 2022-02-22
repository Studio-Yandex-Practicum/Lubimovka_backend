from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from apps.core.models import Status


def get_festival_year():
    if 7 <= timezone.now().month <= 12:
        return timezone.now().year + 1
    return timezone.now().year


def generate_upload_path(instance, filename):
    festival_year = get_festival_year()
    return f"{instance.__class__.__name__}/{festival_year}/{filename}"


def change_status(request, object_pk, status_pk, object_model, view_name):
    messages.info(request, "Статус успешно обновлен!")
    instance = object_model.objects.get(pk=object_pk)
    instance.status = Status.objects.get(pk=status_pk)
    instance.save()
    return HttpResponseRedirect(reverse(f"admin:{view_name}_change", args=[object_pk]))
