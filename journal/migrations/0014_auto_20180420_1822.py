# Generated by Django 2.0.4 on 2018-04-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0013_auto_20180420_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='smallTitre',
            field=models.CharField(default=models.CharField(max_length=255), max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
