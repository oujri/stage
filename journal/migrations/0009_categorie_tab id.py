# Generated by Django 2.0.4 on 2018-04-20 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0008_news_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='Tab id',
            field=models.CharField(default='tab1', max_length=50),
        ),
    ]
