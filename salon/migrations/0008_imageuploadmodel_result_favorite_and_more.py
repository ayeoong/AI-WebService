# Generated by Django 4.0.4 on 2022-11-07 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0007_alter_imageuploadmodel_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageuploadmodel',
            name='result_favorite',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='musicuploadmodel',
            name='result_favorite',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
