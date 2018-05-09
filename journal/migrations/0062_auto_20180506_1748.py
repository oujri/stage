# Generated by Django 2.0.4 on 2018-05-06 16:48

from django.db import migrations, models
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0061_auto_20180505_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=journal.models.PathAndRename('images/2018/05/06')),
        ),
        migrations.AlterField(
            model_name='journalist',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
