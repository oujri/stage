# Generated by Django 2.0.4 on 2018-05-04 14:22

from django.db import migrations, models
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0047_auto_20180502_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'CommentsFilter',
            },
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=journal.models.PathAndRename('images/2018/05/04')),
        ),
    ]