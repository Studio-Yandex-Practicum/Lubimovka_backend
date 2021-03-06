# Generated by Django 3.2.12 on 2022-05-09 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_data_additional_and_updated_email_settings'),
        ('library', '0025_rename_order_in_otherlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='images_in_block',
        ),
        migrations.CreateModel(
            name='PerformanceImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.image')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_in_block', to='library.performance', verbose_name='Изображения спектакля')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.image',),
        ),
    ]
