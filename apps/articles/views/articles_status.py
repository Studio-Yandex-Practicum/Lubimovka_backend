from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.articles.models import BlogItem, NewsItem, Project


def blog_status(request, object_pk, status):
    messages.info(request, "Статус успешно обновлен!")
    instance = BlogItem.objects.get(pk=object_pk)
    instance.status = status
    instance.save()
    return HttpResponseRedirect(reverse("admin:articles_blogitem_change", args=[object_pk]))


def news_status(request, object_pk, status):
    messages.info(request, "Статус успешно обновлен!")
    instance = NewsItem.objects.get(pk=object_pk)
    instance.status = status
    instance.save()
    return HttpResponseRedirect(reverse("admin:articles_newsitem_change", args=[object_pk]))


def project_status(request, object_pk, status):
    messages.info(request, "Статус успешно обновлен!")
    instance = Project.objects.get(pk=object_pk)
    instance.status = status
    instance.save()
    return HttpResponseRedirect(reverse("admin:articles_project_change", args=[object_pk]))
