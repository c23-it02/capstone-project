# Generated by Django 4.2.1 on 2023-06-07 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trash_can_detector', '0007_alter_gallery_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camcard',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='camcard',
            name='timestamp',
        ),
    ]