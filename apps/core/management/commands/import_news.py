import json
import logging
import re
from datetime import datetime
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone, make_aware

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.models import ContentUnitRichText, ImagesBlock, OrderedImage
from apps.core.constants import Status

GENERAL_FAILURE = "Unexpected error for entry {entry}"

logger = logging.getLogger("django")

User = get_user_model()


re_tags = re.compile(r"(<!--.*?-->|<[^>]*>)")
re_img = re.compile(r'<p.{0,40}<img src="(.{10,100}?)" .*?>.{0,40}<\/p>', flags=re.MULTILINE)


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
        image_type = ContentType.objects.get(app_label="content_pages", model="imagesblock")

        NewsItem.objects.filter(creator=archivarius).delete()

        count = 0
        for entry in data:
            try:
                intro_image = Path(json.loads(entry["images"])["image_intro"])
                full_text = entry["fulltext"]

                item = NewsItem()
                item.title = entry["title"]
                item.description = re_tags.sub("", entry["introtext"])
                item.pub_date = make_aware(datetime.fromisoformat(entry["created"]), get_current_timezone())
                item.status = Status.PUBLISHED
                item.creator = archivarius
                if intro_image:
                    image_path = BASE_PATH / intro_image
                    if image_path.exists() and image_path.is_file():
                        with open(image_path, "rb") as file:
                            image_file = File(file)
                            item.image.save(image_path.name, image_file, True)

                item.save()

                post_items = re_img.split(full_text)

                order = 1
                for index, part in enumerate(post_items):
                    part = part.strip("\r\n")
                    if not part:
                        continue
                    if index % 2 == 0:
                        rich = ContentUnitRichText()
                        rich.rich_text = part
                        rich.save()

                        blog_content = NewsItemContent()
                        blog_content.order = order
                        blog_content.item = rich
                        blog_content.content_page = item
                        blog_content.content_type = rich_type
                        blog_content.object_id = rich.pk
                        blog_content.save()
                        order += 1
                    else:
                        image_path = BASE_PATH / part
                        if image_path.exists() and image_path.is_file():
                            image_block = ImagesBlock()
                            image_block.title = image_path.name
                            image_block.save()
                            ordered_image = OrderedImage()
                            ordered_image.order = 1
                            ordered_image.block = image_block
                            with open(image_path, "rb") as file:
                                image_file = File(file)
                                ordered_image.image.save(image_path.name, image_file, True)
                            ordered_image.save()

                            blog_content = NewsItemContent()
                            blog_content.order = order
                            blog_content.item = image_block
                            blog_content.content_page = item
                            blog_content.content_type = image_type
                            blog_content.object_id = image_block.pk
                            blog_content.save()
                            order += 1

                count += 1
            except Exception:
                logger.exception(msg=GENERAL_FAILURE.format(entry=str(entry)))

        self.stdout.write(self.style.SUCCESS(f"Successfully read {count} news records"))
