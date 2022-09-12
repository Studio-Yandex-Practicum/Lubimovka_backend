import os
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Устанавливает сортировку объектов при создании их с помощью фабрик."

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        models = (
            "info.FestTeamMember",
            "info.Partner",
            "info.Sponsor",
            "info.Place",
            "main.Banner",
            "library.AuthorPlay",
            "library.TeamMember",
            "core.Role",
        )
        try:
            for model in models:
                os.system(f"./manage.py reorder {model}")
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка выполнения команды."))
