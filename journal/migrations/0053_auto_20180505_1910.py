# Generated by Django 2.0.4 on 2018-05-05 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0052_auto_20180505_1909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journalist',
            old_name='photoDeProfil',
            new_name='photo_de_profil',
        ),
    ]
