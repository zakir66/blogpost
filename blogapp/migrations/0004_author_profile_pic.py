# Generated by Django 2.1 on 2018-08-29 08:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='profile_pic',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]
