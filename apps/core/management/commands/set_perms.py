from typing import Any, Optional

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

fixture = "apps/core/management/commands/fixture/fixture_group_perms.json"


class Command(BaseCommand):
    help = "Устанавливает права для групп пользователей Администратор и Редактор"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            call_command("loaddata", fixture, app_label="core")
            self.stdout.write(self.style.SUCCESS("Права для пользователей успешно установлены."))
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка установки прав."))
