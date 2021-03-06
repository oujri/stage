# Generated by Django 2.0.4 on 2018-05-12 13:08

from django.db import migrations, models
import django.db.models.deletion
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0070_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=journal.models.PathAndRename('images/2018/05/12')),
        ),
        migrations.AlterField(
            model_name='news',
            name='primary_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.Image'),
        ),
    ]
