# Generated by Django 2.0.4 on 2018-05-01 15:37

from django.db import migrations, models
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0044_video_equipe_selection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=journal.models.PathAndRename('images/%Y/%m/%d')),
        ),
    ]
