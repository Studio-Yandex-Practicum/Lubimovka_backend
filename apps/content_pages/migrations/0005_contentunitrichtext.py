# Generated by Django 3.2.12 on 2022-04-15 20:29

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_pages', '0004_added_eventsblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentUnitRichText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('rich_text', ckeditor.fields.RichTextField(verbose_name='Форматированный текст')),
            ],
            options={
                'verbose_name': 'Форматированный текст',
                'verbose_name_plural': 'Форматированные тексты',
            },
        ),
    ]
