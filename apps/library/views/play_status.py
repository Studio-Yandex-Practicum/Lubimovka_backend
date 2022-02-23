from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.library.models import Play


def play_status(request, object_pk, status):
    messages.info(request, "Статус успешно обновлен!")
    instance = Play.objects.get(pk=object_pk)
    instance.status = status
    instance.save()
    return HttpResponseRedirect(reverse("admin:library_play_change", args=[object_pk]))
