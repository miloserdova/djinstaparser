# Generated by Django 3.0.7 on 2020-06-07 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_instaparser', '0002_auto_20200607_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image_url',
            field=models.TextField(verbose_name='Адрес изображения'),
        ),
    ]
