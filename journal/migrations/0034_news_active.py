# Generated by Django 2.0.4 on 2018-04-26 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0033_remove_reponse_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
