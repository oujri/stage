# Generated by Django 2.0.4 on 2018-05-05 15:47

from django.db import migrations, models
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0050_auto_20180504_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='datePublication',
            new_name='date_publication',
        ),
        migrations.RenameField(
            model_name='publisher',
            old_name='dateCreation',
            new_name='date_creation',
        ),
        migrations.RenameField(
            model_name='publisher',
            old_name='nom',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='publisher',
            old_name='prenom',
            new_name='last_name',
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=journal.models.PathAndRename('images/2018/05/05')),
        ),
    ]
