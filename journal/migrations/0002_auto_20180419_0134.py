# Generated by Django 2.0.4 on 2018-04-19 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='uploads/images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('lien', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='imagePrincipale',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='journal.Image'),
            preserve_default=False,
        ),
    ]