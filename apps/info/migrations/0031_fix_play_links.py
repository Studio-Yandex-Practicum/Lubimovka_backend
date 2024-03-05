# Generated by Django 3.2.23 on 2024-02-03 22:10

from django.db import migrations
from django.db.models import Value
from django.db.models.functions import Replace


def fix_links(apps, schema_editor):
    InfoLink = apps.get_model("info", "InfoLink")
    InfoLink.objects.filter(link__icontains="lubimovka.art/library?").update(link=Replace("link", Value("festival="), Value("year=")))


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0030_alter_festival_year'),
    ]

    operations = [
        migrations.RunPython(fix_links, migrations.RunPython.noop),
    ]