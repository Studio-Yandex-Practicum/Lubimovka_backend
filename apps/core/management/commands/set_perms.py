from typing import Any, Optional

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q


class Command(BaseCommand):
    help = "Устанавливает права для групп пользователей Администратор и Редактор"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            editors_permissions = Permission.objects.filter(
                Q(codename__endswith="access_level_2")
                # permissions for author, play, blog, news, performance, person, role
                | Q(codename__endswith="_authorplay")
                | Q(codename__endswith="_author")
                | Q(codename__endswith="_blogitem")
                | Q(codename__endswith="_blogitemcontent")
                | Q(codename__endswith="_contentpersonrole")
                | Q(codename__endswith="_contentunitrichtext")
                | Q(codename__endswith="_eventsblock")
                | Q(codename__endswith="_extendedperson")
                | Q(codename__endswith="_imagesblock")
                | Q(codename__endswith="_link")
                | Q(codename__endswith="_newsitem")
                | Q(codename__endswith="_newsitemcontent")
                | Q(codename__endswith="_orderedevent")
                | Q(codename__endswith="_orderedimage")
                | Q(codename__endswith="_orderedplay")
                | Q(codename__endswith="_orderedvideo")
                | Q(codename__endswith="_otherlink")
                | Q(codename__endswith="_person")
                | Q(codename__endswith="_personsblock")
                | Q(codename__endswith="_performance")
                | Q(codename__endswith="_performancemediareview")
                | Q(codename__endswith="_performancereview")
                | Q(codename__endswith="_performanceimage")
                | Q(codename__endswith="_play")
                | Q(codename__endswith="_playsblock")
                | Q(codename__endswith="_teammember")
                | Q(codename__endswith="_socialnetworklink")
                | Q(codename__endswith="_videosblock")
                | Q(codename__endswith="_role")
            )

            journalist_permissions = Permission.objects.filter(
                Q(codename__endswith="access_level_1")
                # permissions for blog and news
                | Q(codename__endswith="_blogitem")
                | Q(codename__endswith="_blogitemcontent")
                | Q(codename__endswith="_blogperson")
                | Q(codename__endswith="_contentpersonrole")
                | Q(codename__endswith="_contentunitrichtext")
                | Q(codename__endswith="_eventsblock")
                | Q(codename__endswith="_extendedperson")
                | Q(codename__endswith="_imagesblock")
                | Q(codename__endswith="_link")
                | Q(codename__endswith="_newsitem")
                | Q(codename__endswith="_newsitemcontent")
                | Q(codename__endswith="_orderedevent")
                | Q(codename__endswith="_orderedimage")
                | Q(codename__endswith="_orderedperformance")
                | Q(codename__endswith="_orderedplay")
                | Q(codename__endswith="_orderedvideo")
                | Q(codename__endswith="_personsblock")
                | Q(codename__endswith="_playsblock")
                | Q(codename__endswith="_videosblock")
                | Q(codename="view_person")
            )

            admin_permissions = Permission.objects.all().exclude(
                Q(codename__endswith="access_level_2") | Q(codename__endswith="access_level_1")
            )

            observer_permissions = Permission.objects.filter(Q(codename__icontains="view_"))

            admin, created = Group.objects.get_or_create(name="admin")
            admin.permissions.set(admin_permissions)

            editor, created = Group.objects.get_or_create(name="editor")
            editor.permissions.set(editors_permissions)

            journalist, created = Group.objects.get_or_create(name="journalist")
            journalist.permissions.set(journalist_permissions)

            observer, created = Group.objects.get_or_create(name="observer")
            observer.permissions.set(observer_permissions)

            # Удалить разрешения для приложений Sites и Sessions
            deleted_permissions = Permission.objects.filter(
                Q(codename__icontains="_site") | Q(codename__icontains="_session")
            )
            deleted_permissions.delete()

            self.stdout.write(self.style.SUCCESS("Права для пользователей успешно установлены."))
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка установки прав."))
