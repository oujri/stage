# Generated by Django 2.0.4 on 2018-04-29 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0036_auto_20180429_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='photoDeProfil',
            field=models.ForeignKey(default=60, on_delete=models.SET(60), to='journal.Image'),
        ),
    ]
