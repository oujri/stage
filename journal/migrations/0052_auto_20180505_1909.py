# Generated by Django 2.0.4 on 2018-05-05 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0051_auto_20180505_1647'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Publisher',
            new_name='Journalist',
        ),
    ]
