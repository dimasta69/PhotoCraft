# Generated by Django 5.0.1 on 2024-01-19 20:09

import utils.file_uploader
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0002_remove_photo_status_id_photo_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to=utils.file_uploader.uploaded_file_path, verbose_name='Фото'),
        ),
    ]
