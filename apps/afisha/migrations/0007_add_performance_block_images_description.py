# Generated by Django 3.2.13 on 2022-06-17 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0006_masterclass_performance'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='block_images_description',
            field=models.CharField(blank=True, default=None, help_text='Опишите блок с фотографиями', max_length=200, null=True, verbose_name='Заголовок для фотографий'),
        ),
    ]
