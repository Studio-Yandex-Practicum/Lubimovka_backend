from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import mixins, viewsets

from apps.library.filters import PlayFilter
from apps.library.models import Play
from apps.library.serializers import PlaySerializer


def prev_status(request, object_pk):
    messages.info(request, "Статус успешно обновлен!")
    play = Play.objects.get(pk=object_pk)
    play.status = play.status.prev()
    play.save()
    return HttpResponseRedirect(reverse("admin:library_play_change", args=[object_pk]))


def next_status(request, object_pk):
    messages.info(request, "Статус успешно обновлен!")
    play = Play.objects.get(pk=object_pk)
    play.status = play.status.next()
    play.save()
    return HttpResponseRedirect(reverse("admin:library_play_change", args=[object_pk]))


class PlayViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    filterset_class = PlayFilter
