# Generated by Django 2.0.4 on 2018-05-01 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0043_auto_20180501_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='equipe_selection',
            field=models.BooleanField(default=False),
        ),
    ]
