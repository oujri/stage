# Generated by Django 2.0.4 on 2018-04-19 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20180419_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='icon',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
