from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.core.tests.factories import UserFactory


class Command(BaseCommand):
    help = (
        "Заполняет базу данных тестовыми данными и сейчас доступны:"
        " - Персоны"
        " - Персоны с фотографией"
        " - Персоны с фотографией, городом проживания и email"
        " - Партнёры"
        " - Волонтёры"
        " - Попечители"
        " - Команды фестиваля"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            users_editors = []
            users_admins = []
            index = 1
            for _ in range(5):
                users_editors.append(
                    UserFactory.create(
                        username=f"editor_{index}", add_role_editor=True
                    )
                )
                users_admins.append(
                    UserFactory.create(
                        username=f"admin_{index}", add_role_admin=True
                    )
                )
                index += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(users_editors)} редакторов созданы успешно."
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(users_admins)} админов созданы успешно."
                )
            )
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка наполения БД"))
