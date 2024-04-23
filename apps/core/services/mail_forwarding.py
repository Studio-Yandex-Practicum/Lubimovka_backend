"""Управление записями переадресации электронной почты."""

from typing import Optional

from apps.library.models.author import Author
from apps.postfix.models import Virtual


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
