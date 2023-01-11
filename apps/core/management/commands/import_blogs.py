import json
import re
from datetime import datetime
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone, make_aware

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.models import ContentUnitRichText

User = get_user_model()


tags = re.compile(r"(<!--.*?-->|<[^>]*>)")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("json")
        parser.add_argument("folder")

    def handle(self, *args, **options):
        JSON_FILE = options["json"]
        BASE_PATH = Path(options["folder"])
        with open(JSON_FILE, "r") as file:
            data = next(iter(json.load(file).values()))

        archivarius, _ = User.objects.get_or_create(username="archivarius", last_name="Архивариус")
        rich_type = ContentType.objects.get(app_label="content_pages", model="contentunitrichtext")

        BlogItem.objects.filter(creator=archivarius).delete()

        count = 0
        for entry in data:
            intro_image = Path(json.loads(entry["images"])["image_intro"])

            rich = ContentUnitRichText()
            rich.rich_text = entry["fulltext"]
            rich.save()

            item = BlogItem()
            item.title = entry["title"]
            item.description = tags.sub("", entry["introtext"])
            item.pub_date = make_aware(datetime.fromisoformat(entry["created"]), get_current_timezone())
            item.creator = archivarius
            if intro_image:
                image_path = BASE_PATH / intro_image
                if image_path.exists() and image_path.is_file():
                    with open(image_path, "rb") as file:
                        image_file = File(file)
                        item.image.save(image_path.name, image_file, True)

            item.save()

            blog_content = BlogItemContent()
            blog_content.item = rich
            blog_content.content_page = item
            blog_content.content_type = rich_type
            blog_content.object_id = rich.pk
            blog_content.save()

            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully read {count} blog records"))
