# Generated by Django 2.0.4 on 2018-04-29 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0038_auto_20180429_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='dateCreation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]