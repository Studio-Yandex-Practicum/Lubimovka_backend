"""Управление записями переадресации электронной почты."""

from typing import Callable, Optional

from apps.library.models.author import Author
from apps.postfix.models import Virtual

MAIL_CREATED = "Создан или обновлен виртуальный адрес '{virtual_email}'"
MAIL_DELETED = "Виртуальный адрес '{virtual_email}' был удален"


def create_forwarding(author: Author) -> Virtual:
    virtual_email: Optional[Virtual] = getattr(author, "virtual_email", None)
    if not virtual_email:
        virtual_email = Virtual(author=author, mailbox=author.slug)
        virtual_email.save()
    else:
        virtual_email.mailbox = author.slug
        virtual_email.recipients.all().delete()
    virtual_email.recipients.create(email=author.person.email)
    author.virtual_email = virtual_email
    return virtual_email


def delete_forwarding(author: Author) -> Optional[Virtual]:
    virtual_email: Optional[Virtual] = getattr(author, "virtual_email", None)
    if virtual_email:
        virtual_email.delete()
    author.virtual_email = None
    return virtual_email


def on_change(instance: Author, create: bool, message: Callable[[str], None]) -> Optional[Virtual]:
    if create:
        virtual_email = create_forwarding(instance)
        message(MAIL_CREATED.format(virtual_email=virtual_email))
    else:
        virtual_email = delete_forwarding(instance)
        if virtual_email:
            message(MAIL_DELETED.format(virtual_email=virtual_email))
    return virtual_email
