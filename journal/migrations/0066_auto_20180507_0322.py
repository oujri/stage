# Generated by Django 2.0.4 on 2018-05-07 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0065_auto_20180507_0225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journalist',
            name='user',
        ),
        migrations.AddField(
            model_name='journalist',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='journalist',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='journalist',
            name='first_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='journalist',
            name='last_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]